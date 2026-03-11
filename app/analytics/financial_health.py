import pandas as pd


def calculate_financial_metrics(df):

    income = round(float(df[df["type"] == "credit"]["amount"].sum()), 2)

    expenses = round(float(df[df["type"] == "debit"]["amount"].sum()), 2)

    net_savings = income - expenses

    savings_rate = 0

    if income > 0:
        savings_rate = net_savings / income

    return {
        "income": income,
        "expenses": expenses,
        "net_savings": net_savings,
        "savings_rate": savings_rate
    }

def category_spending(df):

    debit_df = df[df["type"] == "debit"]

    category_totals = debit_df.groupby("category")["amount"].sum()

    return category_totals.to_dict()

def financial_health_score(metrics):

    score = 50   # base score

    savings_rate = metrics["savings_rate"]
    
    if metrics["expenses"] > metrics["income"]:
        score -= 10

    if savings_rate > 0.40:
        score += 30
    elif savings_rate > 0.20:
        score += 20
    elif savings_rate > 0:
        score += 10
    else:
        score -= 20

    return max(0, min(score, 100))