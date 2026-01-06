import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime
import csv
import matplotlib.pyplot as plt

DATA_FILE = "data.json"
selected_index = None

CATEGORIES = [
    "Food",
    "Transport",
    "Shopping",
    "Bills",
    "Entertainment",
    "Other"
]

# ===================== DATA =====================

def init_data_file():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump([], f)

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def calculate_balance(data):
    total = 0
    for t in data:
        total += t["amount"] if t["type"] == "income" else -t["amount"]
    return total

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

# ===================== UI ACTIONS =====================

def refresh_list():
    listbox.delete(0, tk.END)

    filtered = data
    if filter_var.get() != "all":
        filtered = [t for t in data if t["type"] == filter_var.get()]

    for t in filtered:
        sign = "+" if t["type"] == "income" else "-"
        category = t.get("category", "Other")
        listbox.insert(
            tk.END,
            f'{t["date"]} | {t["title"]} | {category} | {sign}{t["amount"]}'
        )

    balance_label.config(text=f"Saldo: Rp {calculate_balance(data)}")
    update_monthly_summary()
    update_category_summary()

def update_monthly_summary():
    month = int(month_var.get())
    year = int(year_var.get())

    income, expense, balance = calculate_monthly_summary(data, month, year)
    monthly_income_label.config(text=f"Pemasukan: Rp {income}")
    monthly_expense_label.config(text=f"Pengeluaran: Rp {expense}")
    monthly_balance_label.config(text=f"Saldo Bulan Ini: Rp {balance}")

def update_category_summary():
    for widget in category_frame.winfo_children():
        widget.destroy()

    summary = calculate_category_summary(data)

    if not summary:
        tk.Label(category_frame, text="Belum ada data").pack(anchor="w")
        return

    for cat, total in summary.items():
        tk.Label(
            category_frame,
            text=f"{cat:<15} : Rp {total}",
            anchor="w"
        ).pack(fill="x")

def clear_input():
    title_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    type_var.set("expense")
    category_var.set(CATEGORIES[0])

def add_transaction():
    title = title_entry.get()
    amount = amount_entry.get()

    if not title or not amount:
        messagebox.showwarning("Error", "Input tidak lengkap")
        return

    try:
        amount = int(amount)
    except ValueError:
        messagebox.showerror("Error", "Nominal harus angka")
        return

    data.append({
        "title": title,
        "amount": amount,
        "type": type_var.get(),
        "category": category_var.get(),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    })

    save_data(data)
    refresh_list()
    clear_input()

def edit_transaction():
    global selected_index
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("Error", "Pilih transaksi")
        return

    selected_index = selected[0]
    t = data[selected_index]

    title_entry.insert(0, t["title"])
    amount_entry.insert(0, t["amount"])
    type_var.set(t["type"])
    category_var.set(t.get("category", "Other"))

