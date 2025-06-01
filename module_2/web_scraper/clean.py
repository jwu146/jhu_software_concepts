import json
from pathlib import Path
from utils import _extract_applicant_fields

def load_data(filepath:Path) -> list[list[str]]:
    """Loads raw applicant data from a JSON file."""
    with open(filepath, "r", encoding="utf-8") as f:
        raw_data = json.load(f)
    return raw_data

def save_data(cleaned_data:list[dict], savepath:Path) -> None:
    """Saves cleaned applicant data (list of dicts) to a JSON file."""
    with open(savepath, "w", encoding="utf-8") as f:
        json.dump(cleaned_data, f, indent=2, ensure_ascii=False)
        
def clean_data(savepath:Path, datapath:Path) -> None:
    """Cleans raw applicant data and saves the structured results."""
    raw_data = load_data(datapath)

    cleaned_data = []
    for applicant_data in raw_data:
        extracted_data = _extract_applicant_fields(applicant_data)
        cleaned_data.append(extracted_data) 
    save_data(cleaned_data, savepath)

if __name__ == "__main__":
    savepath = Path(__file__).parents[1] / "data" / "applicant_data.json"
    datapath = Path(__file__).parents[1] / "data" / "raw_data.json"
    clean_data(savepath, datapath)