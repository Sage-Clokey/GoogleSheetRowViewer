
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import tkinter as tk
from tkinter import ttk
import sys

# === STEP 1: Load the Google Sheet === #
try:
    print("Authenticating and loading spreadsheet...")

    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)

    SHEET_ID = "1v6rqZMn-VyMYS8HSsQtCOLS2c-G3GDANfXHVrVCIyL0"
    sheet = client.open_by_key(SHEET_ID).sheet1

    rows = sheet.get_all_values()
    if not rows:
        print("No data found.")
        input("Press Enter to exit...")
        sys.exit()

    headers = rows[0]
    data = rows[1:]

except Exception as e:
    print("Error loading Google Sheet:", e)
    input("Press Enter to exit...")
    sys.exit()

# === STEP 2: Create the GUI === #
root = tk.Tk()
root.title("Google Sheet Row Viewer")

frame = ttk.Frame(root, padding=20)
frame.grid()

row_index = 0

title = ttk.Label(frame, text=f"Row 1", font=("Helvetica", 16))
title.grid(row=0, column=0, columnspan=2, pady=10)

cell_vars = []
for i, header in enumerate(headers):
    ttk.Label(frame, text=f"{header}:", font=("Arial", 10, "bold")).grid(row=i+1, column=0, sticky="e")
    val = tk.StringVar()
    ttk.Label(frame, textvariable=val, font=("Arial", 10)).grid(row=i+1, column=1, sticky="w")
    cell_vars.append(val)

def show_row(index):
    title.config(text=f"Row {index + 1}")
    row_data = data[index]
    for i in range(len(headers)):
        cell_vars[i].set(row_data[i] if i < len(row_data) else "")

def next_row():
    global row_index
    if row_index < len(data) - 1:
        row_index += 1
        show_row(row_index)

def prev_row():
    global row_index
    if row_index > 0:
        row_index -= 1
        show_row(row_index)

ttk.Button(frame, text="← Previous", command=prev_row).grid(row=len(headers)+2, column=0, pady=10)
ttk.Button(frame, text="Next →", command=next_row).grid(row=len(headers)+2, column=1, pady=10)

show_row(row_index)

try:
    root.mainloop()
except Exception as e:
    print("Error during GUI runtime:", e)
    input("Press Enter to close...")
