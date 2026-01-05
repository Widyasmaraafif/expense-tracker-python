import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime
import csv

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

def init_data_file():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump([], f)

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

def calculate_monthly_summary(data, month, year):
    income = 0
    expense = 0

    for t in data:
        t_date = datetime.strptime(t["date"], "%Y-%m-%d %H:%M")
        if t_date.month == month and t_date.year == year:
            if t["type"] == "income":
                income += t["amount"]
            else:
                expense += t["amount"]

    return income, expense, income - expense

def refresh_list():
    listbox.delete(0, tk.END)

    filtered_data = data
    if filter_var.get() != "all":
        filtered_data = [t for t in data if t["type"] == filter_var.get()]

    for t in filtered_data:
        sign = "+" if t["type"] == "income" else "-"
        category = t.get("category", "Other")
        listbox.insert(
            tk.END,
            f'{t["date"]} | {t["title"]} | {category} | {sign}{t["amount"]}'
        )

    balance_label.config(text=f"Saldo: Rp {calculate_balance(data)}")
    update_monthly_summary()

def update_monthly_summary():
    month = int(month_var.get())
    year = int(year_var.get())

    income, expense, balance = calculate_monthly_summary(data, month, year)

    monthly_income_label.config(text=f"Pemasukan: Rp {income}")
    monthly_expense_label.config(text=f"Pengeluaran: Rp {expense}")
    monthly_balance_label.config(text=f"Saldo Bulan Ini: Rp {balance}")

def add_transaction():
    title = title_entry.get()
    amount = amount_entry.get()
    t_type = type_var.get()

    if not title or not amount:
        messagebox.showwarning("Error", "Input tidak lengkap")
        return

    try:
        amount = int(amount)
    except ValueError:
        messagebox.showerror("Error", "Nominal harus angka")
        return

    transaction = {
        "title": title,
        "amount": amount,
        "type": t_type,
        "category": category_var.get(),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    data.append(transaction)
    save_data(data)
    refresh_list()
    clear_input()

def edit_transaction():
    global selected_index

    filter_var.set("all")
    refresh_list()
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("Error", "Pilih transaksi untuk diedit")
        return

    selected_index = selected[0]
    t = data[selected_index]

    title_entry.delete(0, tk.END)
    title_entry.insert(0, t["title"])

    amount_entry.delete(0, tk.END)
    amount_entry.insert(0, t["amount"])

    type_var.set(t["type"])
    category_var.set(t.get("category", "Other"))

def update_transaction():
    global selected_index
    if selected_index is None:
        messagebox.showwarning("Error", "Tidak ada transaksi yang diedit")
        return

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

    data[selected_index]["title"] = title
    data[selected_index]["amount"] = amount
    data[selected_index]["type"] = type_var.get()
    data[selected_index]["category"] = category_var.get()

    save_data(data)
    refresh_list()
    clear_input()
    selected_index = None

def delete_transaction():
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("Error", "Pilih transaksi yang ingin dihapus")
        return

    index = selected[0]
    if messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus transaksi ini?"):
        data.pop(index)
        save_data(data)
        refresh_list()
        clear_input()

def clear_input():
    title_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    type_var.set("expense")
    category_var.set(CATEGORIES[0])

def export_csv():
    if not data:
        messagebox.showwarning("Error", "Tidak ada data untuk diekspor")
        return

    with open("transactions.csv", "w", newline='') as csvfile:
        fieldnames = ["date", "title","category", "amount", "type"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for t in data:
            writer.writerow({
                "date": t["date"],
                "title": t["title"],
                "category": t.get("category", "Other"),
                "amount": t["amount"],
                "type": t["type"]
            })

    messagebox.showinfo("Sukses", "Data berhasil diekspor ke transactions.csv")

init_data_file()

# Load data
data = load_data()

# GUI
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("450x520")

tk.Label(root, text="Judul").pack()
title_entry = tk.Entry(root)
title_entry.pack(fill="x", padx=20)

tk.Label(root, text="Nominal").pack()
amount_entry = tk.Entry(root)
amount_entry.pack(fill="x", padx=20)

tk.Label(root, text="Kategori").pack()

category_var = tk.StringVar(value=CATEGORIES[0])

tk.OptionMenu(
    root,
    category_var,
    *CATEGORIES
).pack(fill="x", padx=20)

type_var = tk.StringVar(value="expense")
filter_var = tk.StringVar(value="all")
tk.Radiobutton(root, text="Pengeluaran", variable=type_var, value="expense").pack()
tk.Radiobutton(root, text="Pemasukan", variable=type_var, value="income").pack()

tk.Button(root, text="Tambah", command=add_transaction).pack(pady=3)
tk.Button(root, text="Edit Terpilih", command=edit_transaction).pack(pady=3)
tk.Button(root, text="Update", command=update_transaction).pack(pady=3)
tk.Button(root, text="Hapus Terpilih", command=delete_transaction).pack(pady=3)
tk.Button(root, text="Export CSV", command=export_csv).pack(pady=3)

tk.Label(root, text="Filter").pack()
tk.OptionMenu(
    root,
    filter_var,
    "all",
    "income",
    "expense",
    command=lambda _: refresh_list()
).pack(pady=3)
listbox = tk.Listbox(root, width=60)
listbox.pack(pady=10)

balance_label = tk.Label(root, text="Saldo: Rp 0", font=("Arial", 10, "bold"))
balance_label.pack()

tk.Label(root, text="Monthly Summary", font=("Arial", 10, "bold")).pack(pady=5)

month_var = tk.StringVar(value=str(datetime.now().month))
year_var = tk.StringVar(value=str(datetime.now().year))

month_menu = tk.OptionMenu(
    root,
    month_var,
    *[str(i) for i in range(1, 13)],
    command=lambda _: update_monthly_summary()
)
month_menu.pack()

year_menu = tk.OptionMenu(
    root,
    year_var,
    *[str(y) for y in range(2023, datetime.now().year + 1)],
    command=lambda _: update_monthly_summary()
)
year_menu.pack()

monthly_income_label = tk.Label(root, text="Pemasukan: Rp 0")
monthly_income_label.pack()

monthly_expense_label = tk.Label(root, text="Pengeluaran: Rp 0")
monthly_expense_label.pack()

monthly_balance_label = tk.Label(root, text="Saldo Bulan Ini: Rp 0", font=("Arial", 9, "bold"))
monthly_balance_label.pack()

refresh_list()
root.mainloop()
