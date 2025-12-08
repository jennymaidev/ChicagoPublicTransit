# Analyzing Public Transit Impact on Chicago Property Values

## Contributors
- Jenny Mai
- Shenhua Zhang

## Summary

The relationship between public transportation accessibility and residential property values represents a critical area of inquiry in urban planning and real estate economics. This project quantitatively assesses the influence of the Chicago Transit Authority (CTA) rail system on residential property values within Cook County, leveraging data curation and data lifecycle management techniques to acquire, integrate, clean, and analyze three distinct public datasets. Our analysis addresses a fundamental question for urban planners, real estate investors, and prospective homebuyers: does proximity to transit infrastructure meaningfully correlate with higher property values?

The motivation for this research stems from the broader concept of transit-oriented development (TOD), which posits that communities built around public transportation networks demonstrate enhanced economic vitality and social cohesion. Understanding the empirical relationship between CTA accessibility and property pricing provides data-driven insights that can inform decisions regarding real estate investment, neighborhood development, and infrastructure prioritization. For residents considering relocation within the Chicago metropolitan area, such analysis offers concrete evidence of the value proposition offered by transit-accessible locations. For urban planners and municipal policymakers, quantifying the property value impact of transit investments justifies the significant capital expenditures required for system expansion and maintenance.

This project employs a rigorous, reproducible workflow encompassing the full data lifecycle: acquisition of raw datasets from authoritative public sources, integration of geospatial data through coordinate-based proximity analysis, systematic cleaning and filtering to ensure analytical validity, and statistical modeling to address our core research questions. We integrated property sales data from the Cook County Assessor's office with precise geolocation information and CTA station coordinates to create a comprehensive dataset of 124,438 single-family residential transactions recorded between 2018 and 2024.

Our analysis addresses three interconnected research questions:

* (1) Is there a statistically significant correlation between the Euclidean distance of a residential property from the nearest active CTA rail station and its raw sale price?
* (2) How does the specific CTA transit line color (e.g., Red Line versus Blue Line) influence the magnitude and direction of this correlation?
* (3) To what extent do property class and minimum distance to the CTA station jointly influence residential sale prices, and what is the strength of this relationship?

The findings of our analysis reveal a nuanced relationship between transit proximity and property values in Cook County. We observed a statistically significant but weak negative correlation (r = -0.225) between distance to the nearest CTA station and property sale price, indicating that properties in closer proximity to transit nodes command modest price premiums. When examining specific transit lines, we found negligible correlations between proximity to specific CTA lines and sale price (|r| < 0.005), suggesting that the transit premium is driven by general proximity to transit rather than to specific line characteristics. Most notably, our regression analysis incorporating both property class and distance as interactive predictors yielded an R² value of 0.392, indicating that these two variables jointly explain approximately 39% of the variance in property sale prices, a moderate effect size that suggests additional unmeasured factors (such as neighborhood socioeconomic characteristics, school quality, and historical significance) meaningfully influence residential property values.

## Data Profile

Our analysis integrates three complementary datasets from authoritative public sources: property transaction records, property geolocation information, and transit infrastructure locations.

### Dataset 1: Cook County Assessor - Parcel Sales

The primary dataset comprises Cook County Assessor's Parcel Sales records (2.62 million transactions). Each record includes the Property Index Number (PIN, a unique 14-digit identifier), sale price (USD), sale date (ISO 8601), deed type classification, and boolean flags for multi-parcel sales. The dataset was accessed via direct CSV download from the Cook County Data Portal (https://datacatalog.cookcountyil.gov/Property-Taxation/Assessor-Parcel-Sales/wvhk-k5uv/) and is designated as public domain, requiring no authentication.

The dataset encompasses all property classes and transaction types, including commercial, agricultural, residential properties, and non-market transactions (inheritances, court-ordered sales, corporate transfers). Property sales information is legally classified as public record in Illinois under the Property Tax Code. Our analysis excludes owner name fields entirely, focusing on property characteristics and transaction details. Cook County government explicitly permits research use without restriction.

### Dataset 2: Cook County Assessor - Parcel Universe

The Parcel Universe contains geospatial coordinates and property class codes for 48.8 million parcels in Cook County. This authoritative registry includes pre-calculated longitude and latitude coordinates (typically parcel polygon centroids) and three-digit property class codes. Each record uses the same 14-digit PIN as the sales dataset, enabling direct relational joins.

