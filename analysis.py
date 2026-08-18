import pandas as pd
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

CLEANED_FILE = Path("data/processed/cleaned_data.csv")


# ============================================================
# LOAD DATA
# ============================================================

def load_data(file_path: Path) -> pd.DataFrame:
    """Load the cleaned dataset."""

    return pd.read_csv(file_path)


# ============================================================
# SALES ANALYSIS
# ============================================================

def sales_analysis(df: pd.DataFrame) -> None:

    print("\n" + "=" * 60)
    print("E-COMMERCE SALES ANALYSIS")
    print("=" * 60)

    # --------------------------------------------------------
    # 1. Total Revenue
    # --------------------------------------------------------

    total_revenue = df["total_sales"].sum()

    print("\n1. TOTAL REVENUE")
    print("-" * 60)
    print(f"Total Revenue: £{total_revenue:,.2f}")

    # --------------------------------------------------------
    # 2. Total Quantity Sold
    # --------------------------------------------------------

    total_quantity = df["quantity"].sum()

    print("\n2. TOTAL QUANTITY SOLD")
    print("-" * 60)
    print(f"Quantity Sold: {total_quantity:,}")

    # --------------------------------------------------------
    # 3. Number of Orders
    # --------------------------------------------------------

    total_orders = df["invoiceno"].nunique()

    print("\n3. TOTAL ORDERS")
    print("-" * 60)
    print(f"Orders: {total_orders:,}")

    # --------------------------------------------------------
    # 4. Number of Customers
    # --------------------------------------------------------

    if "customerid" in df.columns:

        total_customers = df["customerid"].nunique()

        print("\n4. UNIQUE CUSTOMERS")
        print("-" * 60)
        print(f"Customers: {total_customers:,}")

    # --------------------------------------------------------
    # 5. Average Order Value
    # --------------------------------------------------------

    order_revenue = (
        df.groupby("invoiceno")["total_sales"]
        .sum()
    )

    average_order_value = order_revenue.mean()

    print("\n5. AVERAGE ORDER VALUE")
    print("-" * 60)
    print(
        f"Average Order Value: "
        f"£{average_order_value:,.2f}"
    )

    # --------------------------------------------------------
    # 6. Top Products
    # --------------------------------------------------------

    top_products = (
        df.groupby("description")["total_sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    print("\n6. TOP 10 PRODUCTS BY REVENUE")
    print("-" * 60)
    print(top_products)

    # --------------------------------------------------------
    # 7. Top Countries
    # --------------------------------------------------------

    top_countries = (
        df.groupby("country")["total_sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    print("\n7. TOP 10 COUNTRIES BY REVENUE")
    print("-" * 60)
    print(top_countries)

    # --------------------------------------------------------
    # 8. Monthly Revenue
    # --------------------------------------------------------

    df["invoicedate"] = pd.to_datetime(
        df["invoicedate"],
        errors="coerce"
    )

    monthly_revenue = (
        df.set_index("invoicedate")
        .resample("ME")["total_sales"]
        .sum()
    )

    print("\n8. MONTHLY REVENUE")
    print("-" * 60)
    print(monthly_revenue)


# ============================================================
# MAIN
# ============================================================

def main():

    df = load_data(CLEANED_FILE)

    sales_analysis(df)


if __name__ == "__main__":
    main()