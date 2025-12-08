# src/storage.py

import pandas as pd
import sqlite3
import os

# Configuration
RAW_DATA_DIR = './data/raw/'
INTERIM_DATA_DIR = './data/interim/'
DB_PATH = './data/project_data.db'

FILES_TO_LOAD = {
    'sales_data_raw.csv': {'directory': RAW_DATA_DIR, 'table': 'raw_sales'},
    'cta_l_stops.geojson': {'directory': RAW_DATA_DIR, 'table': 'raw_cta'},
    'universe_pin.txt': {'directory': INTERIM_DATA_DIR, 'table': 'raw_universe'} # Now points to interim
}

def load_data_to_sqlite():
    """Loads raw data files (CSV, GeoJSON/txt) into a SQLite database."""
    db_dir = os.path.dirname(DB_PATH)
    if db_dir and not os.path.exists(db_dir):
        print(f"Creating directory: {db_dir}")
        os.makedirs(db_dir, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    print(f"Connected to database at {DB_PATH}")

    for filename, config in FILES_TO_LOAD.items():
        filepath = os.path.join(config['directory'], filename)
        table_name = config['table']

        if not os.path.exists(filepath):
            print(f"File not found: {filepath}")
            continue

        if filename.endswith('.geojson'):
            try:
                import geopandas as gpd
                df = gpd.read_file(filepath).drop(columns=['geometry'])
            except ImportError:
                 print(f"Cannot load {filename}. Geopandas not available.")
                 continue
        else:
            try:
                df = pd.read_csv(filepath)
            except Exception as e:
                print(f"Error reading {filepath}: {e}")
                continue

        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"Loaded {df.shape[0]} rows into table '{table_name}'.")

    conn.close()
    print("Database connection closed.")

if __name__ == '__main__':
    load_data_to_sqlite()