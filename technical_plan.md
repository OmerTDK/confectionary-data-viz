# COM7021 – Data Visualisation  
## Technical Coding Plan for Task 1 & Task 2 (for Coding Agent)

This document describes, in **executable-level detail**, how to implement the Python-side work for the assignment, including:

- Data loading, cleaning, and feature engineering
- Exploratory data analysis (EDA)
- Analytical visualisations (static + interactive)
- An interactive dashboard
- Support for the written report and grading criteria

The plan includes **decision points**, **branching options**, and **best practices**, so an automated coding agent can follow it step by step.

> **Important constraints (must be respected):**
> - Use **Python** for all analysis and visualisation.
> - Dataset: `confectionary.xlsx` (or `Confectionary_4564.xlsx`).
> - Must support **Task 1** (visualisation and EDA + dashboard) and **Task 2** (report & justification).
> - Visualisations must be chosen and implemented in a way that can be **justified** for **non-technical decision-makers** (board/CEO).
> - Some focus on **EDA**, but not overkill.
> - Final document uses numbered headings: `1`, `1.1`, `1.1.1`, etc. (this affects how we name code sections and comments in support).


---

## 0. Project Structure and Environment

### 0.1 Directory Layout

**Goal:** Create a clean structure that separates data, notebooks/scripts, and dashboard code.

**Required folders (if not present, create):**

- `data/`
  - Store `confectionary.xlsx`.
- `notebooks/`
  - Store Jupyter notebooks (if using).
- `src/`
  - Store Python modules (if using script-based approach).
- `dashboard/`
  - Store dashboard app code (e.g., Streamlit, Dash).

**Decision Point 0.1.A – Notebook vs Script Style**

- **Option 1 (Recommended for clarity + marking):**  
  Use **Jupyter Notebooks** for EDA & visualisations, and a separate **dashboard app** script.
  - `notebooks/01_eda_and_visuals.ipynb`
  - `dashboard/app.py`
- **Option 2:**  
  Use pure Python scripts with modular functions and maybe a `main.py`:
  - `src/eda.py`, `src/plots.py`, `dashboard/app.py`, etc.

**Best Practice:**  
Use **Option 1** for human readability and marking, but structure notebook with **clear sections** that correspond to the report headings (`1.1`, `1.2`, etc.).


### 0.2 Environment Setup

**Create a Python environment** with at least the following packages:

```bash
pip install pandas numpy matplotlib seaborn plotly streamlit (or dash)
```

**Required imports in analysis code (baseline):**

```python
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

import plotly.express as px
import plotly.graph_objects as go

# For dashboard (choose one)
# import streamlit as st
# or
# from dash import Dash, dcc, html
```

**Best Practices:**
- Set a consistent visual style for matplotlib / seaborn (e.g., `sns.set_theme()`).
- Use a **random seed** if any random sampling is used (not strictly needed here but good practice).
- Configure plots to have **clear labels, titles, and legends** – this will matter for marking.


---

## 1. Data Loading and Initial Inspection

### 1.1 Load Data

**Create a function or notebook cell to load the data:**
- Input file: `data/confectionary.xlsx`  
- Output: a pandas DataFrame `df`

```python
DATA_PATH = "data/confectionary.xlsx"

df = pd.read_excel(DATA_PATH)
```

**Check basic information:**

```python
print(df.shape)
print(df.dtypes)
df.head()
```

**Expected columns (for reference):**
- `Date`
- `Country(UK)`
- `Confectionary` (note potential inconsistent spellings)
- `Units Sold`
- `Cost(£)`
- `Profit(£)`
- `Revenue(£)`


### 1.2 Type Conversion and Basic Cleaning

#### 1.2.1 Date Conversion

```python
df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
```

- **Check for any `NaT`:**

  ```python
  df["Date"].isna().sum()
  ```

- **If `NaT` exists**: print those rows and decide whether to **drop** them.  
  Likely safe to **drop a small number of invalid date rows** and **document** the decision.

#### 1.2.2 Numeric Columns

**Ensure numeric types for:**
- `Units Sold`
- `Cost(£)`
- `Profit(£)`
- `Revenue(£)`

```python
numeric_cols = ["Units Sold", "Cost(£)", "Profit(£)", "Revenue(£)"]
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")
```

- Check missing numeric values:

  ```python
  df[numeric_cols].isna().sum()
  ```

