# Workflow Documentation

## ETL Pipeline Overview
1. **Acquisition** (notebook 01): Downloads sales, universe, CTA data
2. **Geocoding** (notebook 02): Loads universe PIN locations
3. **Enrichment** (notebook 03): Calculates distance to nearest CTA station
4. **Cleaning** (notebook 04): Filters to single-family homes, 2018-2024
5. **Analysis** (notebook 05): Statistical analysis and visualizations

## Data Flow
sales_data_raw.csv + universe_pin.csv → [PIN join] → [distance calc] → sales_data_enriched.csv → [filtering] → final_cleaned_data.csv