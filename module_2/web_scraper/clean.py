import json
import re
from bs4 import BeautifulSoup
from utils import *

def load_data(filepath="raw_data.json"):
    with open(filepath, "r", encoding="utf-8") as f:
        raw_entries = json.load(f)
    return raw_entries

def clean_data(raw_entries):
    cleaned = []
    for row_html in raw_entries:
        soup = BeautifulSoup(row_html, "html.parser")
        # Extract and clean each required field
        program_name = _extract_program_name(soup)
        # Repeat for each field...
        entry = {
            "program_name": program_name,
            # ...
        }
        cleaned.append(entry)
    return cleaned

def _extract_program_name(soup):
    # Example: use bs4/string/regex to get the text you need
    # return soup.select_one("td.program_name_selector").get_text(strip=True)
    pass

def save_data(cleaned, filepath="applicant_data.json"):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    raw_entries = load_data()
    cleaned_entries = clean_data(raw_entries)
    save_data(cleaned_entries)