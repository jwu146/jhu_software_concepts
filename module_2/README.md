# Module 2: Web Scraping (Due: 2025-06-01 23:59:00)
**Authored by:** Jonathan Wu *(jwu146)*

## Quick Start
This project uses **uv** for dependency management, but a `requirements.txt` file is also provided

### Using **uv**:

1. Install **uv** (see [uv documentation](https://docs.astral.sh/uv/getting-started/installation/) for installation instructions).  

2. To sync the project's dependencies with the environment, from the project root, run:
   ```bash
   uv sync
   ```

3. To run the project, from the project root, run:
    ```bash
    uv run web_scraper.py
    ```

-----

### Using **pip** and `requirements.txt`:

1. To sync the project's dependencies using `requirements.txt`, run:
    ```bash
    pip install -r requirements.txt
    ```

2. To run the project, from the project root, run:
    ```bash
    python web_scraper.py
    ```

-----

The save location for `applicant_data.json` file is in `/data`.


## robots.txt Compliance

This project strictly adheres to GradCafe’s `robots.txt` policy. As a generic user-agent, none of the disallowed paths (`/cgi-bin/` and `/index-ad-test.php`) are accessed at any point in the code. The only URLs accessed by the scraper are of the form:

```
https://www.thegradcafe.com/survey/?page={page_number}
```

where `page_number` is incremented for pagination.

A screenshot of the `robots.txt` file from GradCafe is included in the project’s root directory as reference.

-----



## Approach

The goal of this project is to programmatically scrape graduate applicant results from The GradCafe website. This includes parsing and cleaning the raw HTML data into a structured JSON format for future use. 

### **Scraping Process**

1. **URL and Pagination:**
   The script constructs URLs for each results page (e.g., `https://www.thegradcafe.com/survey/?page=1`, etc.) and iterates through a specified number of pages, with a default of 750 pages to surpass the minimum of 10,000 applicants (20 applicants per page).

2. **Downloading HTML:**
   For each page, the script uses `urllib3.PoolManager` to make GET requests and downloads the HTML. The results table with applicant data is located by finding the `<tbody>` element on the page.

3. **Grouping Rows by Applicant:**
   The following patterns were noticed on how applicant data is organized on the website:
   
   Each applicant’s data can span 1 to 3 table rows:

   * The start of a new applicant is indicated by a `<tr>` with **no class attribute**.
   * Additional details (such as badges or comments) are in subsequent `<tr>`s with a `class` attribute.
   * Ad placement and placeholder rows are identified by the presence of a `<div>` with an id starting with `"results-ad-placement"` or a single, empty `<td>`, and are skipped.

   The scraper collects each applicant as a **list of HTML strings** (one for each of their rows), resulting in a master data structure that is a list of applicants, where each applicant is itself a list of strings.

4. **Saving Raw Data:**
   After scraping, all raw applicant data is saved to `data/raw_data.json` as a JSON array. This preserves all scraped HTML for reproducibility and later cleaning, and avoids repeated requests to the website.

---

### **Cleaning Process**

1. **Loading and Iterating Over Raw Data:**
   The cleaning script loads the JSON array, which consists of lists of HTML rows (as strings) for each applicant.

2. **Parsing with BeautifulSoup:**
   Each row string is parsed with BeautifulSoup. The script extracts information by the following general observed pattern:

   * The first row (always present) provides **university, program, degree type, date added, status, and URL**.
   * The second row (if present) contains badges for **semester/year, nationality, GRE, GPA, etc.**
   * The third row (if present) contains the **comments** field.

3. **Regex and String Methods:**
   Regular expressions are used to extract structured values (e.g., GRE score, GPA, decision date) from badge text and status messages.

4. **Default Values and Field Consistency:**
   Each applicant is converted to a dictionary with all expected fields; missing values are filled with `None` for consistency.

5. **Saving Cleaned Data:**
   The cleaned, structured data is saved as `data/applicant_data.json`, with each entry as a dictionary suitable for databases.

---