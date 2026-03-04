---
name: social-media-post
description: |
  Post to Facebook, Instagram, and Twitter/X via Gold-Tier MCP servers.
  All posts go through human approval (HITL) before publishing.
  Generates weekly engagement summaries for the CEO Briefing.
  Use when asked to post to any social platform or generate social media reports.
---

# Social Media Post Skill

**Purpose**: Manage Facebook, Instagram, and Twitter/X content with human-in-the-loop approval
**Tier**: Gold
**MCP Servers**: `facebook-instagram`, `twitter-x`
**Safety**: DRY_RUN=true by default — set to false in .env to post for real

---

## When to Use

- User asks to post on Facebook, Instagram, or Twitter
- Business milestone to announce on all platforms
- Weekly social media performance summary needed
- CEO Briefing social section generation

---

## Cross-Platform Posting Workflow

### Step 1 — Draft the content

For business content:
- Use the `linkedin-post` skill format as a template
- Adapt: Twitter max 280 chars, Facebook/Instagram no char limit
- Each platform has its own best practices

### Step 2 — Post to platforms

#### Facebook
```
Tool: post_to_facebook
MCP: facebook-instagram
Arguments:
  message: "Your Facebook post text here..."
  link: "https://yourwebsite.com"  (optional)
```

#### Instagram
```
Tool: post_to_instagram
MCP: facebook-instagram
Arguments:
  caption: "Your caption with #hashtags"
  image_url: "https://public-image-url.com/image.jpg"
```
Note: Instagram requires a public image URL (JPEG/PNG, min 500px).

#### Twitter / X
```
Tool: post_tweet
MCP: twitter-x
Arguments:
  text: "Tweet text (max 280 chars) #hashtags"
```

### Step 3 — All posts go to approval

Each platform post creates a file in `Pending_Approval/`:
- `FB_POST_{timestamp}.md`
- `IG_POST_{timestamp}.md`
- `TWEET_{timestamp}.md`

### Step 4 — Human reviews and approves

Move approval file to `Approved/` → Gold orchestrator publishes automatically.

---

## Social Media Summaries

### Get Facebook performance
```
Tool: get_facebook_summary
MCP: facebook-instagram
Arguments:
  period_days: 7
```

### Get Instagram performance
```
Tool: get_instagram_summary
MCP: facebook-instagram
Arguments:
  period_days: 7
```

### Get Twitter performance
```
Tool: get_twitter_summary
MCP: twitter-x
Arguments:
  period_days: 7
  max_tweets: 10
```

Summaries are saved to `Social_Media/` and included in the CEO Briefing.

---

## Platform Best Practices

### Facebook
- Best posting time: 1-3pm weekdays
- Optimal length: 40-80 words
- Include a question or CTA
- Business updates + project milestones work well

### Instagram
- Must have an image (required by API)
- Caption: 125 chars before "more" — make first line count
- Use 5-10 relevant hashtags
- High-quality image = higher engagement

### Twitter / X
- Max 280 characters
- First 5 words must hook the reader
- Thread for longer content (reply to your own tweet)
- 1-2 hashtags max (more = spam)

---

## Content Calendar (Suggested)

| Day | Platform | Content Type |
|-----|----------|-------------|
| Monday | LinkedIn | CEO Briefing insight |
| Tuesday | Twitter | Industry tip |
| Wednesday | Facebook | Project milestone |
| Thursday | Instagram | Behind-the-scenes |
| Friday | All | Week recap |

---

## Setup Required

### Facebook + Instagram
1. Create Facebook Developer App
2. Add Page + Instagram products
3. Get permanent Page Access Token
4. Set in `.env`: `FB_PAGE_ID`, `FB_PAGE_ACCESS_TOKEN`, `IG_ACCOUNT_ID`
5. Set `ENABLE_FACEBOOK=true` and/or `ENABLE_INSTAGRAM=true`

### Twitter / X
1. Create Twitter Developer Account
2. Create App with Read + Write permissions
3. Generate Access Token + Secret
4. Set in `.env`: `TWITTER_*` variables
5. Set `ENABLE_TWITTER=true`

**See:** `Gold-Tier/config/social_media_setup.md` for step-by-step guides.

---

**Status**: Production Ready
**Tier**: Gold
**Safety**: All posts require human approval. DRY_RUN=true blocks real publishing.
**Related**: `linkedin-post` skill (LinkedIn), `weekly-audit` skill (social reports)