**Decision Point 1.2.A – Handling Missing Numeric Values**

- **Option 1 (Recommended):** Drop rows with missing numeric values if they are few relative to dataset size.
  ```python
  df = df.dropna(subset=numeric_cols)
  ```
- **Option 2:** Impute missing values (e.g., using mean/median per region).  
  This adds complexity and is usually unnecessary unless missingness is substantial.

**Best Practice:**  
Prefer **Option 1** and **document** this in the report as a simple, transparent approach.


### 1.3 Categorical Cleaning – `Country(UK)` and `Confectionary`

#### 1.3.1 Inspect Unique Values

```python
print(df["Country(UK)"].unique())
print(df["Confectionary"].unique())
```

#### 1.3.2 Normalise Confectionery Names

Create a normalised column `Confectionary_clean` that fixes spelling variants.

**Example mapping (extend if needed):**

```python
conf_mapping = {
    "Choclate Chunk": "Chocolate Chunk",
    "Chocolate Chunk": "Chocolate Chunk",
    "Caramel Nut": "Caramel Nut",
    "Caramel nut": "Caramel Nut",
    "Biscuit": "Biscuit",
    "Biscuit Nut": "Biscuit Nut",
    "Plain": "Plain",
    # Add any additional variants discovered
}

df["Confectionary_clean"] = df["Confectionary"].replace(conf_mapping)
```

**Best Practices:**
- After replacement, check for any remaining inconsistent entries:

  ```python
  print(df["Confectionary_clean"].unique())
  ```

- If some values remain unclear, manually map or **group them into an "Other"** category and document this in the report.


---

## 2. Feature Engineering

Goal: Create derived columns that allow for **profit margin** calculation and **time-based analysis**.

### 2.1 Time Components

```python
df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
df["MonthName"] = df["Date"].dt.strftime("%b")
df["Quarter"] = df["Date"].dt.to_period("Q").astype(str)
```


### 2.2 Financial Ratios and Per-Unit Metrics

```python
df["Profit_Margin"] = df["Profit(£)"] / df["Revenue(£)"]
df["Revenue_per_Unit"] = df["Revenue(£)"] / df["Units Sold"]
df["Cost_per_Unit"] = df["Cost(£)"] / df["Units Sold"]
df["Profit_per_Unit"] = df["Profit(£)"] / df["Units Sold"]
```

**Decision Point 2.2.A – Handling Division by Zero / NaNs**

- Before computing per-unit metrics, ensure `Units Sold > 0` or handle division safely:

  ```python
  df = df[df["Units Sold"] > 0]
  df["Profit_Margin"] = df["Profit(£)"] / df["Revenue(£)"]
  df["Revenue_per_Unit"] = df["Revenue(£)"] / df["Units Sold"]
  # etc.
  ```

- After computations, check for `inf` or `NaN` and handle (e.g., drop or fill with `np.nan`).

**Best Practice:**  
Drop rows where `Units Sold <= 0` and `Revenue(£) <= 0` if they are rare and make no practical sense in this business context. Document this assumption.


---

## 3. Exploratory Data Analysis (EDA)

> Focus should be “slight but sufficient” to show understanding of the dataset and support later visualisation decisions.


### 3.1 Overall Distribution of Key Metrics

**EDA objective:** understand general scale, spread, and skew of main metrics.

#### 3.1.1 Summary Statistics

```python
df[numeric_cols + ["Profit_Margin", "Revenue_per_Unit", "Profit_per_Unit"]].describe()
```

Save or display results and refer to them in the report later.

#### 3.1.2 Histograms / KDE Plots

For each key metric (`Units Sold`, `Revenue(£)`, `Profit(£)`, `Profit_Margin`):

```python
fig, axes = plt.subplots(2, 2, figsize=(10, 8))

sns.histplot(df["Units Sold"], ax=axes[0, 0], kde=True)
axes[0, 0].set_title("Distribution of Units Sold")

sns.histplot(df["Revenue(£)"], ax=axes[0, 1], kde=True)
axes[0, 1].set_title("Distribution of Revenue")

sns.histplot(df["Profit(£)"], ax=axes[1, 0], kde=True)
axes[1, 0].set_title("Distribution of Profit")

sns.histplot(df["Profit_Margin"], ax=axes[1, 1], kde=True)
axes[1, 1].set_title("Distribution of Profit Margin")

plt.tight_layout()
```

