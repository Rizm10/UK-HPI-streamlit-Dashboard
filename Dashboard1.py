# -*- coding: utf-8 -*-
"""Untitled17.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/12wVEmHcua2qgvOLbC0vkIAQCH5xRBcYD
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
st.set_page_config(page_title="UK Housing Dashboard", layout="wide")
full_path = 'UK-HPI-full-file-2025-02.csv'
sample_path = 'UK HPI sample (git).csv'

if os.path.exists(full_path):
    df = pd.read_csv(full_path)
    st.success("Loaded full dataset.")
elif os.path.exists(sample_path):
    df = pd.read_csv(sample_path)
    st.warning("Loaded sample dataset (full version not found).")
else:
    st.error("No dataset found. Please add one to the root directory.")

# Preprocessing
df['Date'] = pd.to_datetime(df['Date'], errors='coerce', dayfirst=True)
df = df.dropna(subset=['Date'])  # Drop rows with invalid dates
df = df.sort_values(by='Date')

# Sidebar config
st.title("UK Housing Price Dashboard")
st.markdown("Explore the UK Housing Price Index Dashboard")
st.sidebar.header("Filters")

# Region filter
selected_region = st.sidebar.selectbox('Select Region', df['RegionName'].unique())
filtered_df = df[df['RegionName'] == selected_region]

# Region multiselect
regions = st.multiselect("Select regions", options=df['RegionName'].unique(), default=["London", "South East"])
subset_df = df[df['RegionName'].isin(regions)]

# Columns layout
col1, col2 = st.columns(2)

# Average Price Trend
with col1:
    st.subheader('Average House Price Over Time')
    fig1, ax1 = plt.subplots(figsize=(7, 5))
    for region in regions:
        region_data = subset_df[subset_df['RegionName'] == region]
        ax1.plot(region_data['Date'], region_data['AveragePrice'], label=region)
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Average Price')
    ax1.set_title('Average Price Trend')
    ax1.legend()
    ax1.grid(True)
    st.pyplot(fig1)

# Sales Volume Trend
with col2:
    st.subheader(f'Sales Volume Over Time - {selected_region}')
    region_data = filtered_df.sort_values(by='Date')
    fig2, ax2 = plt.subplots(figsize=(7, 5))
    ax2.plot(region_data['Date'], region_data['SalesVolume'], label=selected_region, color='orange')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Sales Volume')
    ax2.set_title('Sales Volume Trend')
    ax2.legend()
    ax2.grid(True)
    st.pyplot(fig2)

# Property Price Distribution Section
st.markdown("---")
st.subheader("Distribution of Property Prices")

# Reshape for long format
price_cols = {
    'Detached': 'DetachedPrice',
    'SemiDetached': 'SemiDetachedPrice',
    'Terraced': 'TerracedPrice',
    'Flat': 'FlatPrice'
}

long_df = pd.melt(
    df,
    id_vars=['Date', 'RegionName'],
    value_vars=price_cols.values(),
    var_name='Type',
    value_name='Price'
)

type_map = {v: k for k, v in price_cols.items()}
long_df['Type'] = long_df['Type'].map(type_map)

# View mode
view_mode = st.radio("View Mode:", options=["All Property Types", "Single Property Type"])

if view_mode == "All Property Types":
    st.subheader("Distribution of Average Prices by Property Type (All Types)")
    fig3, ax3 = plt.subplots(figsize=(12, 5))
    sns.histplot(data=long_df, x='Price', hue='Type', multiple='stack', bins=30, ax=ax3)
    ax3.set_xlabel("Average Price")
    ax3.set_ylabel("Frequency")
    ax3.grid(True)
    st.pyplot(fig3)
else:
    selected_type = st.selectbox('Select Property Type', options=long_df['Type'].unique())
    filtered_type_df = long_df[long_df['Type'] == selected_type]

    st.subheader(f"Distribution of Average Prices – {selected_type}")
    fig4, ax4 = plt.subplots(figsize=(12, 5))
    sns.histplot(data=filtered_type_df, x='Price', bins=30, color='teal', ax=ax4)
    ax4.set_xlabel("Average Price")
    ax4.set_ylabel("Frequency")
    ax4.grid(True)
    st.pyplot(fig4)

# Final trend plot (full width)
st.subheader('Average House Price Trend for Selected Regions')
fig5, ax5 = plt.subplots(figsize=(15, 8))
for region in regions:
    region_data = subset_df[subset_df['RegionName'] == region]
    ax5.plot(region_data['Date'], region_data['AveragePrice'], label=region)
ax5.set_xlabel('Date')
ax5.set_ylabel('Average Price')
ax5.set_title('Average House Price Over Time by Region')
ax5.legend()
ax5.grid(True)
st.pyplot(fig5)

# Outlier Detection (IQR)
Q1 = subset_df['AveragePrice'].quantile(0.25)
Q3 = subset_df['AveragePrice'].quantile(0.75)
IQR = Q3 - Q1
outliers = subset_df[(subset_df['AveragePrice'] < Q1 - 1.5 * IQR) | (subset_df['AveragePrice'] > Q3 + 1.5 * IQR)]

if not outliers.empty:
    st.markdown("### Potential Outliers in Average Price")
    st.dataframe(outliers[['Date', 'RegionName', 'AveragePrice']].head(10))
