def generate_insights(metrics: dict, top_product: str, top_branch: str, top_payment: str,
    top_product_sales: float, top_branch_sales: float, total_sales: float) -> list[str]:
    pct_sales_last = metrics["pct_sales_last_week"]

    if pct_sales_last > 0.05:
        insight1 = f"Sales up {pct_sales_last:.1%} vs last week, led by {top_product}."
    elif pct_sales_last < -0.05:
        insight1 = f"Sales down {abs(pct_sales_last):.1%} vs last week; {top_product} still top category."
    else:
        insight1 = f"Sales stable ({pct_sales_last:+.1%}) vs last week. {top_product} leads."

    return [
        insight1,
        f"{top_branch} drove {(top_branch_sales / total_sales):.1%} of weekly revenue.",
        f"{top_payment} was the preferred payment method.",
        f"Top category: {top_product} ({(top_product_sales / total_sales):.1%} of sales).",
        f"Average rating stable at {metrics['avg_rating']:.1f}."
    ]