**Decision Point 3.1.A – Log Transform?**

- If distributions are highly skewed, **consider** a log transform for visual clarity:
  ```python
  df["log_Revenue"] = np.log1p(df["Revenue(£)"])
  ```
- **Option:** also plot histograms of log-transformed values.
- Only **do this if necessary** and clearly mark log scale plots, so non-technical readers are not confused.

**Best Practice:**  
If log transforms are used, keep them for EDA/technical understanding but prefer **non-log** charts for the final business-facing visuals, unless the log scale is clearly explained.


### 3.2 Regional Overview

#### 3.2.1 Aggregate by Region

```python
regional_summary = df.groupby("Country(UK)", as_index=False).agg({
    "Units Sold": "sum",
    "Revenue(£)": "sum",
    "Profit(£)": "sum"
})

regional_summary["Profit_Margin"] = (
    regional_summary["Profit(£)"] / regional_summary["Revenue(£)"]
)
```

#### 3.2.2 Static Visualisations

Create bar plots for:
- `Total Revenue by Region`
- `Total Profit by Region`
- `Average Profit Margin by Region`

Example (matplotlib/seaborn):

```python
plt.figure(figsize=(8, 5))
sns.barplot(data=regional_summary, x="Country(UK)", y="Revenue(£)")
plt.title("Total Revenue by Region")
plt.ylabel("Revenue (£)")
plt.xlabel("Region")
plt.tight_layout()
```

Repeat for Profit and Profit_Margin.

**Decision Point 3.2.B – Sorting Bars**

- **Option 1 (Recommended):** sort bars by value (descending), to improve perception.
  ```python
  regional_summary_sorted = regional_summary.sort_values("Profit(£)", ascending=False)
  ```
- **Option 2:** keep alphabetical order if aligning with external conventions.

**Best Practice:**  
Sort by value for most visual clarity; document this in the report as a design choice aiding non-technical stakeholders.


### 3.3 Confectionery Overview

#### 3.3.1 Aggregate by Confectionery Type

```python
conf_summary = df.groupby("Confectionary_clean", as_index=False).agg({
    "Units Sold": "sum",
    "Revenue(£)": "sum",
    "Profit(£)": "sum"
})

conf_summary["Profit_Margin"] = (
    conf_summary["Profit(£)"] / conf_summary["Revenue(£)"]
)
```

#### 3.3.2 Visualisations

- Horizontal bar chart: `Units Sold by Confectionary_clean`  
- Horizontal bar chart: `Profit(£) by Confectionary_clean`  
- Optional scatter: `Units Sold` vs `Profit(£)` per confectionery

Example:

```python
plt.figure(figsize=(8, 5))
sns.barplot(
    data=conf_summary.sort_values("Units Sold", ascending=False),
    y="Confectionary_clean",
    x="Units Sold"
)
plt.title("Total Units Sold by Confectionery Type")
plt.xlabel("Units Sold")
plt.ylabel("Confectionery")
plt.tight_layout()
```

**Best Practice:**  
Use **horizontal bars** for long category labels (confectionery names) to avoid overlapping text.


---

## 4. Region × Confectionery Analysis (Profit Margins)

Goal: identify **which confectionery has the largest/smallest profit margin regionally**.

### 4.1 Aggregate by Region and Confectionery

```python
region_conf = df.groupby(
    ["Country(UK)", "Confectionary_clean"], as_index=False
).agg({
    "Units Sold": "sum",
    "Revenue(£)": "sum",
    "Profit(£)": "sum"
})

region_conf["Profit_Margin"] = (
    region_conf["Profit(£)"] / region_conf["Revenue(£)"]
)
```


### 4.2 Heatmap of Profit Margin

Create pivot table for heatmap:

```python
pivot_margin = region_conf.pivot(
    index="Confectionary_clean",
    columns="Country(UK)",
    values="Profit_Margin"
)
```

Plot with seaborn:

```python
plt.figure(figsize=(8, 6))
sns.heatmap(pivot_margin, annot=True, fmt=".2f", cmap="viridis")
plt.title("Profit Margin by Confectionery and Region")
plt.xlabel("Region")
plt.ylabel("Confectionery")
plt.tight_layout()
```

