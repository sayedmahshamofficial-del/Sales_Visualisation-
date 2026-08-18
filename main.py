from data_cleaning import load_data, clean_data, save_data
from analysis import sales_analysis
from visualization import (
    setup_output_directory,
    plot_sales_by_country,
    plot_top_products,
    plot_monthly_revenue,
    plot_quantity_distribution,
    plot_price_distribution
)

from pathlib import Path


RAW_FILE = Path("data/raw/data.csv")
CLEANED_FILE = Path("data/processed/cleaned_data.csv")


def main():

    print("=" * 60)
    print("E-COMMERCE DATA ANALYSIS PIPELINE")
    print("=" * 60)

    # --------------------------------------------------------
    # 1. LOAD RAW DATA
    # --------------------------------------------------------

    df = load_data(RAW_FILE)

    # --------------------------------------------------------
    # 2. CLEAN DATA
    # --------------------------------------------------------

    cleaned_df = clean_data(df)

    # --------------------------------------------------------
    # 3. SAVE CLEANED DATA
    # --------------------------------------------------------

    save_data(
        cleaned_df,
        CLEANED_FILE
    )

    # --------------------------------------------------------
    # 4. ANALYZE DATA
    # --------------------------------------------------------

    sales_analysis(cleaned_df)

    # --------------------------------------------------------
    # 5. CREATE VISUALIZATIONS
    # --------------------------------------------------------

    setup_output_directory()

    plot_sales_by_country(cleaned_df)
    plot_top_products(cleaned_df)
    plot_monthly_revenue(cleaned_df)
    plot_quantity_distribution(cleaned_df)
    plot_price_distribution(cleaned_df)

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    main()