import streamlit as st
import pandas as pd

from utils import load_all_data, filter_data, create_line_plot, create_boxplot

# ======================
# CONFIG
# ======================
st.set_page_config(
    page_title="African Climate Dashboard",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 African Climate Trend Analysis Dashboard")
st.markdown("COP32 Climate Evidence Dashboard")

# ======================
# LOAD DATA
# ======================
df = load_all_data()

if df.empty:
    st.error("No data loaded. Check your /data folder.")
    st.stop()

df.columns = df.columns.str.strip()
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# ======================
# SIDEBAR FILTERS
# ======================
st.sidebar.header("Filters")

countries = st.sidebar.multiselect(
    "Select Countries",
    df['Country'].unique(),
    default=df['Country'].unique()
)

year_range = st.sidebar.slider(
    "Select Year Range",
    int(df['Year'].min()),
    int(df['Year'].max()),
    (int(df['Year'].min()), int(df['Year'].max()))
)

# ======================
# VARIABLE SELECTOR (FIXED)
# ======================
var_map = {
    "Temperature (T2M)": "T2M",
    "Rainfall (PRECTOTCORR)": "PRECTOTCORR",
    "Humidity (RH2M)": "RH2M",
    "Wind Speed (WS2M)": "WS2M"
}

available_vars = {
    k: v for k, v in var_map.items() if v in df.columns
}

variable = st.sidebar.selectbox(
    "Select Variable",
    list(available_vars.keys())
)

selected_var = available_vars[variable]

# ======================
# FILTER DATA
# ======================
filtered_df = filter_data(df, countries, year_range)

# ======================
# METRICS
# ======================
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Countries", filtered_df['Country'].nunique())

with col2:
    st.metric("Years", f"{year_range[0]} - {year_range[1]}")

with col3:
    if selected_var in filtered_df.columns:
        st.metric(f"Avg {variable}", f"{filtered_df[selected_var].mean():.2f}")
    else:
        st.metric(f"Avg {variable}", "N/A")

# ======================
# TABS
# ======================
tab1, tab2 = st.tabs(["Trends", "Distribution"])

# ======================
# TAB 1 - TREND (FIXED)
# ======================
with tab1:
    st.subheader("Trend Analysis")

    fig = create_line_plot(filtered_df, selected_var)

    if fig:
        st.pyplot(fig)
    else:
        st.warning(f"{variable} not available for trend analysis")

# ======================
# TAB 2 - DISTRIBUTION (FIXED)
# ======================
with tab2:
    st.subheader("Distribution Analysis")

    fig = create_boxplot(filtered_df, selected_var)

    if fig:
        st.pyplot(fig)
    else:
        st.warning(f"{variable} not available for distribution")

# ======================
# DOWNLOAD
# ======================
st.sidebar.markdown("---")

if st.sidebar.button("Download Data"):
    csv = filtered_df.to_csv(index=False)
    st.sidebar.download_button(
        "Download CSV",
        csv,
        "climate_data.csv",
        "text/csv"
    )