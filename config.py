from pathlib import Path
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# ── Base paths ───────────────────────────────────────────────────────────────
BASE_DIR = Path.cwd()
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# ── Configuration ────────────────────────────────────────────────────────────
CONFIG = {
    # Data paths and filenames
    "input_csv": DATA_DIR / "sales.csv",
    "output_dir": OUTPUT_DIR,
    "excel_data_filename": "Weekly_Data.xlsx",
    "excel_report_filename": "Weekly_Report.xlsx",     
    "zip_filename_template": "Weekly_Sales_Report_{date}.zip",
    "excel_sheet": "dashboard_data",
    # Data validation settings
    "expected_columns": [
        "Invoice ID", "Branch", "City", "Customer type", "Gender",
        "Product line", "Unit price", "Quantity", "Tax 5%", "Sales",
        "Date", "Time", "Payment", "cogs", "gross margin percentage",
        "gross income", "Rating"
    ],
    "valid_branches": {"Alex", "Giza", "Cairo", "Yangon", "Mandalay", "Naypyitaw"},
    "valid_cities": {"Yangon", "Mandalay", "Naypyitaw"},
    "valid_customer_types": {"Member", "Normal"},
    "valid_genders": {"Male", "Female"},
    "valid_payments": {"Cash", "Credit card", "Ewallet"},
    "date_format_hints": ["%m/%d/%Y", "%d/%m/%Y", "%Y-%m-%d"],
    # Email settings
    "email_from": os.getenv("EMAIL_FROM"),
    "email_to": os.getenv("EMAIL_TO"),
    "email_password": os.getenv("EMAIL_PASSWORD"),
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
}

# Calculated paths (updated with current date when needed)
def get_paths(today: datetime.date):
    date_str = today.strftime("%Y-%m-%d")
    return {
        "input_csv": CONFIG["input_csv"],
        "output_dir": CONFIG["output_dir"],
        "excel_data": CONFIG["output_dir"] / CONFIG["excel_data_filename"],
        "excel_report": CONFIG["output_dir"] / CONFIG["excel_report_filename"],
        "zip_file": CONFIG["output_dir"] / CONFIG["zip_filename_template"].format(date=date_str),
    }