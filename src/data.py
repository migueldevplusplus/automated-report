import pandas as pd
import numpy as np
from pathlib import Path
import sys
from typing import Union
from config import CONFIG

def load_and_validate_sales_data(filepath: Union[str, Path]) -> pd.DataFrame:
    """
    Load supermarket sales CSV file and perform comprehensive validation.
    
    Raises SystemExit if critical validation fails.
    Returns cleaned and validated DataFrame.
    """
    filepath = Path(filepath)

    # 1. Try to read the file
    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        print(f"Error: File not found → {filepath}")
        sys.exit(1)
    except pd.errors.ParserError:
        print("Error: CSV file appears to be corrupted or malformed")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error reading CSV: {e}")
        sys.exit(1)

    # 2. Check required columns
    missing_cols = [col for col in CONFIG["expected_columns"] if col not in df.columns]
    if missing_cols:
        print(f"Error: Missing required columns: {', '.join(missing_cols)}")
        print("Expected columns:", ", ".join(CONFIG["expected_columns"]))
        sys.exit(1)

    # 3. Convert date with flexible format handling
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce", dayfirst=False)
    
    invalid_dates = df["Date"].isna()
    if invalid_dates.any():
        print(f"Warning: {invalid_dates.sum()} rows with invalid/missing dates were removed")
        df = df.dropna(subset=["Date"])

    # 4. Basic data type and value validations
    critical_checks = [
        (df["Unit price"] <= 0, "Unit price ≤ 0"),
        (df["Quantity"] <= 0, "Quantity ≤ 0"),
        (df["Quantity"] != df["Quantity"].astype(int), "Quantity is not integer"),
        (df["Tax 5%"] < 0, "Tax 5% is negative"),
        (df["Sales"] <= 0, "Sales ≤ 0"),
        (df["Rating"].isna() | (df["Rating"] < 0) | (df["Rating"] > 10), "Invalid Rating values"),
    ]

    for condition, message in critical_checks:
        if condition.any():
            print(f"CRITICAL VALIDATION ERROR: {message}")
            print("Problematic rows (first 5):")
            print(df[condition].head())
            sys.exit(1)

    # 5. Business logic / calculation consistency checks
    tolerance = 1e-5

    # Tax should be ≈ Unit price × Quantity × 0.05
    tax_calc = df["Unit price"] * df["Quantity"] * 0.05
    tax_error = ~np.isclose(df["Tax 5%"], tax_calc, rtol=tolerance, atol=0.01)
    
    if tax_error.any():
        print("WARNING: Inconsistent Tax 5% calculation in some rows")
        print(df[tax_error][["Invoice ID", "Unit price", "Quantity", "Tax 5%"]].head(6))
        print("→ Consider reviewing these rows manually\n")

    # Sales = Unit price × Quantity + Tax
    sales_calc = df["Unit price"] * df["Quantity"] + df["Tax 5%"]
    sales_error = ~np.isclose(df["Sales"], sales_calc, rtol=tolerance, atol=0.01)
    
    if sales_error.any():
        print("WARNING: Inconsistent Sales total in some rows")
        print(df[sales_error][["Invoice ID", "Unit price", "Quantity", "Tax 5%", "Sales"]].head(6))

    # COGS should be Unit price × Quantity
    cogs_error = ~np.isclose(df["cogs"], df["Unit price"] * df["Quantity"], rtol=tolerance)
    if cogs_error.any():
        print("WARNING: Inconsistent COGS values in some rows")

    # gross income typically = Tax in this dataset
    gross_income_error = ~np.isclose(df["gross income"], df["Tax 5%"], rtol=tolerance)
    if gross_income_error.any():
        print("WARNING: gross income doesn't match Tax 5% in some rows")


    # 6. Categorical value validation

    invalid_branches = ~df["Branch"].isin(CONFIG["valid_branches"])
    if invalid_branches.any():
        print(f"Warning: Invalid Branch values found: {df[invalid_branches]['Branch'].unique()}")

    invalid_cities = ~df["City"].isin(CONFIG["valid_cities"])
    if invalid_cities.any():
        print(f"Warning: Invalid City values found: {df[invalid_cities]['City'].unique()}")

    invalid_customer = ~df["Customer type"].isin(CONFIG["valid_customer_types"])
    if invalid_customer.any():
        print(f"Warning: Invalid Customer type values found: {df[invalid_customer]['Customer type'].unique()}")

    invalid_gender = ~df["Gender"].isin(CONFIG["valid_genders"])
    if invalid_gender.any():
        print(f"Warning: Invalid Gender values found: {df[invalid_gender]['Gender'].unique()}")

    invalid_payment = ~df["Payment"].isin(CONFIG["valid_payments"])
    if invalid_payment.any():
        print(f"Warning: Invalid Payment values found: {df[invalid_payment]['Payment'].unique()}")

    # 7. Final report
    print(f"\nDataset loaded successfully")
    print(f"→ Total rows: {len(df):,}")
    print(f"→ Date range: {df['Date'].min():%Y-%m-%d} → {df['Date'].max():%Y-%m-%d}")
    print(f"→ Unique invoices: {df['Invoice ID'].nunique():,}")
    print("All critical validations passed ✓\n")

    return df

