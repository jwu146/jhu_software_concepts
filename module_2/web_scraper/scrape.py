import urllib3
from bs4 import BeautifulSoup
import json
import re
from pathlib import Path

def _save_scraped_data(raw_data:list[list[str]], savepath:Path) -> None:
    """Saves scraped raw applicant HTML data to a JSON file.

    Args:
        raw_data: List of applicants, scraped from `_scrape_data`.
        savepath: Path to save the output JSON file.
    """
    with open(savepath, "w", encoding="utf-8") as f:
        json.dump(raw_data, f, ensure_ascii=False, indent=2)

def _scrape_data(pages:int=750) -> list[list[str]]:
    """Scrapes applicant data from The GradCafe admissions results pages.

    For each page, this function finds the applicant table and groups rows into applicants:
      - The start of a new applicant is indicated by a <tr> with no class attribute.
      - Additional detail rows for the same applicant (such as comments or badges) follow as <tr> tags with a class.
      - Ad placement rows and empty placeholder rows are identified and skipped.

    Each applicant is stored as a list of HTML strings (one for each row belonging to that applicant).

    Args:
        pages: Number of result pages to scrape (default 750).

    Returns:
        List of applicants, each being a list of row HTML strings.
    """
    base_url = "https://www.thegradcafe.com/survey/?page={}"
    http = urllib3.PoolManager()
    raw_data = []

    for curr_page in range(1, pages+1):
        url = base_url.format(curr_page)
        response = http.request("GET", url)
        soup = BeautifulSoup(response.data, "html.parser")
        
        applicant_datatable = soup.find("tbody")
        all_rows = applicant_datatable.find_all("tr", recursive=False)

        curr_applicant = []
        for row in all_rows:
            # Check for ad placement row within applicant
            ad_div = row.find("div", id=re.compile(r"^results-ad-placement"))
            if ad_div:
                continue
            
            # Skip ad placeholder rows
            tds = row.find_all("td", recursive=False)
            if len(tds) == 1 and not tds[0].get_text(strip=True):
                continue
            
            # Parsing applicant data
            if not row.get("class"):    
                if curr_applicant:
                    raw_data.append([str(r) for r in curr_applicant])    
                curr_applicant = [row]
            else:
                curr_applicant.append(row)
        
        if curr_applicant:
            raw_data.append([str(r) for r in curr_applicant])
    return raw_data

def scrape_data(savepath:Path, pages:int=750) -> None:
    """Orchestrates scraping and saving of applicant data.

    Args:
        savepath: Path to save the output JSON file.
        pages: Number of result pages to scrape. Default is 750.
    """
    raw_data = _scrape_data(pages)
    _save_scraped_data(raw_data, savepath)
    
    print(f"Scraped and saved {len(raw_data)} applicants.")
    
if __name__ == "__main__":
    savepath = Path(__file__).parents[1] / "data" / "raw_data.json"
    scrape_data(savepath, pages=5)