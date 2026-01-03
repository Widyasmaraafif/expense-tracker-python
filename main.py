import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
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

def add_transaction():
    title = title_entry.get()
    amount = amount_entry.get()
    t_type = type_var.get()

    if not title or not amount:
        messagebox.showwarning("Error", "Input tidak lengkap")
        return

    transaction = {
        "title": title,
        "amount": int(amount),
        "type": t_type,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    data.append(transaction)
    save_data(data)
    refresh_list()

    title_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)

def refresh_list():
    listbox.delete(0, tk.END)
    for t in data:
        sign = "+" if t["type"] == "income" else "-"
        listbox.insert(
            tk.END,
            f'{t["date"]} | {t["title"]} | {sign}{t["amount"]}'
        )
    balance_label.config(text=f"Saldo: Rp {calculate_balance(data)}")

data = load_data()

root = tk.Tk()
root.title("Expense Tracker")

# UI
tk.Label(root, text="Judul").pack()
title_entry = tk.Entry(root)
title_entry.pack()

tk.Label(root, text="Nominal").pack()
amount_entry = tk.Entry(root)
amount_entry.pack()

type_var = tk.StringVar(value="expense")
tk.Radiobutton(root, text="Pengeluaran", variable=type_var, value="expense").pack()
tk.Radiobutton(root, text="Pemasukan", variable=type_var, value="income").pack()

tk.Button(root, text="Tambah", command=add_transaction).pack(pady=5)

listbox = tk.Listbox(root, width=50)
listbox.pack(pady=10)

balance_label = tk.Label(root, text="Saldo: Rp 0")
balance_label.pack()

refresh_list()
root.mainloop()
