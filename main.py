from msal import ConfidentialClientApplication
import requests
import re

# ====== CONFIG ======
CLIENT_ID = "Your App (client) ID"
TENANT_ID = "Your Tenant ID"
CLIENT_SECRET = "# <-- Secret VALUE, not Secret ID!"

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/.default"]  # Application perms

# ====== AUTHENTICATE ======
app = ConfidentialClientApplication(
    CLIENT_ID,
    authority=AUTHORITY,
    client_credential=CLIENT_SECRET
)

result = app.acquire_token_for_client(scopes=SCOPES)

if "access_token" not in result:
    raise Exception("Failed to get token:", result)

access_token = result["access_token"]
print("✅ Got token without interactive login")

# ====== CALL GRAPH API ======
headers = {"Authorization": f"Bearer {access_token}"}
user_id = "Your email"  # Mailbox to scan
url = f"https://graph.microsoft.com/v1.0/users/{user_id}/messages?$top=20&$select=subject,from,receivedDateTime,bodyPreview"
resp = requests.get(url, headers=headers)
if resp.status_code != 200:
    raise Exception(f"Graph API call failed: {resp.status_code} {resp.text}")

emails = resp.json().get("value", [])

# ====== AUTO-REPLY DETECTION ======
auto_reply_patterns = [
    r"out of office",
    r"auto.?reply",
    r"automatic reply",
    r"away from.*office",
    r"undeliverable",
    r"delivery status notification",
    r"mail delivery subsystem",
    r"vacation(.*)message"
]

print("\n🔍 Auto-replies in last 20 emails:\n")

found_any = False
for mail in emails:
    subject = mail.get("subject", "") or ""
    sender = mail.get("from", {}).get("emailAddress", {}).get("address", "")
    date = mail.get("receivedDateTime", "")
    preview = mail.get("bodyPreview", "") or ""

    text_to_check = (subject + " " + preview).lower()

    if any(re.search(pat, text_to_check, re.IGNORECASE) for pat in auto_reply_patterns):
        found_any = True
        print("⚠️ Auto-reply detected")
        print("📌 Subject:", subject)
        print("👤 From:", sender)
        print("📅 Date:", date)
        print("📨 Preview:", preview[:500], "\n---\n")

if not found_any:
    print("✅ No auto-replies found in the last 20 emails")
