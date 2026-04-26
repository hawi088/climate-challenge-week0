# Week 0 Interim Report
## Climate Challenge: African Climate Trend Analysis

**Name:** Hawi Chala  
**Date:** April 26, 2026  
**GitHub Repository:** https://github.com/hawi088/climate-challenge-week0

---

## Task 1: Git & Environment Setup

### Summary
Successfully completed the Git and environment setup following the challenge requirements.

### Conventional Commits Used

- `init: add .gitignore`
- `chore: add requirements.txt`
- `ci: add GitHub Actions workflow`
- `feat: add Ethiopia EDA`
- `feat: add Kenya EDA`
- `feat: add Sudan EDA`
- `feat: add Tanzania EDA


### CI/CD Status

GitHub Actions workflow runs:

```bash
pip install -r requirements.txt
```
## Task 2: Data profiling, cleaning and EDA

### 1. Data Loading & Date Parsing

```python
import pandas as pd

# Load CSV
df = pd.read_csv('../data/<country>.csv')

# Add country column
df['Country'] = '<Country>'

# Convert YEAR and DOY to datetime
df['Date'] = pd.to_datetime(df['YEAR'] * 1000 + df['DOY'], format='%Y%j')

# Extract month and year
df['Month'] = df['Date'].dt.month
df['Year'] = df['Date'].dt.year

### 2. Missing Value Handling

- There was no -999 data value in the given dataset
- No dupliates were found
```python
df.duplicated().sum()

### 3. Data Quality Assessment

After cleaning:

- **Shape:** ~4,108 rows × 15 columns  
- **Missing values:** No column exceeded 5% missing  
- **Duplicates:** None found  

---

### 4. Outlier Detection

- **Method:** Z-score (|Z| > 3)

- **Variables analyzed:**
  - T2M, T2M_MAX, T2M_MIN  
  - PRECTOTCORR  
  - RH2M  
  - WS2M, WS2M_MAX  

- **Decision:** Outliers were retained  

- **Reason:**  
  Extreme climate values (e.g., heatwaves, heavy rainfall) are real and essential for climate risk analysis.

#### Example: Ethiopia Outliers

| Variable | Outliers |
|----------|---------|
| T2M | 12 |
| T2M_MAX | 8 |
| T2M_MIN | 15 |
| PRECTOTCORR | 45 |
| RH2M | 10 |
| WS2M | 22 |
| WS2M_MAX | 25 |

**Total rows with outliers:** 137 (3.33%)

---

### 5. Summary Statistics

Used:

```python
df.describe()

### 6. Time Series Analysis

| Plot Type | Purpose | Key Finding |
|----------|--------|------------|
| Monthly average T2M (line) | Temperature trends | All countries show warming |
| Monthly PRECTOTCORR (bar) | Rainfall patterns | Extreme rainfall events (200–446 mm) observed |

---

### 7. Correlation & Relationship Analysis

- Heatmaps for all numeric variables  

- Scatter plots:
  - T2M vs RH2M  
  - T2M_RANGE vs WS2M  

**Strong correlations:**

- T2M ↔ T2M_MAX (~0.85–0.95)  
- T2M ↔ T2M_MIN (~0.72–0.92)  
- RH2M ↔ PRECTOTCORR (~0.40–0.45)  

---

### 8. Distribution Analysis

- Histogram of PRECTOTCORR (log scale applied)

**Insight:**

- Most days have low rainfall  
- Rare extreme events (200–446 mm) exist  

---

### 9. Multivariate Analysis

- Bubble chart:
  - **X-axis:** T2M  
  - **Y-axis:** RH2M  
  - **Size:** PRECTOTCORR  

**Insight:**

- Identifies compound risks:
  - Hot + dry → drought  
  - Warm + humid → flood risk  