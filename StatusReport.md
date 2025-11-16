# Status Report (Milestone 3)

**Project Title:** Analyzing Public Transit Impact on Chicago Property Values

**Team Members:** Jenny Mai & Shenhua Zhang

**Date:** November 13, 2025

---

## 1. Executive Summary of Progress (Milestone 2 to 3)

Since the submission of the Project Plan (Milestone 1), the team has made significant strides in building the data infrastructure required to analyze the relationship between public transit and property values in Cook County. We have successfully moved from the planning phase into full execution, completing the core Data Acquisition, Storage, Integration, and Cleaning phases of the data lifecycle.

The primary achievement of this milestone was the successful development of a reproducible ETL (Extract, Transform, Load) pipeline. We addressed the challenge of managing large-volume public data (millions of property records) by implementing a SQLite-based storage strategy and developing optimized Python scripts for geospatial enrichment. Specifically, we utilized KDTree algorithms to efficiently calculate the distance between over 2.6 million properties and 145 CTA rail stations.

Furthermore, we have finalized the analytical dataset. By applying strict data quality filters, isolating single-family homes and removing non-market transactions, we have produced a clean, homogeneous dataset (final_cleaned_data.csv) that allows us to answer our revised research questions with statistical validity. Our initial exploratory analysis has already yielded preliminary correlation metrics, confirming that the data is ready for the final modeling phase.

---

## 2. Changes to Project Plan and Scope

In response to data accessibility challenges and a re-evaluation of project complexity during Milestone 2, we have made a strategic adjustment to the project scope.

### 2.1. Removal of the "Characteristics" Dataset

Originally, our plan included acquiring a fourth dataset ("Assessor - Residential Characteristics") to obtain the square footage of every property. This was intended to create a "Price Per Square Foot" normalization variable. However, integrating this massive, complex dataset introduced significant risks regarding data sparsity and join integrity.

Decision: We eliminated the need for this fourth dataset. Impact: Instead of a multivariate model normalizing by size, we shifted to a "Strict Filtering" approach. We now filter the dataset to include only "Class 202-209" (One-Story and Two-Story Single Family Homes). By isolating a homogeneous housing type, we can use the Raw Sale Price as a valid dependent variable, significantly simplifying the ETL pipeline while maintaining statistical rigor.

We also expanded our scope of the project from covering only Chicago to covering all of Cook County.

### 2.2. Revision of Research Questions

Consequently, our research questions (RQs) were updated to reflect this change:

**RQ 1**: Focuses on the correlation between distance and raw sale price (rather than adjusted price).

**RQ 3**: Focuses specifically on the median price premium for detached single-family homes, rather than a generalized premium for all property types.

---

## 3. Technical Implementation & Artifacts

We have completed the following technical tasks, evidenced by artifacts currently in the GitHub repository.

### 3.1. Data Acquisition and Storage

We implemented a programmatic acquisition strategy using Python.

**Acquisition**: The script src/acquire.py (prototyped in notebooks/1_data_acquisition.ipynb) successfully downloads the Cook County Sales Data (CSV), Parcel Universe locations (API), and CTA Station data (GeoJSON).

**Storage**: To adhere to best practices for data organization, we implemented src/storage.py. This script initializes a SQLite database (data/project_data.db) and loads the raw CSV and JSON data into three distinct tables (raw_sales, raw_universe, raw_cta). This database serves as the single source of truth for downstream processing.

### 3.2. Integration and Geospatial Enrichment

The most complex technical challenge was merging the sales data (which lacks coordinates) with location data.

**PIN-Join**: We utilized the 14-digit Property Index Number (PIN) as the primary key. We handled data inconsistencies by zero-padding PINs to ensure accurate string matching between the raw_sales and raw_universe tables.

**Distance Calculation**: We developed a geospatial enrichment logic (found in notebooks/3_geospatial_enrichment.ipynb). Using scipy.spatial.KDTree, we constructed a spatial tree of all CTA station coordinates. We then queried this tree for every property in the dataset to find the nearest station and calculate the Euclidean distance in meters. This added two critical features to our dataset: min_distance_meters and nearest_cta_station.

### 3.3. Data Cleaning and Filtering

To address the scope changes described in Section 2, we implemented strict cleaning logic in notebooks/4_data_filtering_cleaning.ipynb (logic finalized in src/clean.py).

**Homogeneity Filter**: We filtered the class column to strictly keep codes 202 through 209 (Single Family Homes).

**Market Validity**: We applied boolean filters to exclude non-market sales (is_multisale is False, sale_price > $10k, Warranty/Trustee deeds only).

