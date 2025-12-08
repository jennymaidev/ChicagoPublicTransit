# Data Dictionary

## Overview
This document describes all datasets used in the project: "Analyzing Public Transit Impact on Chicago Property Values." The data flows through three stages: **raw** (source data), **interim** (processed/enriched), and **processed** (final analysis-ready dataset).

---

## Raw Data (`data/raw/`)

### 1. `sales_data_raw.csv`
**Source**: Cook County Assessor - Parcel Sales  
**Description**: Complete residential property sales records from Cook County

| Column | Data Type | Description | Example | Notes |
|--------|-----------|-------------|---------|-------|
| `pin` | String | 14-digit Property Index Number (unique identifier) | `2012000831` | Zero-padded; primary key for joining |
| `sale_price` | Float | Sale price in USD | `285000.00` | Numeric; negative values indicate data quality issues |
| `sale_date` | String | Date of sale (YYYY-MM-DD format) | `2023-06-15` | ISO 8601 format |
| `year` | Integer | Year of sale | `2023` | Derived from sale_date |
| `is_multisale` | Boolean | Flag indicating if property sold multiple times in same year | `0` or `1` | 1 = multisale (excluded in cleaning) |
| `deed_type` | String | Type of deed transaction | `WARRANTY DEED`, `QUIT CLAIM` | Used for filtering non-market transactions |
| `latitude` | Float | Property latitude coordinate | `41.8781` | Added during enrichment |
| `longitude` | Float | Property longitude coordinate | `-87.6298` | Added during enrichment |
| `class` | Integer | Property class code (residential only) | `202`, `203`, `204` | See Property Class Definitions below |

**Record Count**: ~2,600,000
**Coverage**: Cook County, Illinois (includes Chicago and suburbs)  
**Time Period**: 2000-2025  
**Missing Values**: <1% (varies by field)

---

### 2. `cta_l_stops.geojson`
**Source**: City of Chicago Open Data - CTA 'L' Rail Stations  
**Description**: Geographic coordinates and metadata for all 145 CTA rail stations

| Column | Data Type | Description | Example | Notes |
|--------|-----------|-------------|---------|-------|
| `station_id` | Integer | Unique station identifier | `40010` | Primary key |
| `longname` | String | Full station name | `Clark/Lake` | Human-readable name |
| `lines` | String | CTA lines serving station (comma-separated) | `Red Line, Blue Line` | Multiple lines possible |
| `point_x` | Float | X-coordinate (longitude, WGS84) | `-87.6298` | For spatial calculations |
| `point_y` | Float | Y-coordinate (latitude, WGS84) | `41.8857` | For spatial calculations |
| `address` | String | Street address | `504 N State St` | Physical location |
| `ada` | Boolean | ADA accessible | `True` or `False` | Americans with Disabilities Act compliance |
| `pknrd` | Boolean | Park and Ride available | `True` or `False` | Parking facilities |

