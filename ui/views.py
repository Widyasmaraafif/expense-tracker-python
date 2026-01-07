import tkinter as tk
from datetime import datetime

from ui.actions import (
    refresh_list,
    add_transaction,
    edit_transaction,
    update_transaction,
    delete_transaction,
    export_csv,
    show_category_pie_chart,
)
from core.calculator import (
    calculate_balance,
    calculate_monthly_summary,
    calculate_category_summary,
)


def build_ui(root, data, save_data):
    # ===================== CONST =====================
    CATEGORIES = ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Other"]

    # ===================== VARIABLES =====================
    search_var = tk.StringVar()
    filter_var = tk.StringVar(value="all")
    type_var = tk.StringVar(value="expense")
    category_var = tk.StringVar(value=CATEGORIES[0])

    month_var = tk.StringVar(value=str(datetime.now().month))
    year_var = tk.StringVar(value=str(datetime.now().year))

    # ===================== MAIN =====================
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

    tk.OptionMenu(row, category_var, *CATEGORIES).pack(side="left", expand=True, fill="x")
    tk.Radiobutton(row, text="Expense", variable=type_var, value="expense").pack(side="left", padx=5)
    tk.Radiobutton(row, text="Income", variable=type_var, value="income").pack(side="left")

    # ===================== BUTTONS =====================
    btns = tk.Frame(main)
    btns.pack(pady=8)

    # ===================== LIST =====================
    tk.Label(main, text="Cari Transaksi").pack(anchor="w")

    search_entry = tk.Entry(main, textvariable=search_var)
    search_entry.pack(fill="x", pady=(0, 5))

    tk.OptionMenu(main, filter_var, "all", "income", "expense").pack()

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

    summary.columnconfigure(0, weight=1)
    summary.columnconfigure(1, weight=1)

    # ===== LEFT COLUMN =====
    left = tk.Frame(summary)
    left.grid(row=0, column=0, sticky="nw")

    balance_label = tk.Label(left, font=("Arial", 10, "bold"))
    balance_label.pack(anchor="w")

    filter_frame = tk.Frame(left)
    filter_frame.pack(anchor="w", pady=5)

    tk.OptionMenu(
        filter_frame, month_var, *[str(i) for i in range(1, 13)],
        command=lambda _: update_summary()
    ).pack(side="left")

    tk.OptionMenu(
        filter_frame, year_var, *[str(y) for y in range(2023, datetime.now().year + 1)],
        command=lambda _: update_summary()
    ).pack(side="left", padx=5)

    monthly_income_label = tk.Label(left)
    monthly_income_label.pack(anchor="w")

    monthly_expense_label = tk.Label(left)
    monthly_expense_label.pack(anchor="w")

    monthly_balance_label = tk.Label(left, font=("Arial", 9, "bold"))
    monthly_balance_label.pack(anchor="w", pady=(0, 5))

    # ===== RIGHT COLUMN =====
    right = tk.Frame(summary)
    right.grid(row=0, column=1, sticky="ne", padx=(20, 0))

    tk.Label(right, text="Per Kategori", font=("Arial", 9, "bold")).pack(anchor="w")

    category_frame = tk.Frame(right)
    category_frame.pack(anchor="w", pady=3)

    # ===================== SUMMARY UPDATE =====================
    def update_summary():
        balance_label.config(text=f"Saldo: Rp {calculate_balance(data)}")

        m, y = int(month_var.get()), int(year_var.get())
        result = calculate_monthly_summary(data, m, y)

        monthly_income_label.config(text=f"Pemasukan: Rp {result['income']}")
        monthly_expense_label.config(text=f"Pengeluaran: Rp {result['expense']}")
        monthly_balance_label.config(
            text=f"Saldo Bulan Ini: Rp {result['balance']}"
        )

        for w in category_frame.winfo_children():
            w.destroy()

        summary_cat = calculate_category_summary(data, m, y)

        if not summary_cat:
            tk.Label(category_frame, text="Belum ada data").pack(anchor="w")
        else:
            for cat, total in summary_cat.items():
                row = tk.Frame(category_frame)
                row.pack(fill="x")

                tk.Label(row, text=cat, width=14, anchor="w").pack(side="left")
                tk.Label(row, text=f"Rp {total}", anchor="e").pack(side="right")

    # ===================== CONTEXT =====================
    ctx = {
        "data": data,
        "save_data": save_data,
        "listbox": listbox,
        "title_entry": title_entry,
        "amount_entry": amount_entry,
        "type_var": type_var,
        "category_var": category_var,
        "search_var": search_var,
        "filter_var": filter_var,
        "categories": CATEGORIES,
        "update_summary": update_summary,
    }

    # ===================== BUTTON WIRING =====================
    tk.Button(btns, text="Tambah", command=lambda: add_transaction(ctx)).pack(side="left", padx=3)
    tk.Button(btns, text="Edit", command=lambda: edit_transaction(ctx)).pack(side="left", padx=3)
    tk.Button(btns, text="Update", command=lambda: update_transaction(ctx)).pack(side="left", padx=3)
    tk.Button(btns, text="Hapus", command=lambda: delete_transaction(ctx)).pack(side="left", padx=3)
    tk.Button(btns, text="Export CSV", command=lambda: export_csv(ctx)).pack(side="left", padx=3)
    tk.Button(btns, text="Pie Chart", command=lambda: show_category_pie_chart(ctx)).pack(side="left", padx=3)

    search_entry.bind("<KeyRelease>", lambda e: refresh_list(ctx))
    filter_var.trace_add("write", lambda *_: refresh_list(ctx))

    refresh_list(ctx)
