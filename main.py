from datetime import datetime
from pathlib import Path

from config import get_paths, CONFIG
from src.data import load_and_validate_sales_data
from src.date_utils import get_reporting_periods
from src.metrics import calculate_kpis
from src.insights import generate_insights
from src.tables import create_all_tables
from src.excel_report import create_formatted_excel_report
from src.zip_handler import create_report_zip
from src.email_handler import send_weekly_report_email


def main():
    today = datetime.now().date()
    paths = get_paths(today)

    print(f"Generating weekly sales report for {today:%Y-%m-%d}")

    # 1. Load data
    df = load_and_validate_sales_data(paths["input_csv"])

    # 2. Determine periods
    periods = get_reporting_periods(df["Date"].max())

    # 3. Filter dataframes
    week_start, week_end = periods["current"]
    last_start, last_end = periods["last_week"]
    four_start, four_end = periods["four_weeks"]

    df_week = df[(df["Date"] >= week_start) & (df["Date"] <= week_end)]
    df_last = df[(df["Date"] >= last_start) & (df["Date"] <= last_end)]
    df_four = df[(df["Date"] >= four_start) & (df["Date"] <= four_end)]

    # 4. Calculate KPIs
    metrics = calculate_kpis(df_week, df_last, df_four)

    # 5. Generate insights
    insights_list = generate_insights(
        metrics, metrics["top_product"], metrics["top_branch"], metrics["top_payment"],
        metrics["top_product_sales"], metrics["top_branch_sales"], metrics["total_sales"]
    )

    # 6. Prepare tables → We pass all the required arguments to ordered table creation
    all_tables_list = create_all_tables(
        metrics=metrics,
        insights_list=insights_list,
        periods=periods,
        df_week=df_week,
        top_product=metrics["top_product"],
        top_product_sales=metrics["top_product_sales"],
        top_branch=metrics["top_branch"],
        top_branch_sales=metrics["top_branch_sales"],
        top_payment=metrics["top_payment"],
        top_payment_share=metrics["top_payment_share"]
    )

    # 7. Create Excel (receives the ordered list of tables)
    create_formatted_excel_report(paths["excel_data"], all_tables_list)

    # 8. Create ZIP (including both Excel files)
    zip_path = create_report_zip(
        output_dir=paths["output_dir"],
        excel_data_path=paths["excel_data"],
        excel_report_path=paths["excel_report"],
        zip_path=paths["zip_file"]
    )

    # 9. Send email
    send_weekly_report_email(zip_path, periods)

    print("Weekly report process completed.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"ERROR: {e}")
        exit(1)