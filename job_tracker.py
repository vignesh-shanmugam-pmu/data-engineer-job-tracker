import json
import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

companies = {
    "Cognizant": "https://careers.cognizant.com/us-en/jobs/?keyword=Data+Engineer&location=India&lat=&lng=&cname=India&ccode=IN&origin=global"
}

# 🔹 scrape jobs (simplified)
results = []
for company, url in companies.items():
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        res = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(res.text, "html.parser")
        for tag in soup.find_all(["a", "h3", "span"], text=True):
            title = tag.text.strip()
            if "Data Engineer" in title:
                results.append([datetime.now().strftime("%Y-%m-%d %H:%M"), company, title, url])
    except Exception as e:
        print(f"Error: {company} - {e}")

df = pd.DataFrame(results, columns=["Date", "Company", "Job Title", "Link"])

# 🔹 write to Google Sheet
creds_json = json.loads(os.environ["GOOGLE_SHEETS_CREDS"])
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_info(creds_json, scopes=SCOPES)
gc = gspread.authorize(creds)

SHEET_ID = "1ieePp_GWfQDzonyHJCof9KRmIa0_VtwoJ0CP6curfOQ"
worksheet = gc.open_by_key(SHEET_ID).sheet1

# clear & write fresh data
worksheet.clear()
worksheet.append_row(["Date", "Company", "Job Title", "Link"])
if not df.empty:
    worksheet.append_rows(df.values.tolist())
    print(f"✅ Uploaded {len(df)} rows to Google Sheet")
else:
    print("⚪ No jobs found, but sheet cleared successfully.")