**Best Practice:**
- Use **annot=True** so values are visible (helpful for non-technical readers).
- Choose a colourmap that is perceptually uniform (e.g., `viridis`) and friendly to colour-blind users.


### 4.3 Grouped Bar Charts (Optional / Complementary)

To complement the heatmap, consider **grouped bar charts** per confectionery or per region:

```python
sns.catplot(
    data=region_conf,
    x="Confectionary_clean",
    y="Profit_Margin",
    hue="Country(UK)",
    kind="bar",
    height=6,
    aspect=2
)
plt.title("Profit Margin by Region and Confectionery")
plt.xticks(rotation=45, ha="right")
```

**Decision Point 4.3.A – Use Heatmap Only vs Heatmap + Bars**

- **Option 1:** Heatmap only (simpler but dense).  
- **Option 2 (Recommended):** Heatmap + at least one grouped bar focusing on **top 3–4 confectionery types** to simplify the message.

**Best Practice:**  
Use **Option 2** and in the report explain that the grouped bar chart focuses on prioritised products for clearer decision-making.


---

## 5. Temporal Analysis – Peak Sales and Trends

Goal: determine **which region has peak sales over time** and explore seasonality.

### 5.1 Monthly Aggregation by Region

```python
monthly_region = df.groupby(
    [pd.Grouper(key="Date", freq="M"), "Country(UK)"],
    as_index=False
)["Units Sold"].sum()
```


### 5.2 Time Series Plot – Units Sold Over Time

```python
plt.figure(figsize=(12, 6))
sns.lineplot(
    data=monthly_region,
    x="Date",
    y="Units Sold",
    hue="Country(UK)"
)
plt.title("Monthly Units Sold by Region")
plt.xlabel("Date")
plt.ylabel("Units Sold")
plt.tight_layout()
```

**Best Practice:**
- Use different, clearly distinguishable colours per region.
- Ensure a legend is present and readable.


### 5.3 Identifying Peak Months per Region

Compute rank of monthly Units Sold within each region:

```python
monthly_region["Rank_in_region"] = monthly_region.groupby("Country(UK)")["Units Sold"].rank(
    method="first", ascending=False
)

# Get top N months per region
N = 3
peaks = monthly_region[monthly_region["Rank_in_region"] <= N]
```

Create a bar plot of peaks (per region) or a table.

**Decision Point 5.3.A – Top N Selection**

- **Option 1 (Recommended):** Use `N = 3` (top 3 months per region) – enough to highlight peaks without clutter.
- **Option 2:** Use `N = 5` if peaks are similar and need more differentiation.

**Best Practice:**  
Keep `N` small and consistent, and document this in the report as a pragmatic choice.


---

## 6. Interactive Dashboard – Technical Plan

> This is crucial for the assignment and grading (innovation, interactivity, decision support).  
> The following assumes **Streamlit** as the framework; Dash is an alternative.

### 6.1 Framework Choice

**Decision Point 6.1.A – Streamlit vs Dash**

- **Option 1 (Recommended): Streamlit**
  - Easier to set up and explain.
  - Simple script-based app.
- **Option 2: Dash**
  - More control and flexible layouts but more code.

**Proceed with Option 1 (Streamlit)** unless explicitly required otherwise.


### 6.2 Basic Streamlit App Structure

Create `dashboard/app.py` with the following skeleton:

```python
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. Load data
@st.cache_data
def load_data(path="data/confectionary.xlsx"):
    df = pd.read_excel(path)
    # Apply same cleaning and feature engineering as in the notebook
    # (Consider refactoring cleaning into a shared function/module.)
    return df

df = load_data()

# 2. Sidebar filters
st.sidebar.header("Filters")
# ... filters here ...

# 3. KPIs
# ... KPI cards ...

# 4. Charts
# ... region, confectionery, time-series charts ...
```

**Best Practice:**  
Refactor the **cleaning & feature engineering logic** into a reusable function or module (e.g., `src/data_prep.py`) to avoid duplicating code between notebook and dashboard.


### 6.3 Implementing Filters

In `app.py`, after loading and preparing `df` (with all engineered columns):

