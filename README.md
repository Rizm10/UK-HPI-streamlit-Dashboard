# UK-HPI-streamlit-Dashboard

## UK Housing Price Dashboard (Streamlit)

This project is an interactive dashboard built with **Streamlit** to explore the UK House Price Index (HPI). It includes filtering by region, time-based trends, and property type distributions.

---


⸻

🔍 Features
	•	✅ Clean KPI Display
Displays latest average price, sales volume, month-over-month % change, and last update timestamp in a professional layout.
	•	📈 Price Trends Over Time
Visualizes average house prices across selected regions, along with % monthly changes to spot market shifts.
	•	🏘️ Property Type Analysis
Tracks pricing trends for Detached, Semi-Detached, Terraced, and Flat property types.
	•	🌍 Interactive Filters
Dynamic filtering by region(s), property type(s), date range, and price range directly from the sidebar.
	•	📊 Price Distribution Histogram
Stacked histogram showing the distribution of house prices by property type.
	•	⚠️ Outlier Detection
Automatically identifies and displays potential outliers in average prices using IQR method.
	•	🧹 Responsive Layout
Clean chart alignment and spacing for readability — styled with GOV.UK-like aesthetics and dashboard UX principles.
	•	⚙️ Fully Streamlit-Based
Built using Python, Pandas, Matplotlib, Seaborn, and Streamlit — no JavaScript or external backend required.
	•	📦 Demo Dataset Included
Uses a real UK Housing Price Index sample dataset for easy testing and demonstration.
	•	☁️ Deployed on Streamlit Cloud
One-click launch with ngrok or Streamlit Cloud — fully Colab-compatible.

## Live Dashboard

Run instantly in your browser — no setup required:  
**https://uk-hpi-app-dashboard-4hwcfrlqhrjjv9ojaqc6tv.streamlit.app**

---

## Dataset Information

- **Primary Dataset**: `UK-HPI-full-file-2025-02.csv` (UK Government HPI)
- A **sample version** (`UK HPI sample (git).csv`) is included to ensure compatibility with GitHub and Streamlit Cloud.
- To run the full dashboard locally, download the complete dataset from the [official UK HPI portal](https://www.gov.uk/government/statistical-data-sets/uk-house-price-index-data-downloads-february-2025) and place it in the project root.

---

## Running Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/rizm10/uk-hpi-streamlit-dashboard.git
   cd uk-hpi-streamlit-dashboard

   Note: A sample dataset is included. For full functionality, place the official UK HPI dataset in the root directory.
