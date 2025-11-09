"""
Data Engineer Job Tracker
Scrapes job pages for Data Engineer positions in India
and saves results to a timestamped CSV file.
"""

import os
import sys
from datetime import datetime
from typing import List, Dict

import requests
from bs4 import BeautifulSoup
import pandas as pd


class JobTracker:
    """Tracks job postings from Amazon's career site."""
    
    def __init__(self, company: str, job_url: str, search_keyword: str):
        """
        Initialize the job tracker.
        
        Args:
            company: Company name
            job_url: URL to scrape
            search_keyword: Keyword to search for in job titles
        """
        self.company = company
        self.job_url = job_url
        self.search_keyword = search_keyword
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        self.results: List[Dict[str, str]] = []
    
    def fetch_jobs(self) -> bool:
        """
        Fetch and parse job listings from the URL.
        
        Returns:
            True if fetch was successful, False otherwise
        """
        print(f"🔍 Checking {self.company} job site...")
        
        try:
            response = requests.get(
                self.job_url, 
                headers=self.headers, 
                timeout=20
            )
            response.raise_for_status()
            
            self._parse_jobs(response.text)
            return True
            
        except requests.exceptions.HTTPError as e:
            print(f"⚠️ HTTP Error: {e.response.status_code} - {e}")
            return False
        except requests.exceptions.Timeout:
            print(f"⚠️ Request timed out after 20 seconds")
            return False
        except requests.exceptions.RequestException as e:
            print(f"🔴 Request Error: {e}")
            return False
        except Exception as e:
            print(f"🔴 Unexpected Error: {type(e).__name__}: {e}")
            return False
    
    def _parse_jobs(self, html_content: str) -> None:
        """
        Parse HTML content and extract job listings.
        
        Args:
            html_content: Raw HTML content from the response
        """
        soup = BeautifulSoup(html_content, "html.parser")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # Search for job titles in common HTML elements
        tags = soup.find_all(["a", "h3", "span", "div"], string=lambda text: text and self.search_keyword in text)
        
        for tag in tags:
            title = tag.get_text(strip=True)
            
            # Get the job link if available
            link = self.job_url
            if tag.name == "a" and tag.get("href"):
                link = tag.get("href")
                if not link.startswith("http"):
                    link = f"https://www.amazon.jobs{link}"
            
            self.results.append({
                "Date": timestamp,
                "Company": self.company,
                "Job Title": title,
                "Link": link
            })
        
        print(f"� Found {len(self.results)} matching job(s)")
    
    def save_to_csv(self) -> str:
        """
        Save results to a timestamped CSV file.
        
        Returns:
            Filename of the saved CSV
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        filename = f"job_updates_{timestamp}.csv"
        
        # Create DataFrame and save
        df = pd.DataFrame(self.results)
        df.to_csv(filename, index=False, encoding="utf-8-sig")
        
        # Verify file creation
        file_exists = os.path.exists(filename)
        file_size = os.path.getsize(filename) if file_exists else 0
        
        print(f"✅ Saved {len(self.results)} job(s) to: {filename}")
        print(f"📁 File exists: {file_exists} | Size: {file_size} bytes | Path: {os.getcwd()}")
        
        return filename


def main():
    """Main execution function."""
    # Configuration
    COMPANY = "Amazon"
    JOB_URL = "https://www.amazon.jobs/content/en/job-categories/software-development?keyword%5B%5D=Data+Engineer&country%5B%5D=IN"
    SEARCH_KEYWORD = "Data Engineer"
    
    # Create tracker and run
    tracker = JobTracker(COMPANY, JOB_URL, SEARCH_KEYWORD)
    
    # Fetch jobs
    success = tracker.fetch_jobs()
    
    # Always save CSV (even if empty or failed)
    filename = tracker.save_to_csv()
    
    # Exit with appropriate status code
    if not success and len(tracker.results) == 0:
        print("⚠️ Warning: Job fetch failed and no results found")
        sys.exit(1)
    
    print("🎉 Job tracker completed successfully!")
    sys.exit(0)


if __name__ == "__main__":
    main()
