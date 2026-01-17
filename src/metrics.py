import pandas as pd


def safe_pct_change(current: float, previous: float) -> float:
    return (current - previous) / previous if previous != 0 else 0.0


def calculate_kpis(df_week: pd.DataFrame, df_last_week: pd.DataFrame, df_4weeks: pd.DataFrame) -> dict:
    """Calculate main KPIs and percentage changes"""
    # Current week
    total_sales = round(df_week["Sales"].sum(), 1)
    transactions = df_week["Invoice ID"].nunique()
    avg_ticket = round(total_sales / transactions, 1) if transactions else 0.0
    avg_rating = round(df_week["Rating"].mean(), 1) if not df_week.empty else 0.0
    total_quantity = int(df_week["Quantity"].sum())
    gross_income = round(df_week["gross income"].sum(), 1)

    # Top performers

    sales_by_product = df_week.groupby("Product line")["Sales"].sum().round(1)
    top_product = sales_by_product.idxmax()
    top_product_sales = sales_by_product.max()

    sales_by_branch = df_week.groupby("City")["Sales"].sum().round(1)
    top_branch = sales_by_branch.idxmax()
    top_branch_sales = sales_by_branch.max()

    payment_dist = df_week.groupby("Payment")["Sales"].sum()
    top_payment = payment_dist.idxmax()
    top_payment_share = round(payment_dist.max() / payment_dist.sum(), 3)

    # Comparisons
    sales_last_week = round(df_last_week["Sales"].sum(), 1)
    sales_4w_sum = df_4weeks["Sales"].sum()
    sales_4w_avg = sales_4w_sum / 4 if sales_4w_sum else 0.0

    trans_last_week = df_last_week["Invoice ID"].nunique()
    trans_4w = df_4weeks["Invoice ID"].nunique()
    trans_4w_avg = trans_4w / 4 if trans_4w else 0.0

    avg_ticket_last = round(df_last_week["Sales"].sum() / trans_last_week, 1) if trans_last_week else 0.0
    avg_ticket_4w = round(sales_4w_sum / trans_4w, 1) if trans_4w else 0.0

    return {
        "total_sales": total_sales,
        "transactions": transactions,
        "avg_ticket": avg_ticket,
        "avg_rating": avg_rating,
        "total_quantity": total_quantity,
        "gross_income": gross_income,
        "pct_sales_last_week": safe_pct_change(total_sales, sales_last_week),
        "pct_sales_4w": safe_pct_change(total_sales, sales_4w_avg),
        "pct_trans_last_week": safe_pct_change(transactions, trans_last_week),
        "pct_trans_4w": safe_pct_change(transactions, trans_4w_avg),
        "pct_avg_ticket_last_week": safe_pct_change(avg_ticket, avg_ticket_last),
        "pct_avg_ticket_4w": safe_pct_change(avg_ticket, avg_ticket_4w),
        # Raw values for top performers
        "sales_last_week_raw": sales_last_week,
        "top_product": top_product,
        "top_product_sales": top_product_sales,
        "top_branch": top_branch,
        "top_branch_sales": top_branch_sales,
        "top_payment": top_payment,
        "top_payment_share": top_payment_share
    }