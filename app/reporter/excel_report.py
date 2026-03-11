import pandas as pd


def generate_excel_report(df, metrics, categories, ai_advice, weekly_spending):

    writer = pd.ExcelWriter("financial_report.xlsx", engine="xlsxwriter")
    workbook = writer.book

    # ---------------- FORMATS ---------------- #

    title_format = workbook.add_format({
        "bold": True,
        "font_size": 20,
        "align": "center"
    })

    header_format = workbook.add_format({
        "bold": True,
        "bg_color": "#1F4E78",
        "font_color": "white",
        "align": "center",
        "border": 1
    })

    metric_label = workbook.add_format({
        "bold": True,
        "bg_color": "#D9E1F2",
        "border": 1
    })

    metric_value = workbook.add_format({
        "bg_color": "#EBF1F5",
        "border": 1,
        "num_format": "₹#,##0.00"
    })

    currency_format = workbook.add_format({
        "num_format": "₹#,##0.00",
        "border": 1
    })

    section_title = workbook.add_format({
        "bold": True,
        "bg_color": "#4472C4",
        "font_color": "white",
        "align": "center",
        "border": 1
    })

    insight_title = workbook.add_format({
        "bold": True,
        "bg_color": "#70AD47",
        "font_color": "white",
        "align": "center",
        "border": 1
    })

    insight_text = workbook.add_format({
        "text_wrap": True,
        "bg_color": "#E2EFD9",
        "border": 1
    })

    # ---------------- DASHBOARD ---------------- #

    dashboard = workbook.add_worksheet("Dashboard")
    dashboard.merge_range("A1:H1", "Personal Financial Dashboard", title_format)

    # Metric cards
    dashboard.write("A3", "Income", metric_label)
    dashboard.write("B3", metrics["income"], metric_value)

    dashboard.write("C3", "Expenses", metric_label)
    dashboard.write("D3", metrics["expenses"], metric_value)

    dashboard.write("E3", "Net Savings", metric_label)
    dashboard.write("F3", metrics["net_savings"], metric_value)

    # ---------------- CATEGORY TABLE ---------------- #

    dashboard.write("A6", "Category", header_format)
    dashboard.write("B6", "Amount", header_format)

    row = 6
    for cat, amt in categories.items():
        row += 1
        dashboard.write(row, 0, cat)
        dashboard.write(row, 1, amt, currency_format)

    cat_start = 7
    cat_end = row

    # ---------------- CATEGORY CHART ---------------- #

    category_chart = workbook.add_chart({"type": "column"})

    category_chart.add_series({
        "name": "Spending by Category",
        "categories": ["Dashboard", cat_start, 0, cat_end, 0],
        "values": ["Dashboard", cat_start, 1, cat_end, 1],
        "data_labels": {"value": True}
    })

    category_chart.set_title({"name": "Spending by Category"})
    category_chart.set_style(10)

    dashboard.insert_chart("D6", category_chart, {"x_scale": 1.4, "y_scale": 1.4})

    # ---------------- TOP MERCHANTS ---------------- #

    top_merchants = (
        df.groupby("merchant")["amount"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )

    dashboard.write("A15", "Top Merchants", section_title)

    row = 16
    dashboard.write(row, 0, "Merchant", header_format)
    dashboard.write(row, 1, "Amount", header_format)

    row += 1
    for merchant, amt in top_merchants.items():
        dashboard.write(row, 0, merchant)
        dashboard.write(row, 1, amt, currency_format)
        row += 1

    # ---------------- WEEKLY SPENDING TABLE ---------------- #

    dashboard.write("A22", "Week", header_format)
    dashboard.write("B22", "Spending", header_format)

    row = 22
    for _, r in weekly_spending.iterrows():
        row += 1
        dashboard.write(row, 0, f"Week {int(r['week'])}")
        dashboard.write(row, 1, r["amount"], currency_format)

    week_start = 23
    week_end = row

    # ---------------- WEEKLY CHART ---------------- #

    weekly_chart = workbook.add_chart({"type": "line"})

    weekly_chart.add_series({
        "name": "Weekly Spending",
        "categories": ["Dashboard", week_start, 0, week_end, 0],
        "values": ["Dashboard", week_start, 1, week_end, 1],
        "marker": {"type": "circle"}
    })

    weekly_chart.set_title({"name": "Weekly Spending Trend"})
    weekly_chart.set_x_axis({"name": "Week"})
    weekly_chart.set_y_axis({"name": "Amount"})
    weekly_chart.set_style(11)

    dashboard.insert_chart("D20", weekly_chart, {"x_scale": 1.4, "y_scale": 1.4})

    # ---------------- AI INSIGHTS ---------------- #

    insight_start = 45

    dashboard.merge_range(
        insight_start, 3, insight_start, 7,
        "AI Financial Insights",
        insight_title
    )

    row = insight_start + 1

    for line in ai_advice.split("\n"):
        if line.strip():
            dashboard.merge_range(row, 3, row, 7, line, insight_text)
            row += 1

    # Column sizing
    dashboard.set_column("A:A", 25)
    dashboard.set_column("B:B", 18)
    dashboard.set_column("C:C", 4)
    dashboard.set_column("D:H", 35)

    # ---------------- TRANSACTIONS SHEET ---------------- #

    df.to_excel(writer, sheet_name="Transactions", index=False)

    txn_sheet = writer.sheets["Transactions"]
    txn_sheet.freeze_panes(1, 0)

    for col_num, value in enumerate(df.columns.values):
        txn_sheet.write(0, col_num, value, header_format)

    txn_sheet.set_column("A:A", 15)
    txn_sheet.set_column("B:B", 15)
    txn_sheet.set_column("C:C", 40)
    txn_sheet.set_column("D:D", 15)
    txn_sheet.set_column("E:E", 15)
    txn_sheet.set_column("F:F", 20)

    alt1 = workbook.add_format({"bg_color": "#FFFFFF"})
    alt2 = workbook.add_format({"bg_color": "#F2F7FF"})

    for r in range(1, len(df) + 1):
        fmt = alt1 if r % 2 else alt2
        for c in range(len(df.columns)):
            txn_sheet.write(r, c, df.iloc[r - 1, c], fmt)

    writer.close()