```python
st.sidebar.header("Filters")

regions = df["Country(UK)"].unique().tolist()
conf_types = df["Confectionary_clean"].unique().tolist()

selected_regions = st.sidebar.multiselect(
    "Select Regions",
    options=regions,
    default=regions
)

selected_conf = st.sidebar.multiselect(
    "Select Confectionery Types",
    options=conf_types,
    default=conf_types
)

min_date = df["Date"].min()
max_date = df["Date"].max()

date_range = st.sidebar.slider(
    "Select Date Range",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date)
)

# Apply filters
filtered_df = df[
    (df["Country(UK)"].isin(selected_regions)) &
    (df["Confectionary_clean"].isin(selected_conf)) &
    (df["Date"].between(date_range[0], date_range[1]))
]
```

**Best Practices:**
- Ensure filters always have sensible defaults (all regions, all confectionery, full date range).
- Guard against empty `filtered_df` (e.g., show message if no data after filtering).


### 6.4 KPI Cards

At the top of the main page, display key metrics.

```python
st.title("British Confectionary Council Dashboard")

st.subheader("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

total_units = int(filtered_df["Units Sold"].sum())
total_revenue = float(filtered_df["Revenue(£)"].sum())
total_profit = float(filtered_df["Profit(£)"].sum())
avg_margin = float(filtered_df["Profit_Margin"].mean())

col1.metric("Total Units Sold", f"{total_units:,}")
col2.metric("Total Revenue (£)", f"{total_revenue:,.0f}")
col3.metric("Total Profit (£)", f"{total_profit:,.0f}")
col4.metric("Avg Profit Margin", f"{avg_margin:.2%}")
```

**Best Practice:**  
Use thousands separators and percentage formatting for readability.


### 6.5 Region-Level Chart (Interactive)

```python
regional_filtered = filtered_df.groupby("Country(UK)", as_index=False).agg({
    "Units Sold": "sum",
    "Revenue(£)": "sum",
    "Profit(£)": "sum"
})

regional_filtered["Profit_Margin"] = (
    regional_filtered["Profit(£)"] / regional_filtered["Revenue(£)"]
)

fig_profit_region = px.bar(
    regional_filtered,
    x="Country(UK)",
    y="Profit(£)",
    title="Profit by Region",
    hover_data=["Revenue(£)", "Units Sold", "Profit_Margin"]
)

st.plotly_chart(fig_profit_region, use_container_width=True)
```

**Decision Point 6.5.A – Primary Metric in Region Chart**

- **Option 1 (Recommended):** Profit as y-axis; use Revenue & Units & Margin as hover data.
- **Option 2:** Revenue as y-axis; Profit as hover.

**Best Practice:**  
Use **Profit as main y-axis** because the assignment emphasises **profit margin and profit growth** for decision-making.


### 6.6 Confectionery-Level Chart (Interactive)

```python
conf_filtered = filtered_df.groupby("Confectionary_clean", as_index=False).agg({
    "Units Sold": "sum",
    "Revenue(£)": "sum",
    "Profit(£)": "sum"
})
conf_filtered["Profit_Margin"] = (
    conf_filtered["Profit(£)"] / conf_filtered["Revenue(£)"]
)

fig_conf = px.bar(
    conf_filtered.sort_values("Profit(£)", ascending=False),
    x="Confectionary_clean",
    y="Profit(£)",
    title="Profit by Confectionery Type",
    hover_data=["Revenue(£)", "Units Sold", "Profit_Margin"]
)
fig_conf.update_layout(xaxis_title="Confectionery Type", yaxis_title="Profit (£)")

st.plotly_chart(fig_conf, use_container_width=True)
```

**Best Practice:**  
Rotate x-axis labels if necessary for readability (`fig_conf.update_layout(xaxis_tickangle=-45)`).


### 6.7 Region × Confectionery Heatmap (Interactive)

```python
region_conf_filtered = filtered_df.groupby(
    ["Country(UK)", "Confectionary_clean"], as_index=False
).agg({
    "Units Sold": "sum",
    "Revenue(£)": "sum",
    "Profit(£)": "sum"
})
region_conf_filtered["Profit_Margin"] = (
    region_conf_filtered["Profit(£)"] / region_conf_filtered["Revenue(£)"]
)

pivot_heat = region_conf_filtered.pivot(
    index="Confectionary_clean",
    columns="Country(UK)",
    values="Profit_Margin"
)

fig_heat = px.imshow(
    pivot_heat,
    labels=dict(x="Region", y="Confectionery", color="Profit Margin"),
    x=pivot_heat.columns,
    y=pivot_heat.index,
    aspect="auto",
    title="Profit Margin by Region and Confectionery"
)

st.plotly_chart(fig_heat, use_container_width=True)
```

