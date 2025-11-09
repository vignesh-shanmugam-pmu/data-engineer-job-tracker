import pandas as pd
from datetime import datetime
import json
import os
import gspread
from google.oauth2.service_account import Credentials

# 🔹 Step 1: Define Atlassian Job Page
ATLAS_URL = "https://www.atlassian.com/company/careers/all-jobs?team=&location=India&search=Data%20Engineer"

# 🔹 Step 2: Create simple log entry
data = [
    [
        datetime.now().strftime("%Y-%m-%d %H:%M"),
        "Atlassian",
        "Data Engineer Jobs (India)",
        ATLAS_URL,
    ]
]

df = pd.DataFrame(data, columns=["Date", "Company", "Job Title", "Link"])

# 🔹 Step 3: Save to CSV (for GitHub artifact)
filename = f"job_updates_atlassian_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
df.to_csv(filename, index=False, encoding="utf-8-sig")
print(f"✅ CSV created: {filename}")

# 🔹 Step 4: Upload to Google Sheets
if "GOOGLE_SHEETS_CREDS" in os.environ:
    creds_json = json.loads(os.environ["GOOGLE_SHEETS_CREDS"])
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_info(creds_json, scopes=SCOPES)
    gc = gspread.authorize(creds)

    SHEET_ID = "1ieePp_GWfQDzonyHJCof9KRmIa0_VtwoJ0CP6curfOQ"  # paste your Google Sheet ID here
    worksheet = gc.open_by_key(SHEET_ID).sheet1

    # Append instead of clearing (keeps history)
    existing_data = worksheet.get_all_values()
    if not existing_data:
        worksheet.append_row(["Date", "Company", "Job Title", "Link"])

    worksheet.append_rows(df.values.tolist())

    print(f"✅ Added Atlassian job link to Google Sheet successfully.")
else:
    print("⚠️ GOOGLE_SHEETS_CREDS not found, skipping sheet upload.")
