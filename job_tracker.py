import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

company = "Amazon"
url = "https://www.amazon.jobs/en/search?base_query=Data+Engineer&location=India"

print(f"🔍 Checking {company} job site...")

results = []

try:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    res = requests.get(url, headers=headers, timeout=20)

    if res.status_code != 200:
        print(f"⚠️ Unable to access {company} page. Status: {res.status_code}")
    else:
        soup = BeautifulSoup(res.text, "html.parser")

        for tag in soup.find_all(["a", "h3", "span"], text=True):
            title = tag.text.strip()
            if "Data Engineer" in title:
                results.append({
                    "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Company": company,
                    "Job Title": title,
                    "Link": url
                })

except Exception as e:
    print(f"🔴 Error: {e}")

# Always create CSV, even if empty
filename = f"job_updates_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
pd.DataFrame(results).to_csv(filename, index=False, encoding="utf-8-sig")

# Debug print
print(f"✅ Saved {len(results)} job(s) to file: {filename}")
print(f"📁 File exists: {os.path.exists(filename)} at {os.getcwd()}")
