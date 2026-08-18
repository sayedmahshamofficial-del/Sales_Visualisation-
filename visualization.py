import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

CLEANED_FILE = Path("data/processed/cleaned_data.csv")
OUTPUT_DIR = Path("outputs/figures")


# ============================================================
# LOAD DATA
# ============================================================

def load_data(file_path: Path) -> pd.DataFrame:
    """Load the cleaned dataset."""

    df = pd.read_csv(file_path)

    df["invoicedate"] = pd.to_datetime(
        df["invoicedate"],
        errors="coerce"
    )

    return df


# ============================================================
# SETUP
# ============================================================

def setup_output_directory():
    """Create output directory if it doesn't exist."""

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


# ============================================================
# 1. SALES BY COUNTRY
# ============================================================

def plot_sales_by_country(df):

    country_sales = (
        df.groupby("country")["total_sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    plt.figure(figsize=(10, 6))

    sns.barplot(
        x=country_sales.values,
        y=country_sales.index
    )

    plt.title("Top 10 Countries by Revenue")
    plt.xlabel("Revenue (£)")
    plt.ylabel("Country")

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "top_countries_by_revenue.png",
        dpi=300
    )

    plt.close()


# ============================================================
# 2. TOP PRODUCTS
# ============================================================

def plot_top_products(df):

    product_sales = (
        df.groupby("description")["total_sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    plt.figure(figsize=(10, 6))

    sns.barplot(
        x=product_sales.values,
        y=product_sales.index
    )

    plt.title("Top 10 Products by Revenue")
    plt.xlabel("Revenue (£)")
    plt.ylabel("Product")

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "top_products_by_revenue.png",
        dpi=300
    )

    plt.close()


# ============================================================
# 3. MONTHLY REVENUE TREND
# ============================================================

def plot_monthly_revenue(df):

    monthly_sales = (
        df.set_index("invoicedate")
        .resample("ME")["total_sales"]
        .sum()
    )

    plt.figure(figsize=(12, 6))

    sns.lineplot(
        x=monthly_sales.index,
        y=monthly_sales.values
    )

    plt.title("Monthly Revenue Trend")
    plt.xlabel("Month")
    plt.ylabel("Revenue (£)")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "monthly_revenue_trend.png",
        dpi=300
    )

    plt.close()


# ============================================================
# 4. QUANTITY DISTRIBUTION
# ============================================================

def plot_quantity_distribution(df):

    plt.figure(figsize=(10, 6))

    sns.histplot(
        df["quantity"],
        bins=50
    )

    plt.title("Distribution of Quantity Sold")
    plt.xlabel("Quantity")
    plt.ylabel("Number of Transactions")

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "quantity_distribution.png",
        dpi=300
    )

    plt.close()


# ============================================================
# 5. UNIT PRICE DISTRIBUTION
# ============================================================

def plot_price_distribution(df):

    plt.figure(figsize=(10, 6))

    sns.histplot(
        df["unitprice"],
        bins=50
    )

    plt.title("Distribution of Unit Prices")
    plt.xlabel("Unit Price (£)")
    plt.ylabel("Number of Transactions")

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "unit_price_distribution.png",
        dpi=300
    )

    plt.close()


# ============================================================
# MAIN
# ============================================================

def main():

    setup_output_directory()

    df = load_data(CLEANED_FILE)

    print("Generating visualizations...")

    plot_sales_by_country(df)

    plot_top_products(df)

    plot_monthly_revenue(df)

    plot_quantity_distribution(df)

    plot_price_distribution(df)

    print("\nVisualization completed.")

    print(
        f"Charts saved in: {OUTPUT_DIR}"
    )


if __name__ == "__main__":
    main()