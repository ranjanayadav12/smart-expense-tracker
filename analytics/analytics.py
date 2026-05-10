import pandas as pd


# Convert SQLAlchemy objects to DataFrame
def create_dataframe(expenses):

    data = []

    for expense in expenses:

        data.append({
            "title": expense.title,
            "amount": expense.amount,
            "category": expense.category,
            "payment_method": expense.payment_method,
            "date": str(expense.date)
        })

    df = pd.DataFrame(data)

    return df


# Total Spending
def calculate_total(expenses):

    if not expenses:
        return 0

    df = create_dataframe(expenses)

    total = df["amount"].sum()

    return round(total, 2)


# Highest Expense
def highest_expense(expenses):

    if not expenses:
        return 0

    df = create_dataframe(expenses)

    highest = df["amount"].max()

    return round(highest, 2)


# Average Expense
def average_expense(expenses):

    if not expenses:
        return 0

    df = create_dataframe(expenses)

    average = df["amount"].mean()

    return round(average, 2)


# Total Expense Count
def total_transactions(expenses):

    return len(expenses)


# Category-wise Spending
def category_wise_spending(expenses):

    if not expenses:
        return {}

    df = create_dataframe(expenses)

    category_data = (
        df.groupby("category")["amount"]
        .sum()
        .to_dict()
    )

    return category_data


# Monthly Spending
def monthly_spending(expenses):

    if not expenses:
        return {}

    df = create_dataframe(expenses)

    df["date"] = pd.to_datetime(df["date"])

    df["month"] = df["date"].dt.strftime("%B")

    monthly_data = (
        df.groupby("month")["amount"]
        .sum()
        .to_dict()
    )

    return monthly_data


# Category Insights - For Reduction Analysis
def category_insights(expenses):

    if not expenses:
        return []

    df = create_dataframe(expenses)

    total = df["amount"].sum()

    category_data = (
        df.groupby("category")["amount"]
        .agg(["sum", "count"])
        .reset_index()
    )

    category_data.columns = ["category", "total", "count"]

    category_data["percentage"] = (category_data["total"] / total * 100).round(2)

    category_data["average"] = (category_data["total"] / category_data["count"]).round(2)

    category_data = category_data.sort_values("total", ascending=False)

    return category_data.to_dict("records")