We retained only classes 202-209 (one-story and two-story single-family detached homes) to ensure analytical homogeneity. The dataset was accessed through the Cook County Data Portal API (https://datacatalog.cookcountyil.gov/Property-Taxation/Assessor-Parcel-Universe/nj4t-kc8j/) and is designated as public domain with no licensing restrictions. Privacy considerations are minimal: the dataset contains only property location information and administrative codes without personally identifiable information.

### Dataset 3: Chicago Transit Authority - 'L' Rail Stations

The CTA dataset provides precise geospatial coordinates and operational metadata for 145 active rail stations as of August 2024. Obtained from the City of Chicago Open Data Portal (https://data.cityofchicago.org/Transportation/CTA-L-Rail-Stations/3bzw-cg4m/) in GeoJSON format, each record includes station name, transit lines served, longitude/latitude coordinates, ADA accessibility information, and street address.

CTA station data is published under Creative Commons Attribution 4.0 (CC-BY-4.0) by the City of Chicago and CTA, requiring attribution for research use. The data is updated regularly to reflect current transit system configuration. Privacy considerations are non-existent: the dataset contains only public infrastructure locations.

### Data Integration Strategy

We integrated datasets through multi-stage processing: (1) relational join of Parcel Sales and Parcel Universe using 14-digit PIN as primary key, requiring PIN format standardization to address zero-padding inconsistencies; (2) geospatial enrichment using scipy's KDTree algorithm for nearest-neighbor spatial queries. We constructed a spatial tree of 145 CTA station coordinates, then queried this tree to identify the nearest station for each property and calculate Euclidean distance in meters. This enrichment appended two features: minimum distance to nearest CTA station and station name/line(s).

### Ethical and Legal Compliance

All datasets are explicitly designated for public use by government agencies. Cook County and Chicago authorize research use without formal data use agreements. No sensitive personally identifiable information is included; we exclude owner names and contact information. Parcel Sales data represents legally public record under Illinois property tax law.

Our analysis focuses on aggregate statistical patterns rather than individual properties. Results are reported at aggregate levels (citywide correlations, regression coefficients) with no individual property-level findings disclosed. The project complies fully with data use policies and does not require Institutional Review Board approval, involving only secondary analysis of existing public record data.

## Data Quality

Our data quality assessment employed validation across completeness, accuracy, and consistency dimensions, followed by systematic data cleaning to create an analytically valid dataset.

### Assessment Methodology

We audited three dimensions: completeness (missing values), accuracy (value validity), and consistency (format adherence). Audits were performed on each dataset after acquisition and after integration to identify source-level and integration-induced errors.

### Completeness Assessment

The Parcel Sales dataset showed excellent completeness: PIN (100%), sale_price (99.8%, with 5,244 null/zero values excluded), and sale_date (99.6%, with 10,480 invalid dates validated against deed records). The Parcel Universe provided coordinates for 99.2% of parcels (48.2M of 48.8M), with missing values representing unimproved land or unsurveyed areas. Property class and PIN fields were 100% complete. CTA station data showed perfect completeness (100%) across all 145 stations. Following integration via PIN joins, 2.59 million records (98.8%) retained both transaction and location information.

### Accuracy Assessment

Coordinate validation against satellite imagery showed 99.1% of coordinates fell within Cook County boundaries with plausible locations. We identified 23,700 records (0.9%) in geographic anomalies (lake areas, outside boundaries), likely representing data errors or polygon centroid issues. Sale price validation using domain knowledge (typical range \$50,000-\$1,500,000) revealed 3.2% exceeding \$2M (likely misclassified commercial) and 0.4% below \$5,000 (gifts, inheritances, errors). Property class codes aligned with Cook County's scheme, though application inconsistencies existed (multi-family occasionally classified as single-family).

### Consistency Assessment

We examined field relationships across datasets. PIN format inconsistency required standardization: raw sales data used variable zero-padding (12-14 digits) while Parcel Universe used consistent 14-digit PINs. We implemented standardization to enable successful joins. Price distributions stratified by property class appeared log-normal for residential classes (202-209) but showed anomalies for non-residential classes. Date validation identified 1,247 transposed/erroneous dates (e.g., 1990s dates in 2018-2024 dataset).

### Data Cleaning and Filtering

We applied systematic filtering to create an analytically valid dataset, guided by three objectives: (1) sample homogeneity for valid inference, (2) exclusion of non-market transactions, and (3) removal of quality anomalies. We adopted filtering rather than imputation, documenting all criteria while retaining raw data for reproducibility.

**Property Class Homogeneity**: We retained only single-family detached residences (class codes 202-209), reducing from 1.78M to 542,787 records (30.4% retention). This ensures comparability, as including condominiums, commercial properties, or land would introduce heterogeneity unrelated to transit proximity.

**Non-Market Transaction Exclusion**: We retained only Warranty Deeds and Contract for Deed transactions, excluding Trustee Deeds (foreclosures), Tax Deeds (auctions), Gift Deeds, and inheritances. The is_multisale field excluded multi-parcel transactions. This reduced records from 542,787 to 452,038 (17% elimination), ensuring prices reflect buyer willingness to pay.

**Temporal Filtering**: We retained 2018-2024 sales only, ensuring contemporaneous market conditions while avoiding temporal confounding from long-term trends. This seven-year window captures post-2008 recovery and pandemic-era markets, reducing records from 452,038 to 126,829.

**Geographic Filtering**: We excluded properties with nearest stations outside Cook County or exceeding 25 km distance (15.5 miles), a conservative threshold capturing reasonable transit commuting distance while removing anomalies.

**Price Outlier Filtering**: We trimmed the top and bottom 1% of sale prices (below \$25,000, above \$1,550,000), removing approximately 2,540 records likely representing data errors, non-standard transactions, or misclassified properties. This reduced the dataset from 126,829 to 124,438 records.

**Coordinate Validity**: We excluded 8,500 records with distances exceeding 50 km or coordinates in geographic impossibilities (water bodies, outside county).

### Final Dataset Summary

The filtering process reduced 1.78M enriched transactions to 124,438 single-family residential sales (2018-2024), a 6.97% retention rate reflecting legitimate criteria for analytical validity. The final dataset represents arm's-length market transactions for comparable property types. Mean sale price: \$288,717 (SD \$227,000); median: \$247,000 (modest right skew). Distances ranged 30m-34,227m (mean 5,237m, median 4,642m), indicating most properties lie within 5-8 km of transit access.

## Findings

Our statistical analysis addressed three research questions on transit accessibility and property values in Cook County.

### Research Question 1: Distance-Price Correlation

We calculated a Pearson correlation of r = -0.227 (p < 0.001) between distance to nearest CTA station and sale price—a weak but statistically significant negative correlation. Distance alone explains only 5.2% of price variance (r² = 0.052). Figure 1 shows substantial scatter around the regression line, with properties immediately adjacent to stations displaying considerable price variation, indicating that factors beyond transit proximity substantially influence property values.

![Figure 1: Distance to Nearest CTA Station vs. Property Sale Price](docs/figures/distance_vs_price_by_class.png)
*Figure 1: Scatter plot showing the relationship between distance to nearest CTA station (meters) and property sale price (USD), colored by property class. The fitted regression line indicates a weak negative relationship (r = -0.225) between proximity to transit and property values.*

This aligns with transit-oriented development literature: transit proximity represents one of many factors influencing property values, including neighborhood socioeconomics, school quality, and building characteristics.

### Research Question 2: Line-Specific Effects

Correlations between specific CTA lines and sale price were negligible (|r| < 0.005). The Red Line showed r ≈ -0.004; other lines ranged from r ≈ -0.003 (Green) to r ≈ 0.0005 (Blue). Multi-line transit hubs showed no premium over single-line stations (r ≈ -0.0002). This null finding contrasts with our hypothesis that high-capacity downtown lines would show stronger premiums. The transit premium is driven by general accessibility rather than specific line characteristics, suggesting peripheral line investments may yield comparable property value benefits to high-capacity lines.

![Figure 2: Distance to Nearest CTA Station vs. Property Sale Price by Number of Transit Lines](docs/figures/distance_vs_price_by_line_num.png)
*Figure 2: Scatter plot showing the relationship between distance to nearest CTA station and property sale price, stratified by the number of transit lines serving the nearest station (proxy for hub importance). The consistency of negative slopes across categories demonstrates that line-specific effects contribute negligibly to the transit premium.*

### Research Question 3: Interactive Effects of Class and Distance

Ordinary least squares regression (sale_price ~ class + distance + class × distance) achieved R² = 0.392, with property class and distance jointly explaining 39.2% of price variance—substantially improving the 5.2% explained by distance alone. The distance coefficient was -\$0.48 per meter (\$4,800/km), meaning a property at median distance (4.64 km) commands a \$13,900 premium over one at 7 km. Property class was highly significant (p < 0.001), while the interaction term (class × distance) showed significance but modest magnitude. Figure 3 confirms consistent downward trends across property classes despite slight slope variations.

![Figure 3: Distance to Nearest CTA Station vs. Property Sale Price by Property Class](docs/figures/distance_vs_price_by_class.png)
*Figure 3: Scatter plot with fitted regression lines showing the relationship between distance to nearest CTA station and property sale price, stratified by property class (202-209). The parallel slopes across classes indicate consistent distance effects regardless of property type, with class primarily affecting the intercept (baseline price level).*

Figure 4 confirms low correlation between class and distance (r ≈ -0.01), validating minimal multicollinearity.

![Figure 4: Correlation Matrix - Property Class, Transit Distance, and Sale Price](docs/figures/correlation_heatmap.png)
*Figure 4: Heatmap of the correlation matrix showing relationships between property class, distance to nearest CTA station, and sale price. The low off-diagonal correlations (|r| < 0.2) confirm minimal multicollinearity, supporting the validity of regression coefficient estimates.*

## Future Work

This project successfully demonstrated the feasibility of integrating large-scale public datasets to address questions in urban economics. However, our findings revealed important opportunities for extending and refining this analysis.

### Lessons Learned

Throughout the project lifecycle, we encountered several key challenges that inform future work. Data integration at scale required careful attention to quality and type consistency; PIN zero-padding inconsistencies between datasets initially prevented successful joins until we implemented standardization routines. We discovered that filtering decisions substantially shape outcomes: our initial plan included a fourth dataset (Cook County Residential Characteristics), but 40% sparsity and inconsistencies with the Parcel Universe prompted a strategic pivot toward property class codes as proxy measures for structural characteristics.

Most importantly, the modest transit premiums we observed (r = -0.225) align with published literature on transit effects in other major U.S. cities, suggesting that unmeasured confounding variables (neighborhood socioeconomics, school quality, crime rates, walkability, retail amenities) substantially mediate the relationship between transit proximity and property values. The null findings for line-specific effects highlight the critical importance of testing hypotheses rigorously rather than accepting intuitive priors: our expectation that high-capacity downtown lines would show stronger premiums than peripheral lines proved empirically unfounded.

Implementing Snakemake workflow automation midway through the project underscored the importance of investing in reproducibility infrastructure early in the data lifecycle. Retrospectively adding workflow automation required substantial refactoring of existing notebooks and scripts. Future projects would benefit from implementing workflow automation from the outset, enabling incremental development within a reproducible framework rather than retrofitting automation after analysis completion.

### Recommended Data Integration

The most promising direction involves integrating datasets that could explain the 61% of unexplained variance in our regression model. The U.S. Census Bureau's American Community Survey (ACS) provides neighborhood-level socioeconomic data (median household income, educational attainment, racial composition); Illinois Department of Education publishes school performance metrics (standardized test scores, graduation rates); and Chicago Police Department provides crime statistics by block. These additions would enable decomposition of the transit premium into direct accessibility effects versus indirect effects mediated through neighborhood characteristics and perceived safety. Additionally, integrating walkability scores, retail density, and employment center locations would provide a more comprehensive model of urban property valuation.

### Methodological Extensions

Several analytical enhancements could improve our findings. Nonlinear models (spline regression, generalized additive models) could test for threshold effects at distances beyond pedestrian accessibility (0.5-0.8 km), as transit benefits may diminish nonlinearly with distance. More sophisticated accessibility measures accounting for actual walking route distance (rather than Euclidean distance), physical barriers (highways, rivers), and service frequency could better characterize transit proximity.

Panel data approaches treating properties as repeated units over time would reveal temporal dynamics and the impact of service changes or station openings, enabling causal inference rather than purely correlational analysis. Spatial econometric models incorporating spatial autocorrelation would account for neighborhood spillover effects known to influence real estate markets, addressing potential violations of regression independence assumptions. Hedonic pricing models including comprehensive property characteristics (square footage, lot size, building age) would improve variance explanation and isolate transit effects more precisely.

### Additional Opportunities

Extending this methodology to other major metropolitan areas (New York, Washington D.C., San Francisco, Boston) would enable comparative analysis of how urban structure, transit system maturity, and transit mode influence transit premiums. Cross-city comparisons could test hypotheses about whether rail transit shows different capitalization effects than bus rapid transit systems.

Developing interactive decision support tools and web applications could help real estate investors and urban planners apply these findings to individual properties and transit investment evaluations. Publishing final datasets to permanent archival repositories (Zenodo, Dataverse) with DOIs and creating containerized Docker environments would enhance long-term reproducibility and facilitate replication studies.

## Reproducing These Results

To reproduce this analysis from initial data acquisition through final statistical results, follow these sequential steps. Complete code and workflows are available in the project repository.

### Prerequisites and Software Setup

This analysis requires Python 3.9 or later. Install required dependencies using pip:

```bash
pip install -r requirements_frozen.txt
```

This installs all packages at the specific versions used during analysis, ensuring bit-for-bit reproducibility of computational results.

### Step 1: Data Acquisition

Download raw datasets from public sources by executing the acquisition notebook:

```bash
jupyter notebook notebooks/01_data_acquisition.ipynb
```

This notebook downloads three datasets: Cook County Parcel Sales (CSV), Cook County Parcel Universe locations (via Socrata API), and CTA station locations (GeoJSON). The notebook includes error handling and retry logic for network timeouts and implements checksum verification (SHA-256) to detect corruption during download.

Raw datasets will be saved to `data/raw/` with the following filenames:
- `sales_data_raw.csv` (2.6 GB; 2.62 million records)
- `cta_l_stops.geojson` (18 KB; 145 stations)

Expected runtime: 10 minutes depending on network bandwidth. The notebooks include progress indicators and estimated time remaining.

### Step 2: Data Storage and Geocoding

Execute the geocoding and PIN location lookup notebook to standardize PINs and validate coordinates:

```bash
jupyter notebook notebooks/02_pin_location_geocoding.ipynb
```

This step validates geographic coordinates, identifies geographic anomalies, and standardizes PIN formatting (zero-padding to 14 digits). Processed intermediate data is saved to `data/interim/`.

Expected runtime: ~370+ hours.

### Step 3: Geospatial Enrichment

Execute the geospatial enrichment notebook to calculate distances from properties to nearest CTA stations:

```bash
jupyter notebook notebooks/03_geospatial_enrichment.ipynb
```

This computationally intensive step constructs a KDTree of station locations and queries this tree to identify the nearest station for each property and calculate Euclidean distance. The enriched dataset (1.78 million records) is saved to `data/interim/sales_data_enriched.csv`.

Expected runtime: 5 minutes (highly dependent on available RAM and processor core count; 16 GB RAM recommended).

### Step 4: Data Cleaning and Filtering

Execute the data cleaning notebook to apply filtering criteria and create the final analytical dataset:

```bash
jupyter notebook notebooks/04_data_filtering_cleaning.ipynb
```

This step applies the filtering criteria documented in Section V: property class homogeneity (single-family homes only), non-market transaction exclusion, temporal filtering (2018-2024), price outlier trimming, and geographic validity checks. The final analytical dataset is saved to `data/processed/final_cleaned_data.csv`.

Expected runtime: 5 minutes.

### Step 5: Statistical Analysis and Visualization

Execute the analysis notebook to reproduce all statistical results and generate visualizations:

```bash
jupyter notebook notebooks/05_exploring_analysis.ipynb
```

This notebook calculates correlation coefficients, generates scatter plots and box plots, conducts regression analysis, and produces all figures included in this report. Results are saved to `docs/figures/`.

Expected runtime: 5 minutes.

### Alternative: Full Workflow Automation with Snakemake

To execute the complete end-to-end workflow automatically, use the provided Snakefile:

```bash
snakemake --cores all --use-conda
```

This command executes all steps in the correct order, with parallel execution where possible. Snakemake automatically re-runs only steps whose inputs have changed, enabling efficient re-execution during development.

### Data Location in Box

Raw and processed data exceeding GitHub's repository size limits are stored in Box at https://uofi.box.com/s/90qg970raf1p20hqmwn1cu4lccqmevte. Download the complete data folder from Box and extract it to your local project directory:

```bash
# After downloading from Box:
unzip data.zip -d /path/to/project/
```

This will restore the `data/raw/`, `data/interim/`, and `data/processed/` directories with all datasets required for analysis. Do not commit these directories to GitHub; they are included in `.gitignore`.

### Expected Outputs

Upon successful reproduction of the complete workflow, you should observe the following artifacts:

- `data/processed/final_cleaned_data.csv`: 122,544 rows × 12 columns; final analytical dataset
- `docs/figures/`: Directory containing five visualizations (scatter plots, box plots, regression diagnostics)
- Console output displaying correlation coefficients, regression summary statistics, and model diagnostics

Numerical results should match those presented in Section V of this report to at least four decimal places (minor variations due to floating-point arithmetic precision are acceptable).

### System Requirements and Runtime Estimates

- **Processor**: Intel Core i7 or equivalent; 8 cores minimum, 16 cores recommended
- **RAM**: 16 GB minimum, 32 GB recommended (geospatial enrichment is memory-intensive)
- **Storage**: 15 GB free disk space for raw and intermediate data
- **Network**: Broadband internet connection with upload/download speeds ≥ 10 Mbps
- **Total Runtime**: ~375 hours for complete workflow (highly dependent on system specifications and network bandwidth)

## References

### Datasets Cited

Cook County Assessor's Office. (2025). *Assessor - Parcel Sales*. Cook County Data Portal. Retrieved from https://datacatalog.cookcountyil.gov/Property-Taxation/Assessor-Parcel-Sales/wvhk-k5uv/

Cook County Assessor's Office. (2025). *Assessor - Parcel Universe*. Cook County Data Portal. Retrieved from https://datacatalog.cookcountyil.gov/Property-Taxation/Assessor-Parcel-Universe/nj4t-kc8j/

Chicago Transit Authority. (2024). *CTA - 'L' (Rail) Stations*. City of Chicago Open Data Portal. Retrieved from https://data.cityofchicago.org/Transportation/CTA-L-Rail-Stations/3tzw-cg4m/

### Software and Libraries

Pedregosa, F., Varoquaux, G., Gramfort, A., et al. (2011). Scikit-learn: Machine learning in Python. *Journal of Machine Learning Research*, 12, 2825–2830.

Harris, C. R., Millman, K. J., van der Walt, S. J., et al. (2020). Array programming with NumPy. *Nature*, 585(7825), 357–362.

McKinney, W. (2010). Data structures for statistical computing in Python. In *Proceedings of the 9th Python in Science Conference* (pp. 51–56).

Hunter, J. D. (2007). Matplotlib: A 2D graphics environment. *Computing in Science & Engineering*, 9(3), 90–95.

Waskom, M. L. (2021). seaborn: Statistical data visualization. *Journal of Open Source Software*, 6(60), 3021.

Seabold, S., & Perlin, A. (2010). statsmodels: Econometric and statistical modeling with Python. In *Proceedings of the 9th Python in Science Conference* (pp. 57–61).

Rocklin, M. (2015). Dask: Parallel computation with blocked algorithms and task scheduling. In *Proceedings of the 14th Python in Science Conference* (pp. 130–136).

Mölder, F., Jablonski, K. P., Letcher, B., et al. (2021). Sustainable data analysis with Snakemake. *F1000Research*, 10, 33.

Kelsey, T., Weisman, S., Hall, R., & Reilly, B. (2012). Geopandas: Python tools for geographic data. Retrieved from https://github.com/geopandas/geopandas

### Data Licenses and Attribution

All project code is released under Creative Commons Attribution 4.0 (CC-BY-4.0). Cook County Assessor datasets are in the public domain. CTA station data is released under CC-BY-4.0 by the City of Chicago and Chicago Transit Authority.