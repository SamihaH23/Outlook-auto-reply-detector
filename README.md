# Outlook Auto-Reply Detector (MS Graph API + MSAL)

This Python script connects to Microsoft Graph API using MSAL, 
fetches emails from a mailbox, and detects auto-replies 
(e.g., "Out of Office", "Undeliverable", "Vacation Message").

## Features
- Authenticate with MSAL (client credentials flow)
- Fetch recent emails from Outlook via Graph API
- Detect common auto-reply patterns

## Setup
1. Clone this repo
2. Create a `.env` file (see `.env.example`)
3. Install dependencies:
   ```bash
   pip install -r requirements.txt


