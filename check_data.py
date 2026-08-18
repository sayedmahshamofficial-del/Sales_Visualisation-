import pandas as pd

# --------------------------------------------------
# 1. LOAD DATA
# --------------------------------------------------

FILE_PATH = "data/raw/data.csv"

df = pd.read_csv(
    FILE_PATH,
    encoding="ISO-8859-1"
)

# --------------------------------------------------
# 2. BASIC DATASET INFORMATION
# --------------------------------------------------

print("\n" + "=" * 60)
print("DATASET OVERVIEW")
print("=" * 60)

print(f"Rows    : {df.shape[0]:,}")
print(f"Columns : {df.shape[1]}")

# --------------------------------------------------
# 3. COLUMN INFORMATION
# --------------------------------------------------

print("\n" + "=" * 60)
print("COLUMN INFORMATION")
print("=" * 60)

print(df.dtypes)

# --------------------------------------------------
# 4. MISSING VALUES
# --------------------------------------------------

missing_values = df.isnull().sum()

missing_percentage = (
    df.isnull().mean() * 100
).round(2)

missing_report = pd.DataFrame({
    "Missing_Count": missing_values,
    "Missing_Percentage": missing_percentage
})

print("\n" + "=" * 60)
print("MISSING VALUE REPORT")
print("=" * 60)

print(
    missing_report[
        missing_report["Missing_Count"] > 0
    ]
)

# --------------------------------------------------
# 5. DUPLICATES
# --------------------------------------------------

duplicate_count = df.duplicated().sum()

print("\n" + "=" * 60)
print("DUPLICATE REPORT")
print("=" * 60)

print(f"Duplicate rows: {duplicate_count:,}")

# --------------------------------------------------
# 6. SAMPLE DATA
# --------------------------------------------------

print("\n" + "=" * 60)
print("FIRST 5 ROWS")
print("=" * 60)

print(df.head())
