import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime
import csv

DATA_FILE = "data.json"
selected_index = None

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

def refresh_list():
    listbox.delete(0, tk.END)

    filtered_data = data
    if filter_var.get() != "all":
        filtered_data = [t for t in data if t["type"] == filter_var.get()]

    for t in filtered_data:
        sign = "+" if t["type"] == "income" else "-"
        listbox.insert(
            tk.END,
            f'{t["date"]} | {t["title"]} | {sign}{t["amount"]}'
        )

    balance_label.config(text=f"Saldo: Rp {calculate_balance(data)}")


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
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    data.append(transaction)
    save_data(data)
    refresh_list()
    clear_input()

def edit_transaction():
    global selected_index
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

def export_csv():
    if not data:
        messagebox.showwarning("Error", "Tidak ada data untuk diekspor")
        return

    with open("transactions.csv", "w", newline='') as csvfile:
        fieldnames = ["date", "title", "amount", "type"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for t in data:
            writer.writerow(t)

    messagebox.showinfo("Sukses", "Data berhasil diekspor ke transactions.csv")

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

refresh_list()
root.mainloop()