**Temporal Filter**: We filtered for sales occurring between 2018 and 2024 to ensure recent market relevance.

**Outlier Removal**: We capped the top and bottom 1% of sale prices to remove extreme outliers that would skew the mean.

---

## 2. Updated Task Status and Artifacts

The table below reflects the current status of all project milestones. The updated target completion dates reflect the streamlined process.

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
| Statistical Analysis & Visualization Script | Shenhua Zhang | November 17, 2025 | In-Progress | Initial correlation and premium calculation in notebooks/5_exploring_analysis.ipynb |
| Workflow Automation (Snakemake implementation) | Jenny Mai | December 5, 2025 | To Do | Snakefile |
| **Phase 5: Final Submission** | | | | |
| Final README.md Report of Findings & Documentation | Shenhua Zhang | December 10, 2025 | To Do | |
| Final Project Tag/Release & Box Upload | Both | December 10, 2025 | To Do | |

---

## 4. Team Member Contributions

### Jenny Mai (ETL Foundation & Data Acquisition & Cleaning)
During this milestone, I was responsible for establishing the robust and reproducible Extract, Transform, and Load (ETL) foundation for the project. This involved completing the initial Data Acquisition of all three required datasets (Sales, Universe/Location, and CTA Stations) and formalizing the storage strategy by implementing the `src/storage.py` script to load all raw files into the SQLite database (`project_data.db`). I also completed the core integration task by implementing the PIN-Join and Geospatial Enrichment script, which calculated and attached the `min_distance_meters` feature to the property sales data. Finally, I executed the final Data Cleaning and Standardization logic in the workflow, applying strict filters for property type, market validity, and temporal consistency, resulting in the final, clean `final_cleaned_data.csv` ready for Shenhua’s statistical analysis.


### Shenhua Zhang (Data Quality & Analysis)
For Milestone 3, I was responsible for the statistical analysis between Cook County Property Sales and CTA Railway proximity. Given our three revised research questions, I analyzed them with appropriate statistical methods. For RQ1, I used `.corr()` to identify the correlation between CTA distance and sale price, which turned out to be a weak negative correlation (-0.23), suggesting that as distance increases, price slightly decreases. For RQ2, I processed the `nearest_cta_lines` text data into boolean columns to identify line colors (e.g., `contains_blue`, `contains_red`). I found that while individual lines have different degrees of correlation, the relationships were generally weak. Finally, for RQ3, I investigated the interaction between property class and distance. I first verified via heatmap that `class` and `distance` were not collinear (-0.23). I then ran a regression model (`sale_price ~ min_distance_meters * Q('class')`), which indicated a moderate influence (R² = 0.392) of the interaction term on sale price.

---

## 5. Preliminary Analytical Findings

As a result of the completed data cleaning and filtering, we performed an initial analysis on the filtered dataset (`final_analytic_data.csv`) to validate the project's core premise and provide preliminary findings for this report.

| Metric | Value | Interpretation |
| :--- | :--- | :--- |
| **RQ 1: Correlation (Distance vs. Sale Price)** | -0.22 | We observed a statistically significant negative correlation. In this context, a negative correlation implies that as the distance to the station increases, the sale price decreases. This preliminarily supports the hypothesis that proximity to transit is associated with higher property values. |
| **RQ 2: Correlation (CTA Line Number vs. Sale Price)** | 0.107 | We observed weak correlations between specific line colors and price. This suggests that while location matters, the specific line (Red vs. Blue) may be less of a driver of price than the distance itself or the neighborhood characteristics. |
| **RQ 3: Model Fit (R²)** | 0.377 | Our initial regression model, which accounts for both distance and the specific type of single-family home (Class), explains approximately 38% of the variance in sale price. This is a promising start for a real estate model using only two primary variables. |

These initial findings confirm that the integrated and cleaned dataset is suitable for statistical analysis. The data behaves as expected for the domain (showing a "transit premium"), validating the quality of our cleaning pipeline.

---

## 7. Next Steps

With the data infrastructure and cleaning complete, the team will focus on the final two phases of the project:

- Visualization (Shenhua): We will generate some more visualizations, including scatter plots of Distance vs. Price and Box Plots comparing prices across different transit lines and some geospatial visualizations.
- Workflow Automation (Jenny): We will implement Snakemake to chain our Python scripts (acquire.py -> storage.py -> enrich.py -> clean.py -> analysis.py) into a single reproducible command.
- Final Reporting: We will synthesize the statistical findings into the final README.md report.
