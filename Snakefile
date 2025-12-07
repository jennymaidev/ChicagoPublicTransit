# Snakefile for IS 477 Project: CTA Impact Analysis
# Workflow runs notebooks 01-05 sequentially.

# Configuration paths (relative to the Snakefile location)
DATA_RAW = "data/raw"
DATA_INTERIM = "data/interim"
DATA_PROCESSED = "data/processed"

# The final target: the cleaned data and the executed analysis notebook
rule all:
    input:
        f"{DATA_PROCESSED}/final_cleaned_data.csv",
        "notebooks/05_exploring_analysis_executed.ipynb"

# --- R01: Acquisition ---
# Output: raw sales data (Note: CTA data is also downloaded here implicitly,
# but we only track the main data dependency)
rule acquire_sales:
    output:
        sales = f"{DATA_RAW}/sales_data.csv"
    notebook:
        "notebooks/01_data_acquisition.ipynb"

# --- R02: Geocoding/PIN Location Lookup ---
# Output: PIN locations (universe_pin.csv is the likely file used by R03)
rule geocoding_pins:
    input:
        sales = f"{DATA_RAW}/sales_data.csv",
        cta = f"{DATA_RAW}/cta_l_stops.geojson" # Assumes CTA GeoJSON is ready or downloaded in R01/R02
    output:
        pins = f"{DATA_INTERIM}/universe_pin.csv" # Notebook 03 explicitly reads this file
    notebook:
        "notebooks/02_pin_location_geocoding.ipynb"

# --- R03: Geospatial Enrichment ---
# Output: sales data merged with lon/lat and nearest CTA distance/lines
rule enrichment:
    input:
        sales = f"{DATA_RAW}/sales_data.csv",
        cta = f"{DATA_RAW}/cta_l_stops.geojson",
        pins = f"{DATA_INTERIM}/universe_pin.csv"
    output:
        f"{DATA_INTERIM}/sales_data_enriched.csv"
    notebook:
        "notebooks/03_geospatial_enrichment.ipynb"

# --- R04: Filtering & Cleaning ---
# Output: Final cleaned data, ready for statistical analysis
rule cleaning:
    input:
        f"{DATA_INTERIM}/sales_data_enriched.csv"
    output:
        f"{DATA_PROCESSED}/final_cleaned_data.csv"
    notebook:
        "notebooks/04_data_filtering_cleaning.ipynb"

# --- R05: Analysis & Visualization ---
# Output: An executed copy of the analysis notebook
rule analysis:
    input:
        f"{DATA_PROCESSED}/final_cleaned_data.csv"
    output:
        "notebooks/05_exploring_analysis_executed.ipynb"
    notebook:
        "notebooks/05_exploring_analysis.ipynb"