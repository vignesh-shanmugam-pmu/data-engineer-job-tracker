import pandas as pd
from datetime import datetime
import json
import os
import gspread
from google.oauth2.service_account import Credentials

# 🔹 Step 1: Create test job data
data = [
    [datetime.now().strftime("%Y-%m-%d %H:%M"), "TestCompany", "Data Engineer I", "https://example.com/job1"],
    [datetime.now().strftime("%Y-%m-%d %H:%M"), "TestCompany", "Data Engineer II", "https://example.com/job2"],
    [datetime.now().strftime("%Y-%m-%d %H:%M"), "TestCompany", "Senior Data Engineer", "https://example.com/job3"],
]

df = pd.DataFrame(data, columns=["Date", "Company", "Job Title", "Link"])

# 🔹 Step 2: Save test data to CSV (for artifact)
filename = f"job_updates_test_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
df.to_csv(filename, index=False, encoding="utf-8-sig")
print(f"✅ Dummy CSV created: {filename}")

# 🔹 Step 3: Send to Google Sheets (if creds exist)
if "GOOGLE_SHEETS_CREDS" in os.environ:
    creds_json = json.loads(os.environ["GOOGLE_SHEETS_CREDS"])
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_info(creds_json, scopes=SCOPES)
    gc = gspread.authorize(creds)

    SHEET_ID = "1ieePp_GWfQDzonyHJCof9KRmIa0_VtwoJ0CP6curfOQ"  # paste your Sheet ID here
    worksheet = gc.open_by_key(SHEET_ID).sheet1

    worksheet.clear()
    worksheet.append_row(["Date", "Company", "Job Title", "Link"])
    worksheet.append_rows(df.values.tolist())

    print(f"✅ Uploaded {len(df)} test rows to Google Sheet successfully.")
else:
    print("⚠️ GOOGLE_SHEETS_CREDS not found, skipping sheet upload.")
