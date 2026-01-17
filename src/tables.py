import pandas as pd
from datetime import datetime


def create_all_tables(
    metrics: dict,
    insights_list: list[str],
    periods: dict,
    df_week: pd.DataFrame,
    top_product: str,
    top_product_sales: float,
    top_branch: str,
    top_branch_sales: float,
    top_payment: str,
    top_payment_share: float
) -> list:
    """
    Creates ALL tables exactly as in the original script
    and returns them as an ordered list to preserve the sequence in Excel
    """
    today_str = datetime.now().strftime("%m/%d/%y")
    week_start, week_end = periods["current"]

    # 1. Main KPIs
    tbl_kpis = pd.DataFrame({
        "Metric": ["Total Sales", "Transactions", "Average Ticket", "Average Rating", "Total Quantity", "Gross Income"],
        "Value": [
            metrics["total_sales"],
            metrics["transactions"],
            metrics["avg_ticket"],
            metrics["avg_rating"],
            metrics["total_quantity"],
            metrics["gross_income"]
        ]
    })

    # 2. Percentage changes
    tbl_kpis_percentage_changes = pd.DataFrame({
        "Metric": [
            "Sales vs Last Week", "Sales vs Previous 4 Weeks",
            "Transactions vs Last Week", "Transactions vs Previous 4 Weeks",
            "Avg Ticket vs Last Week", "Avg Ticket vs Previous 4 Weeks"
        ],
        "Value": [
            round(metrics["pct_sales_last_week"], 3),
            round(metrics["pct_sales_4w"], 3),
            round(metrics["pct_trans_last_week"], 3),
            round(metrics["pct_trans_4w"], 3),
            round(metrics["pct_avg_ticket_last_week"], 3),
            round(metrics["pct_avg_ticket_4w"], 3),
        ]
    })

    # 3. Top performers
    tbl_top_performers = pd.DataFrame({
        "Category": ["Top Product Line", "Best Performing Branch", "Top Payment Method"],
        "Detail": [top_product, top_branch, top_payment],
        "Value": [top_product_sales, top_branch_sales, top_payment_share]
    })

    # 4. Insights
    tbl_insights = pd.DataFrame({"Insight": insights_list})

    # 5. Report information
    tbl_report_info = pd.DataFrame({
        "Report Information": [
            "WEEKLY SALES PERFORMANCE REPORT",
            f"Week: {week_start.strftime('%m/%d/%y')} – {week_end.strftime('%m/%d/%y')}",
            f"Generated automatically on: {today_str}"
        ]
    })

    # 6. Sales by day
    df_day = df_week.copy() 
    df_day["Day"] = df_day["Date"].dt.day_name()
    sales_by_day = df_day.groupby("Day")["Sales"].sum().round(1).reset_index()
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    sales_by_day["Day"] = pd.Categorical(sales_by_day["Day"], categories=day_order, ordered=True)
    sales_by_day = sales_by_day.sort_values("Day").reset_index(drop=True)

    # 7. Payment method distribution
    tbl_payment_distribution = df_week.groupby("Payment", as_index=False)["Sales"].sum().round(1)
    tbl_payment_distribution["Percentage"] = (tbl_payment_distribution["Sales"] / tbl_payment_distribution["Sales"].sum()).round(3)

    # 8. Sales by product line
    tbl_sales_by_product = df_week.groupby("Product line", as_index=False)["Sales"].sum().round(1)

    # Return an ordered list exactly matching the original script structure
    return [
        ("tbl_kpis", tbl_kpis),
        ("tbl_kpis_percentage_changes", tbl_kpis_percentage_changes),
        ("tbl_top_performers", tbl_top_performers),
        ("tbl_sales_by_product", tbl_sales_by_product),
        ("tbl_sales_by_day", sales_by_day),
        ("tbl_payment_distribution", tbl_payment_distribution),
        ("tbl_insights", tbl_insights),
        ("tbl_report_info", tbl_report_info),
    ]