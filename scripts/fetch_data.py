from pathlib import Path
import requests

# City of Vancouver Open Data API
URL = (
    "https://opendata.vancouver.ca/api/explore/v2.1/"
    "catalog/datasets/council-voting-records/exports/csv"
)

OUTPUT = Path("data/raw/council_voting_records.csv")

def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    response = requests.get(URL, timeout=120)
    response.raise_for_status()

    OUTPUT.write_bytes(response.content)

    print(f"Dataset downloaded to {OUTPUT}")

if __name__ == "__main__":
    main()