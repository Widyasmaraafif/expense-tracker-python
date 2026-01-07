import csv
from datetime import datetime
from tkinter import messagebox


# ===================== STATE =====================

selected_index = None


# ===================== ACTIONS =====================

def refresh_list(ctx):
    """
    Refresh listbox + summary
    ctx = dictionary berisi semua reference UI & data
    """
    listbox = ctx["listbox"]
    data = ctx["data"]
    search_var = ctx["search_var"]
    filter_var = ctx["filter_var"]

    listbox.delete(0, "end")

    keyword = search_var.get().lower()
    filtered = data

    # filter type
    if filter_var.get() != "all":
        filtered = [t for t in filtered if t["type"] == filter_var.get()]

    # search
    if keyword:
        filtered = [
            t for t in filtered
            if keyword in t["title"].lower()
            or keyword in t.get("category", "").lower()
            or keyword in str(t["amount"])
        ]

    for t in filtered:
        sign = "+" if t["type"] == "income" else "-"
        listbox.insert(
            "end",
            f'{t["date"]} | {t["title"]} | {t["category"]} | {sign}{t["amount"]}'
        )

    ctx["update_summary"]()


def clear_input(ctx):
    ctx["title_entry"].delete(0, "end")
    ctx["amount_entry"].delete(0, "end")
    ctx["type_var"].set("expense")
    ctx["category_var"].set(ctx["categories"][0])


def add_transaction(ctx):
    title = ctx["title_entry"].get()
    amount = ctx["amount_entry"].get()

    if not title or not amount:
        messagebox.showwarning("Error", "Input tidak lengkap")
        return

    try:
        amount = int(amount)
    except ValueError:
        messagebox.showerror("Error", "Nominal harus angka")
        return

    ctx["data"].append({
        "title": title,
        "amount": amount,
        "type": ctx["type_var"].get(),
        "category": ctx["category_var"].get(),
        "date": datetime.now().strftime("%Y-%m-%d")
    })

    ctx["save_data"](ctx["data"])
    refresh_list(ctx)
    clear_input(ctx)


def edit_transaction(ctx):
    global selected_index

    selected = ctx["listbox"].curselection()
    if not selected:
        messagebox.showwarning("Error", "Pilih transaksi")
        return

    selected_index = selected[0]
    t = ctx["data"][selected_index]

    ctx["title_entry"].delete(0, "end")
    ctx["amount_entry"].delete(0, "end")

    ctx["title_entry"].insert(0, t["title"])
    ctx["amount_entry"].insert(0, t["amount"])
    ctx["type_var"].set(t["type"])
    ctx["category_var"].set(t["category"])


def update_transaction(ctx):
    global selected_index

    if selected_index is None:
        return

    try:
        ctx["data"][selected_index]["amount"] = int(ctx["amount_entry"].get())
    except ValueError:
        messagebox.showerror("Error", "Nominal harus angka")
        return

    ctx["data"][selected_index]["title"] = ctx["title_entry"].get()
    ctx["data"][selected_index]["type"] = ctx["type_var"].get()
    ctx["data"][selected_index]["category"] = ctx["category_var"].get()

    ctx["save_data"](ctx["data"])
    refresh_list(ctx)
    clear_input(ctx)
    selected_index = None


def delete_transaction(ctx):
    selected = ctx["listbox"].curselection()
    if not selected:
        return

    if messagebox.askyesno("Konfirmasi", "Hapus transaksi ini?"):
        ctx["data"].pop(selected[0])
        ctx["save_data"](ctx["data"])
        refresh_list(ctx)
        clear_input(ctx)


def export_csv(ctx):
    if not ctx["data"]:
        return

    with open("transactions.csv", "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["date", "title", "category", "amount", "type"]
        )
        writer.writeheader()
        for t in ctx["data"]:
            writer.writerow(t)

    messagebox.showinfo("Sukses", "Export CSV berhasil")
