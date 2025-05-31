import urllib3
from bs4 import BeautifulSoup, Tag
import time
import json
import re
from pathlib import Path

def scrape_data(pages:int=500): # 20 entries per page, default 500 pages for min 10_000 applicant entries
    base_url = "https://www.thegradcafe.com/survey/?page={}"
    http = urllib3.PoolManager()
    raw_entries = []

    for curr_page in range(1, pages+1):
        url = base_url.format(curr_page)
        response = http.request("GET", url)
        soup = BeautifulSoup(response.data, "html.parser")
        
        applicant_datatable = soup.find("tbody")
        all_rows = applicant_datatable.find_all("tr", recursive=False)

        curr_applicant = []
        for i, row in enumerate(all_rows):
            if not row.get("class"):    
                if curr_applicant:
                    raw_entries.append([str(r) for r in curr_applicant])    
                curr_applicant = [row]
            else:
                curr_applicant.append(row)
                
        if curr_applicant:
            raw_entries.append([str(r) for r in curr_applicant])
    
    raw_entries_path = Path(__file__).parents[1] / "data" / "raw_data.json"
    with open(raw_entries_path, "w", encoding="utf-8") as f:
        json.dump(raw_entries, f, ensure_ascii=False, indent=2)
            
    print(f"Scraped and saved {len(raw_entries)} applicants.")

if __name__ == "__main__":
    scrape_data(pages=1)