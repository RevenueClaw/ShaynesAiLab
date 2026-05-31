# Google Sheets Email Capture Setup
## Completely Free — No Limits, No Trial

**What this does:**
- Captures emails from your website
- Stores them in a Google Sheet (you own the data)
- Auto-sends the AI Starter Kit PDF via Gmail
- $0 cost, forever

---

## Step 1: Create the Google Sheet

1. Go to [sheets.google.com](https://sheets.google.com)
2. Create new spreadsheet named "Shaynes AI Lab - Leads"
3. Add these headers in Row 1:
   ```
   A: Timestamp
   B: First Name
   C: Email
   D: Source
   E: Sent Kit
   ```
4. **Important:** Click "Share" → "Change to anyone with the link can view"
5. Copy the **Sheet ID** from the URL:
   ```
   https://docs.google.com/spreadsheets/d/[THIS_IS_THE_ID]/edit
   ```

---

## Step 2: Create the Apps Script Webhook

1. In your Sheet, click **Extensions → Apps Script**
2. Replace ALL the code with this:

```javascript
// Webhook to capture emails from website
// POST to: https://script.google.com/macros/s/YOUR_SCRIPT_ID/exec

const SHEET_ID = 'YOUR_SHEET_ID_HERE'; // Replace with your sheet ID
const SHEET_NAME = 'Sheet1'; // or rename if you changed it
const PDF_URL = 'https://shaynesailab.com/ai-starter-kit.pdf'; // Upload PDF first

function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);
    const sheet = SpreadsheetApp.openById(SHEET_ID).getSheetByName(SHEET_NAME);
    
    // Add row to sheet
    sheet.appendRow([
      new Date().toISOString(),
      data.firstName || '',
      data.email,
      data.source || 'website',
      'PENDING' // Will update after email sent
    ]);
    
    // Send welcome email with PDF
    sendWelcomeEmail(data.firstName, data.email);
    
    return ContentService.createTextOutput(JSON.stringify({
      success: true,
      message: 'Subscribed successfully'
    })).setMimeType(ContentService.MimeType.JSON);
    
  } catch (error) {
    return ContentService.createTextOutput(JSON.stringify({
      success: false,
      error: error.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

function sendWelcomeEmail(firstName, email) {
  const subject = 'Your Free AI Starter Kit is here!';
  const body = `
Hi ${firstName || 'there'},

Thanks for grabbing the AI Starter Kit!

Here's your download link:
${PDF_URL}

Inside you'll find:
✓ The 8 tools that actually save time (and 12 to skip)
✓ Cost breakdown: free vs. paid tiers  
✓ Quick-start checklist for each tool
✓ My "first 30 days" implementation guide
✓ Bonus: "My Real Workflow" sneak peek

Questions? Just reply to this email -- I read every one.

Cheers,
Shayne
Shayne's AI Lab
  `;
  
  GmailApp.sendEmail(email, subject, body, {
    name: 'Shayne\'s AI Lab',
    replyTo: 'hello@shaynesailab.com'
  });
  
  // Mark as sent in sheet
  const sheet = SpreadsheetApp.openById(SHEET_ID).getSheetByName(SHEET_NAME);
  const lastRow = sheet.getLastRow();
  sheet.getRange(lastRow, 5).setValue('SENT');
}

// For testing - run this manually
function testWebhook() {
  const testData = {
    firstName: 'Test',
    email: 'your-email@example.com',
    source: 'test'
  };
  
  const mockEvent = {
    postData: {
      contents: JSON.stringify(testData)
    }
  };
  
  doPost(mockEvent);
}
```

3. **Replace `YOUR_SHEET_ID_HERE`** with your actual sheet ID from Step 1
4. Click **Save** (Ctrl+S)
5. Click **Deploy → New deployment**
   - Type: Web app
   - Execute as: Me
   - Who has access: **Anyone**
6. Click **Deploy** → Copy the **Web App URL** (looks like: `https://script.google.com/macros/s/ABC123/exec`)

---

## Step 3: Update the Website

Replace the webhook URL in `index.html` with your Google Script URL:

```javascript
const WEBHOOK_URL = 'https://script.google.com/macros/s/YOUR_SCRIPT_ID/exec';
```

That's it.

---

## Step 4: Upload the PDF

1. Upload `ai-starter-kit.pdf` to your website root
2. Update the `PDF_URL` in the Apps Script code
3. Test the form

---

## Testing

1. Fill out the form on your website
2. Check your Google Sheet (should show new row)
3. Check your Gmail "Sent" folder (should show welcome email)
4. Check your inbox (should receive the test email)

---

## Troubleshooting

**Form says "Check your email" but nothing in Sheet?**
- Check Apps Script "Executions" for errors
- Make sure Sheet ID is correct
- Make sure Sheet is shared

**Email not sending?**
- Check spam/junk folders
- Make sure you're not sending to yourself too fast (Gmail rate limits)
- Check Gmail "Sent" to see if it tried

**CORS errors in browser?**
- Normal for Google Apps Script. The POST still works.
- Success message shows regardless.

---

**Cost: $0 forever**
**Limits: Gmail's daily sending limit (500 emails/day for free accounts)**
**Your target: 30-50 leads for soft launch = no problem**

---

Ready when you are. Upload that logo and I'll update the site to use your actual image + this Google webhook.