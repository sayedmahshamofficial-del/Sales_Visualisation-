import pandas as pd
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

RAW_FILE = Path("data/raw/data.csv")
OUTPUT_FILE = Path("data/processed/cleaned_data.csv")


# ============================================================
# LOAD DATA
# ============================================================

def load_data(file_path: Path) -> pd.DataFrame:
    """Load the raw e-commerce dataset."""

    print("Loading dataset...")

    df = pd.read_csv(
        file_path,
        encoding="ISO-8859-1"
    )

    print(f"Loaded {len(df):,} rows and {len(df.columns)} columns.")

    return df


# ============================================================
# CLEAN DATA
# ============================================================

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardize the e-commerce dataset."""

    print("\nStarting data cleaning...")

    # --------------------------------------------------------
    # 1. Remove completely duplicated rows
    # --------------------------------------------------------

    duplicate_count = df.duplicated().sum()

    print(f"Duplicate rows found: {duplicate_count:,}")

    df = df.drop_duplicates().copy()

    print(
        f"Removed {duplicate_count:,} duplicate rows."
    )

    # --------------------------------------------------------
    # 2. Standardize column names
    # --------------------------------------------------------

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # --------------------------------------------------------
    # 3. Clean text columns
    # --------------------------------------------------------

    text_columns = [
        "description",
        "country"
    ]

    for column in text_columns:

        if column in df.columns:

            df[column] = (
                df[column]
                .astype("string")
                .str.strip()
            )

    # --------------------------------------------------------
    # 4. Convert InvoiceDate to datetime
    # --------------------------------------------------------

    if "invoicedate" in df.columns:

        df["invoicedate"] = pd.to_datetime(
            df["invoicedate"],
            errors="coerce"
        )

    # --------------------------------------------------------
    # 5. Convert numeric columns
    # --------------------------------------------------------

    numeric_columns = [
        "quantity",
        "unitprice",
        "customerid"
    ]

    for column in numeric_columns:

        if column in df.columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    # --------------------------------------------------------
    # 6. Remove rows with missing essential values
    # --------------------------------------------------------

    required_columns = [
        "invoiceno",
        "stockcode",
        "quantity",
        "unitprice",
        "country"
    ]

    existing_required_columns = [
        column
        for column in required_columns
        if column in df.columns
    ]

    before = len(df)

    df = df.dropna(
        subset=existing_required_columns
    )

    removed = before - len(df)

    print(
        f"Removed {removed:,} rows with missing essential values."
    )

    # --------------------------------------------------------
    # 7. Remove invalid quantities
    # --------------------------------------------------------

    if "quantity" in df.columns:

        invalid_quantity = (
            df["quantity"] <= 0
        ).sum()

        df = df[
            df["quantity"] > 0
        ].copy()

        print(
            f"Removed {invalid_quantity:,} rows "
            "with invalid quantity."
        )

    # --------------------------------------------------------
    # 8. Remove invalid prices
    # --------------------------------------------------------

    if "unitprice" in df.columns:

        invalid_price = (
            df["unitprice"] <= 0
        ).sum()

        df = df[
            df["unitprice"] > 0
        ].copy()

        print(
            f"Removed {invalid_price:,} rows "
            "with invalid unit price."
        )

    # --------------------------------------------------------
    # 9. Create Total Sales column
    # --------------------------------------------------------

    if {
        "quantity",
        "unitprice"
    }.issubset(df.columns):

        df["total_sales"] = (
            df["quantity"] *
            df["unitprice"]
        )

    print(
        f"\nCleaning completed: {len(df):,} rows remaining."
    )

    return df


# ============================================================
# SAVE CLEANED DATA
# ============================================================

def save_data(
    df: pd.DataFrame,
    output_file: Path
) -> None:
    """Save cleaned dataset."""

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        output_file,
        index=False
    )

    print(
        f"\nCleaned dataset saved to:"
        f"\n{output_file}"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    df = load_data(RAW_FILE)

    cleaned_df = clean_data(df)

    save_data(
        cleaned_df,
        OUTPUT_FILE
    )


if __name__ == "__main__":
    main()