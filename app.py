
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# --- Page Config ---
st.set_page_config(page_title="UK Housing Dashboard", layout="wide")

# --- Logo + Title in Sidebar ---
st.sidebar.image("gov_logo.png", width=100)
st.sidebar.markdown("## UK Housing Dashboard")
st.sidebar.markdown("---")

# --- Load Data ---
df = pd.read_csv('UK-HPI-full-file-2025-02.csv')
df['Date'] = pd.to_datetime(df['Date'], errors='coerce', dayfirst=True)
df = df.dropna(subset=['Date']).sort_values(by='Date')

# --- Filters ---
st.sidebar.header("Filters")
regions = st.sidebar.multiselect("Select Region(s)", options=df['RegionName'].unique(), default=["London", "South East"])
property_types = st.sidebar.multiselect("Select Property Type(s)", options=['Detached', 'SemiDetached', 'Terraced', 'Flat'], default=['Detached', 'Flat'])
date_range = st.sidebar.date_input("Select Date Range", [df['Date'].min(), df['Date'].max()])
price_min, price_max = st.sidebar.slider("Select Price Range", int(df['AveragePrice'].min()), int(df['AveragePrice'].max()), (int(df['AveragePrice'].min()), int(df['AveragePrice'].max())))

# --- Filtered DF ---
price_cols = {
    'Detached': 'DetachedPrice',
    'SemiDetached': 'SemiDetachedPrice',
    'Terraced': 'TerracedPrice',
    'Flat': 'FlatPrice'
}

filtered_df = df[
    (df['RegionName'].isin(regions)) &
    (df['Date'] >= pd.to_datetime(date_range[0])) &
    (df['Date'] <= pd.to_datetime(date_range[1])) &
    (df['AveragePrice'] >= price_min) &
    (df['AveragePrice'] <= price_max)
]

# --- Info Section ---
st.markdown("### 📌 About This Dashboard")
st.markdown("This dashboard visualizes UK Housing Price Index trends with region, date, and property type filtering. Built with Streamlit.")

# --- KPI Metrics ---
latest_date = filtered_df['Date'].max()
latest_df = filtered_df[filtered_df['Date'] == latest_date]
latest_price = latest_df['AveragePrice'].mean()
latest_volume = latest_df['SalesVolume'].sum()
prev_month = latest_date - pd.DateOffset(months=1)
prev_df = filtered_df[filtered_df['Date'] == prev_month]
prev_price = prev_df['AveragePrice'].mean() if not prev_df.empty else np.nan
pct_change = ((latest_price - prev_price) / prev_price) * 100 if not np.isnan(prev_price) else "N/A"

st.markdown("### 💡 Key Metrics")
col1, col2, col3, col4 = st.columns([1,1,1,1])
col1.metric("Latest Avg Price", f"£{latest_price:,.0f}")
col2.metric("Sales Volume", f"{int(latest_volume):,}")
col3.metric("MoM Change", f"{pct_change:.2f}%" if not isinstance(pct_change, str) else "N/A")
col4.metric("Last Updated", latest_date.strftime("%b %Y"))

# --- Charts Grid ---
st.markdown("### 📈 Data Visualizations")
c1, c2 = st.columns(2)

with c1:
    st.subheader("Monthly % Change in Avg Price")
    filtered_df = filtered_df.sort_values(by='Date')
    filtered_df['PctChange'] = filtered_df.groupby('RegionName')['AveragePrice'].pct_change() * 100
    fig1, ax1 = plt.subplots(figsize=(7, 4))
    for region in regions:
        region_data = filtered_df[filtered_df['RegionName'] == region]
        ax1.plot(region_data['Date'], region_data['PctChange'], label=region)
    ax1.axhline(0, color='gray', linestyle='--')
    ax1.set_ylabel("% Change")
    ax1.set_title("MoM % Change")
    ax1.legend()
    ax1.grid(True)
    st.pyplot(fig1)

with c2:
    st.subheader("Average Price Trend")
    fig2, ax2 = plt.subplots(figsize=(7, 4))
    for region in regions:
        region_data = filtered_df[filtered_df['RegionName'] == region]
        ax2.plot(region_data['Date'], region_data['AveragePrice'], label=region)
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Avg Price")
    ax2.set_title("House Prices Over Time")
    ax2.legend()
    ax2.grid(True)
    st.pyplot(fig2)

c3, c4 = st.columns(2)
with c3:
    st.subheader("Price Trend by Property Type")
    type_df = df[
        (df['RegionName'].isin(regions)) &
        (df['Date'] >= pd.to_datetime(date_range[0])) &
        (df['Date'] <= pd.to_datetime(date_range[1]))
    ]
    fig3, ax3 = plt.subplots(figsize=(7, 4))
    for p_type in property_types:
        ax3.plot(type_df['Date'], type_df[price_cols[p_type]], label=p_type)
    ax3.set_xlabel("Date")
    ax3.set_ylabel("Price")
    ax3.set_title("Avg Price by Type")
    ax3.legend()
    ax3.grid(True)
    st.pyplot(fig3)

with c4:
    st.subheader("Price Distribution")
    long_df = pd.melt(
        df[df['RegionName'].isin(regions)],
        id_vars=['Date', 'RegionName'],
        value_vars=[price_cols[p] for p in property_types],
        var_name='Type', value_name='Price'
    )
    type_map = {v: k for k, v in price_cols.items()}
    long_df['Type'] = long_df['Type'].map(type_map)
    fig4, ax4 = plt.subplots(figsize=(7, 4))
    sns.histplot(data=long_df, x='Price', hue='Type', multiple='stack', bins=30, ax=ax4)
    ax4.set_xlabel("Price")
    ax4.set_title("Price Distribution")
    ax4.grid(True)
    st.pyplot(fig4)

# --- Outliers ---
Q1 = filtered_df['AveragePrice'].quantile(0.25)
Q3 = filtered_df['AveragePrice'].quantile(0.75)
IQR = Q3 - Q1
outliers = filtered_df[
    (filtered_df['AveragePrice'] < Q1 - 1.5 * IQR) |
    (filtered_df['AveragePrice'] > Q3 + 1.5 * IQR)
]

if not outliers.empty:
    with st.expander("📌 View Outliers"):
        st.dataframe(outliers[['Date', 'RegionName', 'AveragePrice']].head(10))
