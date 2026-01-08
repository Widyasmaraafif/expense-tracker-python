from datetime import datetime
from collections import defaultdict


DATE_FORMATS = [
    "%Y-%m-%d %H:%M",
    "%Y-%m-%d"
]


def parse_date(date_str):
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"Format tanggal tidak dikenali: {date_str}")


def calculate_balance(data):
    balance = 0
    for t in data:
        balance += t["amount"] if t["type"] == "income" else -t["amount"]
    return balance


def calculate_monthly_summary(data, month, year):
    income = 0
    expense = 0

    for t in data:
        date = parse_date(t["date"])   # pakai helper kalau ada
        if date.month == month and date.year == year:
            if t["type"] == "income":
                income += t["amount"]
            else:
                expense += t["amount"]

    return {
        "income": income,
        "expense": expense,
        "balance": income - expense
    }


def calculate_category_summary(data, month=None, year=None):
    summary = defaultdict(int)

    for t in data:
        if t["type"] != "expense":
            continue

        date = parse_date(t["date"])
        if not date:
            continue

        if month and year:
            if date.month != month or date.year != year:
                continue

        category = t.get("category", "Other")
        summary[category] += t["amount"]

    return dict(summary)
