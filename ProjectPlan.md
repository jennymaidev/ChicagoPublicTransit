# Project Plan: Analyzing Public Transit Impact on Chicago Property Values

---

## 1. Overview

The overall goal of this project is to quantitatively assess the influence of the Chicago Transit Authority (CTA) rail system on residential property values within Cook County, focusing on the City of Chicago. We will employ data curation and data lifecycle techniques to acquire, integrate, clean, and analyze three distinct public datasets.

The end product will be a robust, reproducible workflow and a final report detailing the statistical correlation found between proximity to CTA rail stations (L-stops) and recent residential sale prices. This project is motivated by providing data-driven insights to urban planners and real estate investors regarding transit-oriented development (TOD).

---

## 2. Research Question(s)

This project seeks to answer the following research questions:

* Is there a statistically significant correlation between the Euclidean distance (in meters) of a residential property from the nearest active CTA rail station and its raw sale price?
* How does the transit line color (e.g., Red Line vs. Brown Line) influence the average sale price of properties within a quarter mile of the station, compared to the regional median?
* How do Residense Property Class and Minimum distance to the CTA station influence the sale price? Is there a strong correlation?


---

## 3. Team

| Team Member | Role/Focus Area | Specific Responsibilities (Evidence in Git) |
| :--- | :--- | :--- |
| **Jenny Mai** | ETL Foundation & Data Acquisition | Set up GitHub repository and file structure. Programmatically acquire all three datasets. Design and implement the SQL database schema. Develop the PIN-Join and Distance Calculation script (Enrichment). Develop the final workflow for automation (Snakemake implementation). |
| **Shenhua Zhang** | Data Quality, Cleaning & Analysis | Conduct initial data profiling and quality assessment. Develop cleaning scripts (Python/Pandas) for missing values, outliers, and data type standardization. Execute statistical analysis and generate final visualizations for the report. Develop the Final README.md Report & Documentation. |


---

## 4. Datasets

We will use three complementary datasets, all sourced from the Cook County or City of Chicago public data portals.

| Dataset Name | Source/Access Method | Key Data Points & Role |
| :--- | :--- | :--- |
| **1. Assessor - Parcel Sales** | [Cook County Data Portal](https://datacatalog.cookcountyil.gov/Property-Taxation/Assessor-Parcel-Sales/wvhk-k5uv/) (Direct requests CSV Download) | Contains `pin`, `sale_price`, `sale_date`, and various quality flags (`is_multisale`, `deed_type` filters). This is the core dependent variable data. |
| **2. Assessor - Parcel Universe** | [Cook County Data Portal](https://datacatalog.cookcountyil.gov/Property-Taxation/Assessor-Parcel-Universe/nj4t-kc8j/) (Socrata API Query) | Contains `pin`, and the property's pre-calculated location: `lon` and `lat`. Essential for integration and geospatial analysis. |
| **3. CTA Rail Stations** | [City of Chicago Open Data](https://data.cityofchicago.org/Transportation/CTA-L-Rail-Stations/3tzw-cg4m/) (GeoJSON File Download) | Contains precise geospatial coordinates and line color metadata. Essential for the proximity calculation. |

### Integration Strategy (Geospatial Enrichment)
The primary integration strategy involves a series of relational joins and geospatial enrichment steps:

1.  **Integration (Relational Join):** Use the common **PIN** identifier to join the Parcel Sales data with the Parcel Universe data to associate sale price and date with the property's pre-calculated latitude and longitude.
2.  **Enrichment (Geospatial):** Calculate the Euclidean distance (in meters) between the coordinates of each property and the nearest CTA rail stop using the **`scipy.spatial.KDTree`** for highly optimized nearest-neighbor searching.
3.  **Final Integration:** The calculated minimum distance (in meters) and the lines of the nearest station will be added as new columns (enriched features) to the primary property sales table.

---

## 5. Timeline

| Milestone | Responsible Team Member(s) | Target Completion Date | Status | Artifacts & Evidence of Completion |
| :--- | :--- | :--- | :--- | :--- |
| **Phase 1: Planning & Setup** | | | | |
| Project Plan & GitHub Release | Both | October 7, 2025 | Completed | ProjectPlan.md, GitHub Tag: project-plan |
| **Phase 2: Acquisition & Storage** | | | | |
| Data Acquisition & Initial Storage (CSV/JSON) | Jenny Mai | October 13, 2025 | Completed | Scripts in src/acquire.py, Notebook: notebooks/1_data_acquisition_test.ipynb |
| SQLite Schema Design & Data Load | Jenny Mai | October 17, 2025 | Completed | Script: src/storage.py, Output: data/project_data.db (Ignored by Git) |
| **Phase 3: Integration & Cleaning** | | | | |
| PIN-Join & Distance Calculation Script (Enrichment) | Jenny Mai | October 23, 2025 | Completed | Script logic tested in notebooks/3_geospatial_enrichment.ipynb |
| Data Cleaning Scripts | Both | November 3, 2025 | Completed | Script: src/clean.py, Notebook: notebooks/4_data_filtering_cleaning.ipynb |
| **Phase 4: Reporting & Automation** | | | | |
| Interim Status Report Submission | Both | November 13, 2025 | Completed | This document (StatusReport.md) |
| Statistical Analysis & Visualization Script | Shenhua Zhang | November 17, 2025 | Completed | Initial correlation and premium calculation in notebooks/5_exploring_analysis.ipynb |
| Workflow Automation (Snakemake implementation) | Jenny Mai | December 5, 2025 | Completed | Snakefile |
| **Phase 5: Final Submission** | | | | |
| Final README.md Report of Findings & Documentation | Shenhua Zhang | December 7, 2025 | Completed | README.md (355 lines, ~3700 words), all figures integrated |
| Final Project Tag/Release & Box Upload | Both | December 7, 2025 | Completed | GitHub release tag: final-project, Box link: https://uofi.box.com/s/90qg970raf1p20hqmwn1cu4lccqmevte |

---

## 6. Constraints

* **Data Volume:** Chicago property data is large (millions of rows), requiring efficient Python/Pandas operations to manage processing time and memory.
* **API Rate Limits:** While bulk downloads are used, the necessity of querying the Parcel Universe API by individual PINs (even in batches) introduces a risk of rate limits or service timeouts, requiring built-in `sleep` and error handling.
* **Data Integration Complexity:** Joining the various Cook County datasets by PIN requires careful management of data types and zero-padding to ensure accurate matches across large files.
* **Coordinate Accuracy:** We rely on the coordinates pre-calculated by the Cook County Assessor's office.

---

## 7. Gaps

* **Price Normalization Variable:** We urgently need to find the appropriate Cook County dataset (likely Assessor - Residential Characteristics) that contains structural characteristics (like living square footage) to calculate an accurate Price per Square Foot for normalization.
* **Temporal Trends:** We must determine the correct method to normalize or account for changes in the Chicago housing market based on the `sale_date` (e.g., filtering for recent years and potentially using a regional price index).
