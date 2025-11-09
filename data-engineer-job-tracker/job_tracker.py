import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

company = "Amazon"
url = "https://www.amazon.jobs/en/search?base_query=Data+Engineer&location=India"

print(f"🔍 Checking {company} job site...")

try:
    res = requests.get(url, timeout=15)
    soup = BeautifulSoup(res.text, "html.parser")

    job_cards = soup.find_all("a", href=True)
    results = []

    for tag in job_cards:
        title = tag.text.strip()
        if "Data Engineer" in title:
            results.append({
                "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Company": company,
                "Job Title": title,
                "Link": "https://www.amazon.jobs" + tag["href"]
            })

    if results:
        df = pd.DataFrame(results)
        filename = f"job_updates_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
        df.to_csv(filename, index=False)
        print(f"✅ Found {len(results)} jobs and saved to {filename}")
    else:
        print("❌ No 'Data Engineer' jobs found on Amazon.")

except Exception as e:
    print(f"🔴 Error: {e}")
