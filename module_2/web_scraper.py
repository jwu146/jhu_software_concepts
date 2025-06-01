from pathlib import Path

from web_scraper.scrape import scrape_data
from web_scraper.clean import clean_data

def main(raw_data_path:Path, clean_data_path:Path) -> None:
    """Runs the full GradCafe scraping and cleaning pipeline.

    This function scrapes raw applicant data from GradCafe and saves it to the specified path,
    then processes and cleans the raw data into a structured format and saves the cleaned data.

    Args:
        raw_data_path: Path where the raw scraped applicant data will be saved (JSON).
        clean_data_path: Path where the cleaned/structured applicant data will be saved (JSON).

    Returns:
        None
    """
    scrape_data(raw_data_path)
    clean_data(clean_data_path, raw_data_path)
    return None

if __name__ == "__main__":
    raw_data_path = Path(__file__).parent / "data" / "raw_data.json"
    clean_data_path = Path(__file__).parent / "data" / "applicant_data.json"
    main(raw_data_path, clean_data_path)
