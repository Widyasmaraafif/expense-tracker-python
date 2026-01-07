from datetime import datetime
from collections import defaultdict


def calculate_balance(data):
    """
    Hitung total saldo keseluruhan
    """
    balance = 0
    for t in data:
        if t["type"] == "income":
            balance += t["amount"]
        else:
            balance -= t["amount"]
    return balance


def monthly_summary(data, month, year):
    """
    Hitung income, expense, balance per bulan
    """
    income = 0
    expense = 0

    for t in data:
        date = datetime.strptime(t["date"], "%Y-%m-%d")
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


def category_summary(data, month=None, year=None):
    """
    Ringkasan expense per kategori
    Bisa global atau per bulan
    """
    summary = defaultdict(int)

    for t in data:
        if t["type"] != "expense":
            continue

        date = datetime.strptime(t["date"], "%Y-%m-%d")

        if month and year:
            if date.month != month or date.year != year:
                continue

        category = t.get("category", "Other")
        summary[category] += t["amount"]

    return dict(summary)
