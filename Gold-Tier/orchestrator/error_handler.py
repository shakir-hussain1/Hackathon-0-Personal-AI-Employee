"""
Gold-Tier Error Handler
Implements exponential backoff retry (Section 7.2) and graceful degradation (Section 7.3).
Every Gold-Tier action wraps through here.
"""

import time
import logging
import functools
from typing import Callable, Type

logger = logging.getLogger('gold.error_handler')

# Error categories (Section 7.1)
class TransientError(Exception):
    """Network timeout, rate limit — safe to retry."""
    pass

class AuthError(Exception):
    """Expired token, revoked access — alert human, pause."""
    pass

class LogicError(Exception):
    """Misinterpretation — send to human review queue."""
    pass

class DataError(Exception):
    """Corrupted file, missing field — quarantine + alert."""
    pass

class SystemError(Exception):
    """Orchestrator crash, disk full — watchdog handles."""
    pass


def with_retry(
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    retryable: tuple = (TransientError, ConnectionError, TimeoutError),
    on_failure: Callable = None,
):
    """
    Exponential backoff retry decorator (Section 7.2).
    Retries on transient errors, raises immediately on auth/logic/data errors.

    Usage:
        @with_retry(max_attempts=3, base_delay=2)
        def call_api():
            ...
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except retryable as e:
                    last_error = e
                    if attempt == max_attempts - 1:
                        logger.error(f'{func.__name__} failed after {max_attempts} attempts: {e}')
                        if on_failure:
                            on_failure(e)
                        raise
                    delay = min(base_delay * (2 ** attempt), max_delay)
                    logger.warning(
                        f'{func.__name__} attempt {attempt + 1}/{max_attempts} failed: {e}. '
                        f'Retrying in {delay:.1f}s...'
                    )
                    time.sleep(delay)
                except (AuthError, LogicError, DataError) as e:
                    # Never retry these — alert immediately
                    logger.error(f'{func.__name__} non-retryable error [{type(e).__name__}]: {e}')
                    raise
                except Exception as e:
                    # Classify unknown exceptions as transient for safety
                    last_error = e
                    if attempt == max_attempts - 1:
                        logger.error(f'{func.__name__} unexpected error: {e}')
                        raise
                    delay = min(base_delay * (2 ** attempt), max_delay)
                    logger.warning(f'{func.__name__} unexpected error (attempt {attempt + 1}): {e}. Retry in {delay:.1f}s')
                    time.sleep(delay)
            raise last_error
        return wrapper
    return decorator


def safe_run(func: Callable, *args, default=None, log_errors: bool = True, **kwargs):
    """
    Run func safely — returns default on any exception.
    Used for non-critical operations that should not crash the orchestrator.
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        if log_errors:
            logger.error(f'safe_run({func.__name__}) failed: {e}')
        return default


class CircuitBreaker:
    """
    Circuit breaker pattern — after N consecutive failures, stop calling
    the service for RECOVERY_TIMEOUT seconds (graceful degradation).
    """

    def __init__(self, name: str, failure_threshold: int = 5, recovery_timeout: int = 300):
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self._failures = 0
        self._last_failure_time = 0
        self._open = False

    @property
    def is_open(self) -> bool:
        if self._open:
            if time.time() - self._last_failure_time > self.recovery_timeout:
                logger.info(f'CircuitBreaker [{self.name}] half-open — trying recovery')
                self._open = False
                return False
        return self._open

    def record_success(self):
        self._failures = 0
        self._open = False

    def record_failure(self):
        self._failures += 1
        self._last_failure_time = time.time()
        if self._failures >= self.failure_threshold:
            if not self._open:
                logger.warning(
                    f'CircuitBreaker [{self.name}] OPEN after {self._failures} failures. '
                    f'Pausing for {self.recovery_timeout}s.'
                )
            self._open = True

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if self.is_open:
                raise TransientError(
                    f'CircuitBreaker [{self.name}] is open — service temporarily unavailable'
                )
            try:
                result = func(*args, **kwargs)
                self.record_success()
                return result
            except Exception as e:
                self.record_failure()
                raise
        return wrapper


# Pre-built circuit breakers for Gold-Tier services
odoo_breaker = CircuitBreaker('odoo', failure_threshold=3, recovery_timeout=120)
meta_breaker = CircuitBreaker('meta_api', failure_threshold=5, recovery_timeout=300)
twitter_breaker = CircuitBreaker('twitter_api', failure_threshold=5, recovery_timeout=300)
