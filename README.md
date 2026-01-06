# Python GUI Expense Tracker

A simple desktop expense tracker built with Python and Tkinter.
This application allows users to record income and expenses
and automatically calculate the balance.
Designed for Windows users.

## Features

- Add income and expense transactions
- Delete selected transaction list with date & type
- Edit existing transaction
- Export transactions to CSV
- Filter transactions (All / Income / Expense)
- Search transactions
- Mothly Summary
- Category Summary
- Add Category
- Display transaction list
- Automatic balance calculation
- Local JSON storage (offline)
- Desktop GUI (no browser required)

## Visualization

This application includes a pie chart visualization to show expense distribution by category using Matplotlib.

## Tech Stack

- Python 3
- Tkinter (built-in GUI library)
- JSON (local storage)
- PyInstaller (for EXE build – optional)

## Requirements

- Windows 10 / 11
- Python 3.10 or newer

## How to Run (Source Code)
- Clone this repository
    ```bash
    git clone https://github.com/Widyasmaraafif/expense-tracker-python.git
    ```

- Enter the project directory
    ```bash
    cd expense-tracker-python
    ```

- Run the application
    ```bash
    python main.py
    ```

The application window will open automatically.

## Build as Windows EXE (Optional)

This repository contains source code only.
Build files such as dist/ and build/ are intentionally ignored.

1. Install PyInstaller
    ```bash
    pip install pyinstaller
    ```

2. Build EXE
    ```bash
    pyinstaller --onefile --windowed main.py
    ```

3. Result

    The executable file will be generated in:
    dist/main.exe

    You can rename it to:
    ExpenseTracker.exe

## Project Structure
```
expense-tracker-python/
│
├── main.py Main application
├── data.json Local data storage
├── README.md Documentation
└── .gitignore Ignore cache and build files
```

## Notes

- All data is stored locally in data.json
- Exported CSV files are generated locally and not tracked by Git
- No internet connection required
- Works offline on Windows

## Author

Widyasmaraafif