**Best Practice:**  
Ensure heatmap colour scale is intuitive (higher profit margin = more intense colour).


### 6.8 Time Series Panel

```python
monthly_filtered = filtered_df.groupby(
    [pd.Grouper(key="Date", freq="M"), "Country(UK)"],
    as_index=False
)["Units Sold"].sum()

fig_time = px.line(
    monthly_filtered,
    x="Date",
    y="Units Sold",
    color="Country(UK)",
    title="Monthly Units Sold by Region"
)

st.plotly_chart(fig_time, use_container_width=True)
```

**Decision Point 6.8.A – Time Granularity**

- **Option 1 (Recommended):** Monthly aggregation – balances smoothness and detail.
- **Option 2:** Quarterly aggregation if monthly is too noisy.

**Best Practice:**  
Use **monthly** by default and mention that the slider can restrict to narrower periods if needed.


---

## 7. Support for Report and Grading Criteria

### 7.1 Traceability: Label and Save Key Figures

For each important visualisation used in the report:

- Assign a **figure identifier** (e.g., `"fig_2_1_profit_by_region.png"`).
- Save figures to a folder, e.g., `figures/`:

```python
plt.savefig("figures/fig_2_1_profit_by_region.png", bbox_inches="tight")
```

This makes it easy to insert into the Word document and reference as **Figure 2.1** etc.

### 7.2 Documenting Decisions in Code

Add **short, clear comments** in the code wherever a decision point exists, e.g.:

```python
# Decision: drop rows with missing numeric values because they represent <1% of data
# and imputing would add complexity without clear benefit.
df = df.dropna(subset=numeric_cols)
```

These comments can be directly translated into Task 2 text, showing critical reflection and awareness of limitations.


---

## 8. Optional Enhancements (If Time and Scope Allow)

> These are **not required**, but can improve impression if implemented cleanly and briefly.

### 8.1 Seaborn Pairplot (Quick Multivariate Glimpse)

```python
sns.pairplot(df[["Units Sold", "Revenue(£)", "Profit(£)", "Profit_Margin"]])
```

Use only for your understanding, not necessarily in the final report (pairplots can overwhelm non-technical readers).


### 8.2 KPI Comparison Between Regions

Implement a small table in Streamlit showing **top region by Profit**, **top region by Profit Margin**, etc.

```python
top_profit_region = regional_filtered.loc[regional_filtered["Profit(£)"].idxmax(), "Country(UK)"]
top_margin_region = regional_filtered.loc[regional_filtered["Profit_Margin"].idxmax(), "Country(UK)"]
```

Display with `st.write()` or `st.table()`.


---

## 9. Summary of Execution Order (High-Level Checklist)

1. **Set up project structure and environment.**
2. **Load data** from `confectionary.xlsx` into a DataFrame.
3. **Clean and preprocess data:**
   - Convert `Date` to datetime.
   - Ensure numeric types for financial columns.
   - Handle missing values (prefer dropping small amounts).
   - Normalise `Confectionary` names into `Confectionary_clean`.
4. **Feature engineering:**
   - Add `Year`, `Month`, `MonthName`, `Quarter`.
   - Compute `Profit_Margin`, `Revenue_per_Unit`, `Profit_per_Unit`, etc.
5. **EDA (slight focus):**
   - Summary statistics for key metrics.
   - Distributions (histograms/KDE).
   - Regional and confectionery aggregations.
6. **Analytical visualisations:**
   - Region-level: revenue, profit, profit margin.
   - Confectionery-level: volume vs. profit vs. margin.
   - Region × Confectionery: heatmap + possibly grouped bars.
   - Temporal trends: monthly Units Sold by region, peak detection.
7. **Build interactive dashboard (Streamlit):**
   - Implement filters for region, confectionery, date range.
   - Implement KPI cards.
   - Implement interactive charts: region-level, product-level, heatmap, time series.
8. **Save key figures** to `figures/` for inclusion in Word report.
9. **Ensure code is clean and well-commented** for Task 1 appendix and Task 2 reference.
10. **Use the notebook / code comments** as raw material for the written justification (Task 2).

This plan is now ready for a coding agent to execute step by step, making informed decisions at specified branches while staying faithful to the assignment guidelines and grading criteria.
