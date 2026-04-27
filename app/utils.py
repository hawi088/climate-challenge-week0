import pandas as pd
import os
import matplotlib.pyplot as plt
import streamlit as st


@st.cache_data
def load_all_data():
    """Load all cleaned country data"""

    countries = ['ethiopia', 'kenya', 'sudan', 'tanzania', 'nigeria']
    dfs = []

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    DATA_DIR = os.path.join(BASE_DIR, "data")

    for country in countries:
        try:
            file_path = os.path.join(DATA_DIR, f"{country}_clean.csv")

            df = pd.read_csv(file_path)

            # clean column names (VERY IMPORTANT)
            df.columns = df.columns.str.strip()

            df['Country'] = country.capitalize()

            dfs.append(df)

        except FileNotFoundError:
            print(f"Missing file: {file_path}")

    if len(dfs) == 0:
        return pd.DataFrame()

    return pd.concat(dfs, ignore_index=True)


def filter_data(df, countries, year_range):
    """Filter dataset"""

    df = df.copy()

    df = df[df['Country'].isin(countries)]
    df = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]

    return df


def create_line_plot(df, variable):
    """Clean, smoothed climate trend plot"""

    if variable not in df.columns:
        return None

    df = df.copy()
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.to_period('M').dt.to_timestamp()

    # monthly aggregation
    monthly = df.groupby(['Country', 'Month'])[variable].mean().reset_index()

    # smoothing
    monthly['Smoothed'] = monthly.groupby('Country')[variable].transform(
        lambda x: x.rolling(window=3, min_periods=1).mean()
    )

    fig, ax = plt.subplots(figsize=(12, 6))

    for country in monthly['Country'].unique():
        data = monthly[monthly['Country'] == country]

        ax.plot(
            data['Month'],
            data['Smoothed'],
            linewidth=2.5,
            alpha=0.9,
            label=country
        )

    ax.set_title(f"{variable} Trend (Monthly Smoothed)")
    ax.set_xlabel("Date")
    ax.set_ylabel(variable)

    ax.grid(True, alpha=0.2)
    ax.legend(frameon=False)

    return fig


def create_boxplot(df, variable):
    """Generic boxplot for any variable"""

    if variable not in df.columns:
        return None

    fig, ax = plt.subplots(figsize=(10, 6))

    countries = df['Country'].unique()

    data = [
        df[df['Country'] == c][variable].dropna()
        for c in countries
    ]

    ax.boxplot(data, labels=countries)

    ax.set_title(f"{variable} Distribution by Country")
    ax.set_ylabel(variable)

    if variable == "PRECTOTCORR":
        ax.set_yscale("log")

    return fig