**Record Count**: 145 stations  
**Coverage**: City of Chicago (and O'Hare/Midway airports)  
**Update Frequency**: Quarterly (as of Aug 2024)  
**Missing Values**: 0%

---

## Interim Data (`data/interim/`)

### 3. `universe_pin.csv`
**Source**: Cook County Assessor - Parcel Universe (filtered)  
**Description**: All residential parcels with geographic coordinates

| Column | Data Type | Description | Example | Notes |
|--------|-----------|-------------|---------|-------|
| `pin` | String | 14-digit Property Index Number | `2012000831` | Primary key; joins with sales_data |
| `latitude` | Float | Parcel latitude (WGS84) | `41.8781` | From Cook County assessor geocoding |
| `longitude` | Float | Parcel longitude (WGS84) | `-87.6298` | From Cook County assessor geocoding |

**Record Count**: ~500,000 unique pins
**Coverage**: Cook County (all property types, pre-filtered to residential)  
**Missing Values**: 0% (coordinates validated by assessor)

---

### 4. `sales_data_enriched.csv`
**Source**: sales_data_raw.csv + universe_pin.csv (via PIN join)  
**Description**: Sales data joined with property coordinates; geospatial enrichment added

| Column | Data Type | Description | Example | Notes |
|--------|-----------|-------------|---------|-------|
| `pin` | String | 14-digit Property Index Number | `2012000831` | Primary key |
| `sale_price` | Float | Sale price in USD | `285000.00` | Raw price before cleaning |
| `sale_date` | String | Sale date (YYYY-MM-DD) | `2023-06-15` | ISO 8601 |
| `year` | Integer | Sale year | `2023` | Extracted from sale_date |
| `latitude` | Float | Property latitude | `41.8781` | From parcel universe |
| `longitude` | Float | Property longitude | `-87.6298` | From parcel universe |
| `min_distance_meters` | Float | Distance to nearest CTA station in meters | `487.5` | **Calculated via KDTree** (see Enrichment) |
| `nearest_cta_station` | String | Name of nearest CTA station | `Clark/Lake` | Identified during enrichment |
| `nearest_cta_lines` | String | CTA lines at nearest station | `Red Line, Blue Line` | Comma-separated; multiple possible |
| `class` | Integer | Property class code | `202` | Residential only |
| `is_multisale` | Boolean | Multisale flag | `0` or `1` | |
| `deed_type` | String | Deed type | `WARRANTY DEED` | |

**Record Count**: 1,785,902 (enriched sales with valid coordinates)
**Key Transformation**: Geospatial enrichment using scipy.spatial.KDTree for nearest-neighbor distance calculation
**Missing Values**: Minimal (properties without valid coordinates removed prior to enrichment)

---

### 5. `pins_to_check.txt`
**Source**: Data Quality Check  
**Description**: List of PIN numbers flagged during quality assessment for manual review

**Format**: One PIN per line (no header)  
**Example**:
```
2012000831
9352170080
3293400010
```

**Purpose**: Tracking properties with potential data quality issues for investigation  
**Record Count**: 0

---

## Processed Data (`data/processed/`)

### 6. `final_cleaned_data.csv` **PRIMARY ANALYSIS DATASET**
**Source**: sales_data_enriched.csv (cleaned and filtered)  
**Description**: Final dataset ready for statistical analysis; single-family residential properties

| Column | Data Type | Description | Valid Range | Missing % |
|--------|-----------|-------------|-------------|-----------|
| `pin` | String | 14-digit Property Index Number | [0-9]{14} | 0% |
| `year` | Integer | Sale year | 2018-2024 | 0% |
| `sale_price` | Float | Sale price in USD | $25,000 - $1,550,000 | <1% |
| `latitude` | Float | Property latitude (WGS84) | 41.5 - 42.2 | 0% |
| `longitude` | Float | Property longitude (WGS84) | -88.2 - -87.4 | 0% |
| `min_distance_meters` | Float | Distance to nearest CTA station (meters) | 30 - 34,227 | 0% |
| `nearest_cta_station` | String | Name of nearest CTA station | Valid station names | <1% |
| `nearest_cta_lines` | String | CTA lines at nearest station | Line colors (Red, Blue, etc.) | <1% |
| `class` | Integer | Property class code | 202, 203, 204, 205, 206, 207, 208, 209 | 0% |
| `is_multisale` | Boolean | Multisale flag | 0 | 0% (filtered out) |
| `deed_type` | String | Deed type | WARRANTY DEED | 0% (non-market excluded) |

**Record Count**: 124,438 properties
**Time Period**: 2018-2024 (7 years)
**Geographic Coverage**: Cook County (includes Chicago and suburbs)  
**Data Quality**: High (outliers removed, missing values <1%)

---

## Property Class Definitions
*(Cook County Assessor Residential Classifications)*

| Class Code | Description |
|------------|-------------|
| 202 | 1-story residence, any age, up to 999 sq ft |
| 203 | 1-story residence, any age, 1,000-1,800 sq ft |
| 204 | 1-story residence, any age, 1,801+ sq ft |
| 205 | 2+ story residence, 62+ years old, up to 2,200 sq ft |
| 206 | 2+ story residence, 62+ years old, 2,201-4,999 sq ft |
| 207 | 2+ story residence, <62 years old, up to 2,000 sq ft |
| 208 | 2+ story residence, <62 years old, 2,001-4,999 sq ft |
| 209 | 2+ story residence, any age, 5,000+ sq ft |

---

## Data Quality Assessment Summary

| Aspect | Assessment | Details |
|--------|------------|---------|
| **Completeness** | High | 98%+ of required fields populated in final dataset |
| **Validity** | High | Coordinates validated; prices reasonable; dates valid |
| **Consistency** | High | PIN format consistent; data types standardized |
| **Accuracy** | Medium-High | Source data from official government assessor; minor outliers removed |
| **Timeliness** | Current | Sales data updated monthly; CTA data updated quarterly (Aug 2024) |

### Cleaning Actions Performed
- Removed multisale transactions (same property, same year)
- Excluded non-market deeds (foreclosures, gifts, quit claims)
- Filtered to single-family residential classes only (202-209)
- Removed properties with sale price less than $50,000 or more than $2,000,000 (outliers)
- Excluded properties with missing geographic coordinates
- Filtered to sales years 2018-2024 (recent, stable market period)

---

## Data Integration Notes

### Join Strategy
1. **Sales + Universe**: PIN-to-PIN join (left join on sales_data)
   - Source: `sales_data_raw.csv` ← `universe_pin.csv`
   - Result: Geographic coordinates added to sales records

2. **Distance Calculation**: KDTree nearest-neighbor search
   - For each property coordinate, find nearest CTA station (145 total)
   - Calculate Euclidean distance in meters (projected to UTM)
   - Add `min_distance_meters` and `nearest_cta_station` columns

3. **Final Filtering**: Single-family residential, 2018-2024
   - Apply property class filter
   - Apply temporal filter
   - Remove outliers and missing values

### Data Lineage
```
sales_data_raw.csv (raw)
    ↓ [PIN join]
    + universe_pin.csv (raw)
    ↓ [Geospatial enrichment via KDTree]
    + cta_l_stops.geojson (raw)
    ↓ [Cleaning & filtering]
    final_cleaned_data.csv (processed) ← ANALYSIS DATASET
```

---

## Access & Attribution

**Data Sources**:
- Cook County Assessor: Public Domain
- City of Chicago: CC-BY-4.0 (attribution required)

**How to Cite**:
```
Mai, J., & Zhang, S. (2025). Final cleaned dataset: Chicago Transit Impact on Property Values.
University of Illinois IS 477 Course Project.
Retrieved from https://uofi.box.com/s/90qg970raf1p20hqmwn1cu4lccqmevte.
```

---

## Questions or Data Issues?

- **For raw data questions**: See original dataset documentation
  - Cook County: https://datacatalog.cookcountyil.gov/
  - City of Chicago: https://data.cityofchicago.org/
  
- **For processing methodology**: See Jupyter notebooks in `notebooks/` folder
  
- **For this dictionary**: Contact Jenny Mai or Shenhua Zhang