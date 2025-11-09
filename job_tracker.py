import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

companies = {
    "Salesforce": "https://careers.salesforce.com/en/jobs/?search=data%20engineer&location=India",
    "Apple": "https://jobs.apple.com/en-in/search?team=software-services&location=india",
    "Atlassian": "https://www.atlassian.com/company/careers/all-jobs",
}

print("🔍 Checking job sites...")

results = []

for company, url in companies.items():
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        res = requests.get(url, headers=headers, timeout=20)

        if res.status_code != 200:
            print(f"⚠️  {company}: Failed to access ({res.status_code})")
            continue

        soup = BeautifulSoup(res.text, "html.parser")

        found = 0
        for tag in soup.find_all(["a", "h3", "span"], text=True):
            title = tag.text.strip()
            if "Data Engineer" in title:
                results.append({
                    "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Company": company,
                    "Job Title": title,
                    "Link": url
                })
                found += 1

        print(f"🟢 {company}: Found {found} possible job(s)")

    except Exception as e:
        print(f"🔴 {company}: Error - {e}")

# Save results (always creates CSV)
filename = f"job_updates_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
pd.DataFrame(results).to_csv(filename, index=False, encoding="utf-8-sig")
print(f"✅ Saved {len(results)} total job(s) to {filename}")
