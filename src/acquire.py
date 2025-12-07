import requests
import os
import json

# Constants
RAW_DATA_DIR = '../data/raw/'

SALES_DATA_URL = 'https://datacatalog.cookcountyil.gov/resource/wvhk-k5uv.csv?$limit=3000000'
SALES_DATA_FILE = os.path.join(RAW_DATA_DIR, 'sales_data_raw.csv')

CTA_STATIONS_URL = 'https://data.cityofchicago.org/api/geospatial/8pix-ypme?method=export&format=geojson'
CTA_STATIONS_FILE = os.path.join(RAW_DATA_DIR, 'cta_l_stops.geojson')


def download_sales_data(url, filepath):
    """Downloads the large CSV sales dataset."""
    print(f"Downloading Cook County Sales data to {filepath}...")
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(filepath, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print("Sales data download complete.")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading sales data: {e}")

def download_cta_data(url, filepath):
    """Downloads the CTA stations GeoJSON file."""
    print(f"Downloading CTA Stations GeoJSON data to {filepath}...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        geojson_data = response.json()
        
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(geojson_data, file, indent=4)
        print("CTA data download complete.")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading CTA data: {e}")
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from CTA data response.")


def main():
    """Main function to ensure directory exists and run all downloads."""
    # os.makedirs(RAW_DATA_DIR, exist_ok=True)
    
    # # Download Dataset 1: Parcel Sales
    # download_sales_data(SALES_DATA_URL, SALES_DATA_FILE)
    
    # # Download Dataset 3: CTA Rail Stations
    # download_cta_data(CTA_STATIONS_URL, CTA_STATIONS_FILE)

    

if __name__ == '__main__':
    main()