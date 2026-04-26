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

---


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
```
### 2. Missing Value Handling

- There was no -999 data value in the given dataset
- No dupliates were found
```python
df.duplicated().sum()
```
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
```
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

### 10. Cleaned Data Export

```python
df.to_csv('../data/<country>_clean.csv')
```

## Tools & Libraries Used

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
```
## Challenges Encountered & Solutions

| Challenge | Solution |
|----------|--------|
| Git merge conflicts | Used `git checkout --theirs` and force checkout method |
| No -999 values found | Standard missing value handling applied |
| Skewed rainfall distribution | Applied log scale for histogram visualization |
| Diverged branches | Used `git push --force` after verification |

---

## Key Findings Summary

| Country | Temperature Trend | Rainfall Peak | Key Risk |
|--------|------------------|--------------|----------|
| Ethiopia | Warming | 446.6 mm | Humid heatwaves + floods |
| Kenya | Warming | 213.9 mm | Bimodal rainfall variability |
| Sudan | Stable/Warming | 206.0 mm | Extreme heat + flash floods |
| Tanzania | Warming | Data pending | Annual aggregation needed |
| Nigeria | Slight warming | Data pending | Annual aggregation needed |

## References

- NASA POWER Climate Data  
- WMO State of the Climate in Africa (2024)  
- World Bank Climate Risk Country Profiles  