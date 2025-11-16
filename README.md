# Arden Confectionary Sales Data Visualization

## Course Information
**Course:** COM7021 – Data Visualisation  
**Institution:** Arden University  
**Student:** Muhammad Umar Uz Zaman  
**Student ID:** STU1197819  

## Project Overview

This project analyzes UK confectionary sales data to understand regional performance, product profitability, and temporal trends. The analysis aims to provide actionable insights for business decision-makers in the British Confectionary Council.

### Key Research Questions
1. **Regional Performance:** How do sales and profitability differ between UK regions?
2. **Product Analysis:** Which confectionery products have the highest and lowest profit margins?
3. **Temporal Trends:** How do regional sales change over time, and which regions show peak performance?

## Dataset

**Source:** `confectionary.xlsx`  
**Records:** 1,001 sales transactions  
**Time Period:** 2000-2005  
**Regions:** England, Jersey, Northern Ireland, Scotland, Wales  

### Data Structure
- **Date:** Transaction date
- **Country(UK):** UK region
- **Confectionary:** Product type (Chocolate Chunk, Caramel Nut, Biscuit, etc.)
- **Units Sold:** Quantity sold
- **Cost(£):** Cost price
- **Profit(£):** Profit amount
- **Revenue(£):** Revenue amount

## Analysis Components

### 1. Exploratory Data Analysis (EDA)
- **Data Cleaning:** Handling missing values, standardizing product names
- **Descriptive Statistics:** Distribution analysis of key metrics
- **Visual Exploration:** Histograms, box plots, and correlation analysis

### 2. Regional Analysis
- **Performance Metrics:** Total revenue, profit, and units sold by region
- **Profit Margins:** Average profit margins across regions
- **Comparative Visualizations:** Bar charts and ranking analysis

### 3. Product Analysis
- **Profitability Assessment:** Profit margins by confectionery type
- **Volume vs. Profit:** Scatter plots and ranking charts
- **Regional Product Performance:** Cross-tabulation analysis

### 4. Temporal Analysis
- **Time Series Trends:** Monthly sales patterns by region
- **Seasonality Detection:** Peak sales periods identification
- **Year-over-Year Growth:** Annual performance comparison

### 5. Interactive Dashboard (Planned)
- **Streamlit Application:** Real-time data exploration
- **Dynamic Filters:** Region, product, and date range selection
- **KPI Cards:** Key performance indicators display
- **Interactive Charts:** Region-level, product-level, and time series visualizations

## Project Structure

```
├── main.ipynb                 # Main analysis notebook with comprehensive EDA
├── confectionary.xlsx        # Raw sales data
├── grading criteria.xlsx     # Assessment criteria
├── Task.pdf                  # Project requirements
├── outputs/                  # Aggregated data exports
│   ├── region_summary.csv       # Regional performance summary
│   ├── region_conf_summary.csv  # Region × Product analysis
│   ├── month_region.csv         # Monthly regional sales
│   └── year_region.csv          # Annual regional sales
├── generate_visualizations.py # Script to create visualization images
├── images/                   # Generated visualization images
│   ├── key_distributions.png
│   ├── regional_profit.png
│   └── product_profit.png
├── src/                      # Source code modules
│   └── data_prep.py          # Data preparation functions
├── dashboard/                # Interactive dashboard
│   ├── app.py                # Streamlit application
│   └── capture_dashboard_screenshots.py # Screenshot capture tool
└── README.md                 # This file
```

## Key Findings

### Regional Performance (2000-2005)
- **Scotland:** Highest total revenue (£633.4M) and profit (£926.3K)
- **Jersey:** Strong profit margins (0.32%) and consistent performance
- **Northern Ireland:** Best average profit margin (0.38%)
- **Wales:** Competitive performance across multiple metrics

### Product Performance
- **Chocolate Chunk:** Most popular product by volume
- **Caramel Nut:** Strong profit performance
- **Regional Variations:** Different products excel in different regions

### Temporal Patterns
- **Peak Seasons:** Varying peak periods across regions
- **Growth Trends:** Overall positive sales trajectory
- **Seasonal Variations:** Clear monthly patterns in sales volume

## Visualizations & Results

### Data Distributions
![Key Distributions](images/key_distributions.png)
*Figure 1: Distribution of key metrics showing right-skewed patterns in revenue and profit, indicating a few large transactions drive most of the business value.*

### Regional Performance
![Regional Profit](images/regional_profit.png)
*Figure 2: Total profit by UK region (2000-2005), with Scotland leading in absolute profit while Northern Ireland shows strongest profit margins.*

### Product Performance
![Product Profit](images/product_profit.png)
*Figure 3: Profit by confectionery type, highlighting Chocolate Chunk as the volume leader and Caramel Nut as a premium margin product.*

### Dashboard Preview
The interactive Streamlit dashboard includes:
- **KPI Cards:** Total units, revenue, profit, and average margin (dynamically updating)
- **Regional Analysis:** Interactive bar charts showing profit by region
- **Product Insights:** Performance comparison across confectionery types
- **Time Series:** Monthly trends with region filtering and interactive legends
- **Cross-Analysis:** Heatmap showing profit margins by region and product type

**🎯 Key Dashboard Benefits:**
- **Real-time Filtering:** Instantly see how different combinations affect business metrics
- **Interactive Exploration:** Hover over charts for detailed information
- **Business Intelligence:** Support data-driven decision making for the British Confectionary Council
- **Mobile Friendly:** Responsive design that works on all devices

### Key Statistics Summary

| Metric | Mean | Median | Std Dev | Min | Max |
|--------|------|--------|---------|-----|-----|
| Units Sold | 1,452 | 1,374 | 937 | 1 | 4,452 |
| Revenue (£) | 2.1M | 1.8M | 1.8M | -1.4M | 19.7M |
| Profit (£) | 3,200 | 2,700 | 3,400 | -8,000 | 31,000 |
| Profit Margin | 0.31% | 0.29% | 0.15% | -0.76% | 1.2% |

*Data based on 984 cleaned transactions after removing missing values*

## Contact Information

**Student:** Muhammad Umar Uz Zaman  
**Student ID:** STU1197819  
**Course:** COM7021 – Data Visualisation  
**Institution:** Arden University  

## Acknowledgments

- Arden University for course materials and assessment framework
- British Confectionary Council for providing the dataset
- Open-source Python community for data science tools

---

*This project demonstrates comprehensive data visualization skills for business intelligence applications, focusing on actionable insights for non-technical decision-makers.*
