import pandas as pd
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

CLEANED_FILE = Path("data/processed/cleaned_data.csv")


# ============================================================
# LOAD CLEANED DATA
# ============================================================

def load_cleaned_data(file_path: Path) -> pd.DataFrame:
    """Load the cleaned dataset."""

    return pd.read_csv(file_path)


# ============================================================
# VALIDATE DATA
# ============================================================

def validate_data(df: pd.DataFrame) -> None:
    """Run data-quality checks on the cleaned dataset."""

    print("\n" + "=" * 60)
    print("CLEANED DATA VALIDATION")
    print("=" * 60)

    # --------------------------------------------------------
    # 1. Dataset size
    # --------------------------------------------------------

    print("\n1. DATASET SIZE")
    print("-" * 60)
    print(f"Rows    : {len(df):,}")
    print(f"Columns : {len(df.columns)}")

    # --------------------------------------------------------
    # 2. Missing values
    # --------------------------------------------------------

    print("\n2. MISSING VALUES")
    print("-" * 60)

    missing = df.isnull().sum()

    missing = missing[missing > 0]

    if missing.empty:
        print("✓ No missing values found.")
    else:
        print(missing)

    # --------------------------------------------------------
    # 3. Duplicate rows
    # --------------------------------------------------------

    print("\n3. DUPLICATE ROWS")
    print("-" * 60)

    duplicates = df.duplicated().sum()

    print(f"Duplicate rows: {duplicates:,}")

    if duplicates == 0:
        print("✓ No duplicate rows found.")

    # --------------------------------------------------------
    # 4. Invalid quantities
    # --------------------------------------------------------

    print("\n4. INVALID QUANTITIES")
    print("-" * 60)

    if "quantity" in df.columns:

        invalid_quantity = (
            df["quantity"] <= 0
        ).sum()

        print(
            f"Quantity <= 0: {invalid_quantity:,}"
        )

    # --------------------------------------------------------
    # 5. Invalid prices
    # --------------------------------------------------------

    print("\n5. INVALID PRICES")
    print("-" * 60)

    if "unitprice" in df.columns:

        invalid_price = (
            df["unitprice"] <= 0
        ).sum()

        print(
            f"Unit price <= 0: {invalid_price:,}"
        )

    # --------------------------------------------------------
    # 6. Data types
    # --------------------------------------------------------

    print("\n6. DATA TYPES")
    print("-" * 60)

    print(df.dtypes)

    # --------------------------------------------------------
    # 7. Total sales validation
    # --------------------------------------------------------

    print("\n7. TOTAL SALES VALIDATION")
    print("-" * 60)

    if {
        "quantity",
        "unitprice",
        "total_sales"
    }.issubset(df.columns):

        expected_sales = (
            df["quantity"] *
            df["unitprice"]
        )

        incorrect = (
            (df["total_sales"] - expected_sales)
            .abs() > 0.01
        ).sum()

        print(
            f"Incorrect total_sales rows: {incorrect:,}"
        )

        if incorrect == 0:
            print("✓ Total sales calculation is correct.")

    # --------------------------------------------------------
    # 8. Final status
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("VALIDATION COMPLETED")
    print("=" * 60)


# ============================================================
# MAIN
# ============================================================

def main():

    df = load_cleaned_data(CLEANED_FILE)

    validate_data(df)


if __name__ == "__main__":
    main()