from bs4 import BeautifulSoup
import re

def _extract_applicant_fields(applicant_rows) -> dict[str, str|None]:
    """
    Parse applicant data from a list of HTML row strings (1-3 rows per applicant).
    Returns a dict with all fields, defaulting to None if not present.
    """
    
    entry = {
        "program": None,
        "university": None,
        "comments": None,
        "date_added": None,
        "url": None,
        "status": None,
        "date_decision": None,
        "term": None,
        "nationality": None,
        "gre": None,
        "gre_v": None,
        "degree": None,
        "gpa": None,
        "gre_aw": None
    }

    # Row 1: Program, University, Date Added, Status, Degree, URL
    soup1 = BeautifulSoup(applicant_rows[0], "html.parser")
    tr_tag = soup1.find("tr")
    tds = tr_tag.find_all("td", recursive=False)
    
    #/ University /#
    university_div = tds[0].find("div", class_="tw-font-medium tw-text-gray-900 tw-text-sm")
    if university_div:
        entry["university"] = university_div.get_text(strip=True)
        
    #/ Program & Degree /#
    prog_div = tds[1].find("div")
    if prog_div:
        spans = prog_div.find_all("span")
        if len(spans) >= 1:
            entry["program"] = spans[0].get_text(strip=True)
        if len(spans) >= 2:
            entry["degree"] = spans[1].get_text(strip=True)
            
    #/ Date Added /#
    entry["date_added"] = tds[2].get_text(strip=True) or None
    
    #/ Status & Acceptance/Rejection Date /#
    status_div = tds[3].find("div")
    if status_div:
        status_text = status_div.get_text(strip=True)
        if "Accepted" in status_text:
            entry["status"] = "Accepted"
            m = re.search(r"Accepted on ([\w\s\d]+)", status_text)
            if m:
                entry["date_decision"] = m.group(1)
        elif "Rejected" in status_text:
            entry["status"] = "Rejected"
            m = re.search(r"Rejected on ([\w\s\d]+)", status_text)
            if m:
                entry["date_decision"] = m.group(1)
        elif "Wait listed" in status_text:
            entry["status"] = "Wait listed"
            m = re.search(r"Wait listed on ([\w\s\d]+)", status_text)
            if m:
                entry["date_decision"] = m.group(1)
        elif "Interview" in status_text:
            entry["status"] = "Interview"
            m = re.search(r"Interview on ([\w\s\d]+)", status_text)
            if m:
                entry["date_decision"] = m.group(1)
        else:
            entry["status"] = status_text
            
    #/ URL link /#
    for a in tds[4].find_all("a"):
        if "/result/" in a['href']:
            entry["url"] = (
                "https://www.thegradcafe.com" + a['href']
                if a['href'].startswith("/")
                else a['href']
            )
            break

    # Row 2: Badges (term, nationality, GRE, GRE V, GPA, GRE AW)
    if len(applicant_rows) > 1:
        soup2 = BeautifulSoup(applicant_rows[1], "html.parser")
        badges = soup2.find_all("div", class_="tw-inline-flex")
        for badge in badges:
            text = badge.get_text(" ", strip=True)
            if re.search(r"(Fall|Spring|Summer)\s*\d{4}", text):
                entry["term"] = text
            elif text in ("American", "International"):
                entry["nationality"] = text
            elif text.startswith("GRE ") and "V" not in text and "AW" not in text:
                m = re.match(r"GRE (\d+)", text)
                if m:
                    entry["gre"] = m.group(1)
            elif text.startswith("GRE V"):
                m = re.match(r"GRE V (\d+)", text)
                if m:
                    entry["gre_v"] = m.group(1)
            elif text.startswith("GRE AW"):
                m = re.match(r"GRE AW ([\d\.]+)", text)
                if m:
                    entry["gre_aw"] = m.group(1)
            elif text.startswith("GPA"):
                m = re.match(r"GPA ([\d\.]+)", text)
                if m:
                    entry["gpa"] = m.group(1)

    # Row 3: Comments
    if len(applicant_rows) > 2:
        soup3 = BeautifulSoup(applicant_rows[2], "html.parser")
        p = soup3.find("p")
        if p:
            entry["comments"] = p.get_text(strip=True)

    return entry
