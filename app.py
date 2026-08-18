import streamlit as st
import pandas as pd
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

CLEANED_FILE = Path("data/processed/cleaned_data.csv")


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="E-Commerce Sales Dashboard",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    df = pd.read_csv(CLEANED_FILE)

    df["invoicedate"] = pd.to_datetime(
        df["invoicedate"],
        errors="coerce"
    )

    return df


df = load_data()


# ============================================================
# TITLE
# ============================================================

st.title("📊 E-Commerce Sales Analysis")

st.write(
    "Interactive analysis of UK e-commerce sales data."
)


# ============================================================
# KEY PERFORMANCE INDICATORS
# ============================================================

total_revenue = df["total_sales"].sum()

total_orders = df["invoiceno"].nunique()

total_customers = df["customerid"].nunique()

total_quantity = df["quantity"].sum()

order_revenue = (
    df.groupby("invoiceno")["total_sales"]
    .sum()
)

average_order_value = order_revenue.mean()


# ============================================================
# KPI CARDS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Revenue",
        f"£{total_revenue:,.2f}"
    )

with col2:
    st.metric(
        "Total Orders",
        f"{total_orders:,}"
    )

with col3:
    st.metric(
        "Customers",
        f"{total_customers:,}"
    )

with col4:
    st.metric(
        "Average Order Value",
        f"£{average_order_value:,.2f}"
    )


# ============================================================
# SIDEBAR FILTER
# ============================================================

st.sidebar.header("Filters")

countries = sorted(
    df["country"]
    .dropna()
    .unique()
)

selected_country = st.sidebar.selectbox(
    "Select Country",
    ["All Countries"] + countries
)


# ============================================================
# APPLY FILTER
# ============================================================

if selected_country == "All Countries":

    filtered_df = df.copy()

else:

    filtered_df = df[
        df["country"] == selected_country
    ].copy()


# ============================================================
# FILTERED KPIs
# ============================================================

filtered_revenue = filtered_df["total_sales"].sum()

filtered_orders = filtered_df["invoiceno"].nunique()

filtered_customers = filtered_df["customerid"].nunique()


# ============================================================
# REVENUE BY COUNTRY
# ============================================================

st.subheader("🌍 Revenue by Country")

country_sales = (
    filtered_df
    .groupby("country")["total_sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(country_sales)


# ============================================================
# MONTHLY REVENUE
# ============================================================

st.subheader("📈 Monthly Revenue")

monthly_sales = (
    filtered_df
    .set_index("invoicedate")
    .resample("ME")["total_sales"]
    .sum()
)

st.line_chart(monthly_sales)


# ============================================================
# TOP 10 PRODUCTS
# ============================================================

st.subheader("🏆 Top 10 Products")

top_products = (
    filtered_df
    .groupby("description")["total_sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(top_products)


# ============================================================
# QUANTITY SOLD
# ============================================================

st.subheader("📦 Quantity Sold")

st.metric(
    "Total Quantity",
    f"{filtered_df['quantity'].sum():,}"
)


# ============================================================
# DATA PREVIEW
# ============================================================

st.subheader("📋 Data Preview")

st.dataframe(
    filtered_df.head(100),
    use_container_width=True
)