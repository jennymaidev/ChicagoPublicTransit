# Project Metadata

## Project Information

| Field | Value |
|-------|-------|
| **Title** | Analyzing Public Transit Impact on Chicago Property Values |
| **Creators** | Jenny Mai & Shenhua Zhang |
| **Date Published** | December 7, 2025 |
| **Description** | Quantitative analysis of the correlation between proximity to Chicago Transit Authority (CTA) rail stations and residential property sale prices in Cook County, Chicago. Integration of three public datasets using geospatial enrichment and statistical modeling. |
| **Subject Keywords** | Public Transit, Real Estate, Urban Planning, Geospatial Analysis, Chicago, CTA, Transit-Oriented Development (TOD) |
| **License** | CC-BY-4.0 (code); Public Domain / CC-BY-4.0 (data) |
| **Funding** | University of Illinois Urbana-Champaign, IS 477 Data Management, Curation & Reproducibility Course |
| **Version** | 1.0 |
| **Repository** | https://github.com/jennymaidev/ChicagoPublicTransit |
| **Data Storage (Box)** | https://uofi.box.com/s/90qg970raf1p20hqmwn1cu4lccqmevte |
| **Project Duration** | September 26, 2025 - December 7, 2025 |

## Datasets Used

### Dataset 1: Cook County Assessor - Parcel Sales
| Attribute | Value |
|-----------|-------|
| **Title** | Assessor - Parcel Sales |
| **Creator** | Cook County Assessor's Office |
| **Date Published** | April 18, 2022 (Last updated: December 3, 2025) |
| **Access URL** | https://datacatalog.cookcountyil.gov/Property-Taxation/Assessor-Parcel-Sales/wvhk-k5uv/ |
| **Format** | CSV (via Socrata API) |
| **Records** | ~2,620,000 records |
| **Key Variables** | pin, sale_price, sale_date, deed_type, is_multisale |
| **License** | Public Domain |
| **Citation** | Cook County Assessor's Office. (2025). Assessor - Parcel Sales. Retrieved from https://datacatalog.cookcountyil.gov/ |

### Dataset 2: Cook County Assessor - Parcel Universe
| Attribute | Value |
|-----------|-------|
| **Title** | Assessor - Parcel Universe |
| **Creator** | Cook County Assessor's Office |
| **Date Published** | May 1, 2023 (Last updated: December 2, 2025) |
| **Access URL** | https://datacatalog.cookcountyil.gov/Property-Taxation/Assessor-Parcel-Universe/nj4t-kc8j/ |
| **Format** | CSV (via Socrata API) |
| **Records** | ~48,800,000 parcels |
| **Key Variables** | pin, longitude, latitude, property class |
| **License** | Public Domain |
| **Citation** | Cook County Assessor's Office. (2025). Assessor - Parcel Universe. Retrieved from https://datacatalog.cookcountyil.gov/ |

### Dataset 3: CTA - 'L' (Rail) Stations
| Attribute | Value |
|-----------|-------|
| **Title** | CTA - 'L' (Rail) Stations |
| **Creator** | Chicago Transit Authority |
| **Date Published** | August 9, 2024 (Last updated: August 16, 2024) |
| **Access URL** | https://data.cityofchicago.org/Transportation/CTA-L-Rail-Stations/3tzw-cg4m/ |
| **Format** | GeoJSON / CSV |
| **Records** | 145 stations |
| **Key Variables** | station_id, longname, lines, point_x, point_y, ada, address |
| **License** | CC-BY-4.0 (City of Chicago Open Data) |
| **Citation** | Chicago Transit Authority. (2024). CTA - 'L' (Rail) Stations. City of Chicago Open Data Portal. Retrieved from https://data.cityofchicago.org/Transportation/CTA-L-Rail-Stations/3tzw-cg4m/ |

## Data Availability & Preservation

| Aspect | Details |
|--------|---------|
| **Raw Data Location** | https://uofi.box.com/s/90qg970raf1p20hqmwn1cu4lccqmevte |
| **Processed Data Location** | https://uofi.box.com/s/90qg970raf1p20hqmwn1cu4lccqmevte |
| **Code Repository** | https://github.com/jennymaidev/ChicagoPublicTransit |
| **Final Dataset** | `data/processed/final_cleaned_data.csv` |
| **Box Access Instructions** | Download from Box; extract to `data/raw/`, `data/interim/`, `data/processed/` folders |

## Data Processing Workflow

1. **Data Acquisition** (Notebook 01): Download three source datasets
2. **Geocoding** (Notebook 02): Load and validate PIN locations
3. **Geospatial Enrichment** (Notebook 03): Calculate distance to nearest CTA station
4. **Data Cleaning** (Notebook 04): Filter to single-family homes (2018-2024), remove outliers
5. **Analysis** (Notebook 05): Statistical analysis and visualizations

## Data Quality & Completeness

| Dataset | Records | Missing Values | Quality Issues |
|---------|---------|---|---|
| Sales Data (raw) | ~2,600,000 | 0% | Includes multi-sales, non-market transactions |
| Parcel Pins | ~900,000 | 42% | Pin values validated by assessor |
| CTA Stations | 145 | 0% | Updated regularly by CTA |
| Final Dataset | 122,544 | <2% | Filtered: single-family, 2018-2024, valid coordinates |

## Reproducibility Information

- **Python Version**: 3.9+
- **Key Dependencies**: pandas, geopandas, scipy, statsmodels, matplotlib, seaborn
- **Compute Requirements**: ~16 GB RAM, ~375 hours runtime
- **Documentation**: See `README.md` for full reproducibility instructions
- **Code Location**: `src/` and `notebooks/` folders

## Contact & Attribution

- **Course**: IS 477 Data Management, Curation, and Reproducibility, University of Illinois Urbana-Champaign
- **Instructor**: Prof. Bertram Ludäscher
- **Project Contributors**: 
  - Jenny Mai (ETL, Acquisition, Cleaning, Automation)
  - Shenhua Zhang (Analysis, Visualization, Reporting)