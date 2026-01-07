from datetime import datetime

def calculate_balance(data):
    return sum(
        t["amount"] if t["type"] == "income" else -t["amount"]
        for t in data
    )

def calculate_monthly_summary(data, month, year):
    income, expense = 0, 0

    for t in data:
        t_date = datetime.strptime(t["date"], "%Y-%m-%d %H:%M")
        if t_date.month == month and t_date.year == year:
            if t["type"] == "income":
                income += t["amount"]
            else:
                expense += t["amount"]

    return income, expense, income - expense

def calculate_category_summary(data):
    summary = {}
    for t in data:
        if t["type"] != "expense":
            continue
        cat = t.get("category", "Other")
        summary[cat] = summary.get(cat, 0) + t["amount"]
    return summary
