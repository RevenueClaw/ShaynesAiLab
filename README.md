# Shayne's AI Lab Website

**Live Site:** https://shaynesailab.com

## Files in This Repo

| File | Purpose |
|------|---------|
| `index.html` | Main website with email capture form |
| `logo.png` | Your logo file (REPLACE THIS with your actual logo) |
| `AI-STARTER-KIT.md` | The lead magnet content (convert to PDF) |
| `GOOGLE-SHEETS-SETUP.md` | Instructions for setting up free email capture |

## Setup Required

### 1. Replace Logo
**Action needed:** Replace `logo.png` with your actual logo file (the one you uploaded).

```bash
cp /path/to/your/actual/logo.png ./logo.png
```

### 2. Create PDF Deliverable
Convert `AI-STARTER-KIT.md` to PDF:

**Option A: Google Docs**
1. Copy content from `AI-STARTER-KIT.md`
2. Paste into Google Docs
3. File → Download → PDF
4. Upload as `ai-starter-kit.pdf`

**Option B: Markdown to PDF tools**
- md2pdf.netlify.app
- pandoc (command line)

**Option C: Canva**
- Create a simple PDF design
- Copy content from the markdown file

### 3. Set Up Email Capture
Follow instructions in `GOOGLE-SHEETS-SETUP.md` to:
- Create Google Sheet for leads
- Create webhook to capture emails
- Auto-send the PDF to subscribers

### 4. Update Webhook URL
In `index.html`, replace `YOUR_SCRIPT_ID_HERE` with your actual Google Apps Script URL.

### 5. Deploy
Push to GitHub, Cloudflare will auto-deploy.

## What Works Now

- ✅ Complete website design
- ✅ Email capture form (just needs webhook URL)
- ✅ Responsive layout
- ✅ Dark theme matching your logo
- ✅ "Brutal honesty" messaging throughout
- ✅ Workshop #1 ($29) and #2 ($39) displayed

## What's Missing (You Need To Do)

1. **Replace logo.png** with your actual logo file
2. **Create PDF** from AI-STARTER-KIT.md
3. **Set up Google Sheets webhook** (free)
4. **Test the form** to make sure emails arrive

## Questions?

Email: hello@shaynesailab.com