import tkinter as tk

from core.data_manager import init_data_file, load_data, save_data
from ui.views import build_ui


def main():
    # Init data.json (auto create jika belum ada)
    init_data_file()

    # Load data transaksi
    data = load_data()

    # Window utama
    root = tk.Tk()
    root.title("Expense Tracker")
    root.geometry("520x640")
    root.minsize(500, 600)

    # Build UI
    build_ui(
        root=root,
        data=data,
        save_data=lambda d=data: save_data(d)
    )

    root.mainloop()


if __name__ == "__main__":
    main()