def update_transaction():
    global selected_index
    if selected_index is None:
        return

    try:
        data[selected_index]["amount"] = int(amount_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Nominal harus angka")
        return

    data[selected_index]["title"] = title_entry.get()
    data[selected_index]["type"] = type_var.get()
    data[selected_index]["category"] = category_var.get()

    save_data(data)
    refresh_list()
    clear_input()
    selected_index = None

def delete_transaction():
    selected = listbox.curselection()
    if not selected:
        return

    if messagebox.askyesno("Konfirmasi", "Hapus transaksi ini?"):
        data.pop(selected[0])
        save_data(data)
        refresh_list()
        clear_input()

def export_csv():
    if not data:
        return

    with open("transactions.csv", "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["date", "title", "category", "amount", "type"]
        )
        writer.writeheader()
        for t in data:
            writer.writerow(t)

    messagebox.showinfo("Sukses", "Export berhasil")

def calculate_category_summary(data):
    summary = {}

    for t in data:
        if t["type"] != "expense":
            continue

        category = t.get("category", "Other")
        summary[category] = summary.get(category, 0) + t["amount"]

    return summary

def get_category_expense_data():
    summary = {}

    for t in data:
        if t["type"] != "expense":
            continue

        cat = t.get("category", "Other")
        summary[cat] = summary.get(cat, 0) + t["amount"]

    return summary

def show_category_pie_chart():
    summary = get_category_expense_data()

    if not summary:
        messagebox.showinfo("Info", "Belum ada data pengeluaran")
        return

    labels = list(summary.keys())
    values = list(summary.values())

    plt.figure(figsize=(6, 6))
    plt.pie(
        values,
        labels=labels,
        autopct="%1.1f%%",
        startangle=140
    )
    plt.title("Pengeluaran per Kategori")
    plt.axis("equal")
    plt.show()

# ===================== INIT =====================

init_data_file()
data = load_data()

root = tk.Tk()
root.title("Expense Tracker")
root.geometry("520x640")
root.minsize(500, 600)

main = tk.Frame(root, padx=15, pady=15)
main.pack(fill="both", expand=True)

# ===================== INPUT =====================

tk.Label(main, text="Transaksi", font=("Arial", 11, "bold")).pack(anchor="w")

tk.Label(main, text="Judul").pack(anchor="w")
title_entry = tk.Entry(main)
title_entry.pack(fill="x")

tk.Label(main, text="Nominal").pack(anchor="w", pady=(5, 0))
amount_entry = tk.Entry(main)
amount_entry.pack(fill="x")

row = tk.Frame(main)
row.pack(fill="x", pady=5)

category_var = tk.StringVar(value=CATEGORIES[0])
tk.OptionMenu(row, category_var, *CATEGORIES).pack(side="left", expand=True, fill="x")

type_var = tk.StringVar(value="expense")
tk.Radiobutton(row, text="Expense", variable=type_var, value="expense").pack(side="left", padx=5)
tk.Radiobutton(row, text="Income", variable=type_var, value="income").pack(side="left")

btns = tk.Frame(main)
btns.pack(pady=8)

tk.Button(btns, text="Tambah", command=add_transaction).pack(side="left", padx=3)
tk.Button(btns, text="Edit", command=edit_transaction).pack(side="left", padx=3)
tk.Button(btns, text="Update", command=update_transaction).pack(side="left", padx=3)
tk.Button(btns, text="Hapus", command=delete_transaction).pack(side="left", padx=3)
tk.Button(btns, text="Export CSV", command=export_csv).pack(side="left", padx=3)
tk.Button(btns, text="Pie Chart", command=show_category_pie_chart).pack(side="left", padx=3)

# ===================== LIST =====================

filter_var = tk.StringVar(value="all")
tk.OptionMenu(main, filter_var, "all", "income", "expense", command=lambda _: refresh_list()).pack()

list_frame = tk.Frame(main)
list_frame.pack(fill="both", expand=True, pady=8)

scroll = tk.Scrollbar(list_frame)
scroll.pack(side="right", fill="y")

listbox = tk.Listbox(list_frame, yscrollcommand=scroll.set, height=8)
listbox.pack(side="left", fill="both", expand=True)
scroll.config(command=listbox.yview)

# ===================== SUMMARY =====================

summary = tk.LabelFrame(main, text="Ringkasan", padx=10, pady=10)
summary.pack(fill="x", pady=5)

balance_label = tk.Label(summary, text="Saldo: Rp 0", font=("Arial", 10, "bold"))
balance_label.pack(anchor="w")

month_var = tk.StringVar(value=str(datetime.now().month))
year_var = tk.StringVar(value=str(datetime.now().year))

tk.OptionMenu(summary, month_var, *[str(i) for i in range(1, 13)], command=lambda _: update_monthly_summary()).pack(side="left")
tk.OptionMenu(summary, year_var, *[str(y) for y in range(2023, datetime.now().year + 1)], command=lambda _: update_monthly_summary()).pack(side="left", padx=5)

monthly_income_label = tk.Label(summary)
monthly_income_label.pack(anchor="w")

monthly_expense_label = tk.Label(summary)
monthly_expense_label.pack(anchor="w")

monthly_balance_label = tk.Label(summary, font=("Arial", 9, "bold"))
monthly_balance_label.pack(anchor="w")

# ================= Category Summary =================
tk.Label(summary, text="Per Kategori", font=("Arial", 9, "bold")).pack(anchor="w", pady=(8, 3))

category_frame = tk.Frame(summary)
category_frame.pack(fill="x")


refresh_list()
root.mainloop()
