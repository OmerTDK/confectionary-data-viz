#!/usr/bin/env python3
"""
British Confectionary Council Interactive Dashboard
Built with Streamlit for data-driven decision making
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

# Add src directory to path for imports
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
src_dir = os.path.join(parent_dir, 'src')
sys.path.insert(0, src_dir)

try:
    from data_prep import prepare_data, get_regional_summary, get_product_summary, get_regional_product_matrix, get_monthly_trends
except ImportError:
    st.error("❌ Could not import data_prep module. Please ensure you're running from the project root directory.")
    st.stop()


# Set page configuration
st.set_page_config(
    page_title="British Confectionary Council Dashboard",
    page_icon="🍫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 0.25rem solid #ff4b4b;
    }
    .sidebar-header {
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    """Load and prepare data with caching"""
    try:
        # Look for data file in parent directory (project root)
        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        data_file = os.path.join(parent_dir, "confectionary.xlsx")

        df = prepare_data(data_file)
        return df
    except FileNotFoundError:
        st.error("❌ Data file 'confectionary.xlsx' not found. Please ensure it's in the project root directory.")
        st.stop()
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        st.stop()


def main():
    """Main dashboard application"""

    # Load data
    df = load_data()

    # Title and description
    st.title("🍫 British Confectionary Council Dashboard")
    st.markdown("*Interactive analytics for UK confectionary sales performance (2000-2005)*")

    # Sidebar filters
    st.sidebar.markdown('<div class="sidebar-header">🎛️ Filters</div>', unsafe_allow_html=True)

    # Region filter
    regions = sorted(df["Country(UK)"].unique())
    selected_regions = st.sidebar.multiselect(
        "Select Regions",
        options=regions,
        default=regions,
        help="Choose regions to analyze"
    )

    # Product filter
    products = sorted(df["Confectionary_clean"].unique())
    selected_products = st.sidebar.multiselect(
        "Select Confectionery Types",
        options=products,
        default=products,
        help="Choose product types to analyze"
    )

    # Date range filter
    min_date = df["Date"].min().date()
    max_date = df["Date"].max().date()
    date_range = st.sidebar.slider(
        "Select Date Range",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date),
        help="Filter data by date range"
    )

    # Apply filters
    filtered_df = df[
        (df["Country(UK)"].isin(selected_regions)) &
        (df["Confectionary_clean"].isin(selected_products)) &
        (df["Date"].dt.date >= date_range[0]) &
        (df["Date"].dt.date <= date_range[1])
    ]

    # Check if filtered data is empty
    if filtered_df.empty:
        st.warning("⚠️ No data matches your current filter selections. Please adjust your filters.")
        return

    # KPI Cards
    st.subheader("📊 Key Performance Indicators")

    col1, col2, col3, col4 = st.columns(4)

    total_units = int(filtered_df["Units Sold"].sum())
    total_revenue = float(filtered_df["Revenue(£)"].sum())
    total_profit = float(filtered_df["Profit(£)"].sum())
    avg_margin = float(filtered_df["Profit_Margin"].mean())

    with col1:
        st.metric("Total Units Sold", f"{total_units:,}")

    with col2:
        st.metric("Total Revenue (£)", f"£{total_revenue:,.0f}")

    with col3:
        st.metric("Total Profit (£)", f"£{total_profit:,.0f}")

    with col4:
        st.metric("Avg Profit Margin", f"{avg_margin:.1%}")

    # Charts section
    st.markdown("---")

    # Regional Performance Chart
    st.subheader("🏆 Regional Performance")

    regional_filtered = get_regional_summary(filtered_df)

    if not regional_filtered.empty:
        regional_filtered = regional_filtered.sort_values("Profit(£)", ascending=False)

        fig_profit_region = px.bar(
            regional_filtered,
            x="Country(UK)",
            y="Profit(£)",
            title="Profit by Region",
            labels={"Profit(£)": "Profit (£)", "Country(UK)": "Region"},
            color="Profit(£)",
            color_continuous_scale="viridis"
        )
        fig_profit_region.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_profit_region, use_container_width=True)
    else:
        st.info("No regional data available for current filters")

    # Product Performance Chart
    st.subheader("🍬 Product Performance")

    conf_filtered = get_product_summary(filtered_df)

    if not conf_filtered.empty:
        conf_filtered = conf_filtered.sort_values("Profit(£)", ascending=False)

        fig_conf = px.bar(
            conf_filtered,
            x="Confectionary_clean",
            y="Profit(£)",
            title="Profit by Confectionery Type",
            labels={"Profit(£)": "Profit (£)", "Confectionary_clean": "Product Type"},
            color="Profit(£)",
            color_continuous_scale="plasma"
        )
        fig_conf.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_conf, use_container_width=True)
    else:
        st.info("No product data available for current filters")

    # Region × Product Heatmap
    st.subheader("🔍 Regional Product Performance Matrix")

    region_conf_filtered = get_regional_product_matrix(filtered_df)

    if not region_conf_filtered.empty:
        # Create pivot table for heatmap
        pivot_heat = region_conf_filtered.pivot(
            index="Confectionary_clean",
            columns="Country(UK)",
            values="Profit_Margin"
        )

        # Create heatmap
        fig_heat = px.imshow(
            pivot_heat,
            labels=dict(x="Region", y="Product", color="Profit Margin"),
            x=pivot_heat.columns,
            y=pivot_heat.index,
            aspect="auto",
            title="Profit Margin by Region and Product",
            color_continuous_scale="RdYlGn"
        )
        fig_heat.update_layout(
            xaxis_title="Region",
            yaxis_title="Confectionery Type"
        )
        st.plotly_chart(fig_heat, use_container_width=True)

        # Add interpretation
        st.markdown("""
        **💡 Interpretation:**
        - Darker green = Higher profit margins
        - Darker red = Lower profit margins
        - Use this matrix to identify regional strengths and opportunities
        """)
    else:
        st.info("No cross-regional data available for current filters")

    # Time Series Panel
    st.subheader("📈 Sales Trends Over Time")

    monthly_filtered = get_monthly_trends(filtered_df)

    if not monthly_filtered.empty:
        fig_time = px.line(
            monthly_filtered,
            x="Date",
            y="Units Sold",
            color="Country(UK)",
            title="Monthly Units Sold by Region",
            labels={"Units Sold": "Units Sold", "Date": "Date", "Country(UK)": "Region"}
        )
        fig_time.update_layout(
            xaxis_title="Date",
            yaxis_title="Units Sold"
        )
        st.plotly_chart(fig_time, use_container_width=True)
    else:
        st.info("No time series data available for current filters")

    # Footer
    st.markdown("---")
    st.markdown("""
    **📋 About This Dashboard**
    - Built with Streamlit and Plotly for interactive data exploration
    - Data covers UK confectionary sales from 2000-2005
    - Use the sidebar filters to explore different aspects of the business
    - All metrics update dynamically based on your filter selections
    """)

    # Add some spacing
    st.markdown("<br>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
