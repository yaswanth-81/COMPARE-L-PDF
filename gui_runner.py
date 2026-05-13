import tkinter as tk
from tkinter import ttk
import threading
import subprocess
import sys
import time


# ==========================================
# CONFIG
# ==========================================

MAIN_SCRIPT = r"Y:\DRDO DAY 2 TASK\PROJECT\main.py"

PYTHON_EXE = r"Y:\DRDO DAY 2 TASK\PROJECT\venv\Scripts\python.exe"

ORIGINAL_FILE = r"Y:\DRDO DAY 2 TASK\PROJECT\selected_original.txt"


# ==========================================
# GET MODIFIED PDF
# ==========================================

modified_pdf = sys.argv[1]

with open(ORIGINAL_FILE, "r", encoding="utf-8") as f:
    original_pdf = f.read().strip()


# ==========================================
# GUI
# ==========================================

root = tk.Tk()

root.title("PDF Comparison Tool")

root.geometry("500x220")
root.resizable(False, False)

# Center window
root.eval('tk::PlaceWindow . center')


title_label = tk.Label(
    root,
    text="Comparing PDFs",
    font=("Segoe UI", 16, "bold")
)

title_label.pack(pady=15)


status_label = tk.Label(
    root,
    text="Initializing...",
    font=("Segoe UI", 11)
)

status_label.pack(pady=10)


progress = ttk.Progressbar(
    root,
    orient="horizontal",
    length=400,
    mode="determinate"
)

progress.pack(pady=20)



# ==========================================
# PROCESS FUNCTION
# ==========================================

def run_comparison():

    try:

        # ======================================
        # TEXT DIFF
        # ======================================

        status_label.config(
            text="Comparing  Differences..."
        )

        root.update()

        progress['value'] = 10

        # ======================================
        # START PROCESS IN BACKGROUND
        # ======================================

        process = subprocess.Popen(

            [
                PYTHON_EXE,
                MAIN_SCRIPT,
                original_pdf,
                modified_pdf
            ],

            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,

            creationflags=subprocess.CREATE_NO_WINDOW
        )

        # ======================================
        # READ LIVE OUTPUT
        # ======================================

        while True:

            line = process.stdout.readline()

            if not line:
                break

            line = line.strip()

            print(line)

            # ==================================
            # DYNAMIC STATUS UPDATES
            # ==================================

            if "Text Difference Completed" in line:

                status_label.config(
                    text="Text Comparison Completed"
                )

                progress['value'] = 35

                root.update()

            elif "Image Difference Completed" in line:

                status_label.config(
                    text="Image Comparison Completed"
                )

                progress['value'] = 65

                root.update()

            elif "Cosmetic Difference Completed" in line:

                status_label.config(
                    text="Cosmetic Comparison Completed"
                )

                progress['value'] = 90

                root.update()

            elif "FINAL PDF GENERATED SUCCESSFULLY" in line:

                status_label.config(
                    text="Generating Final Output..."
                )

                progress['value'] = 100

                root.update()

        process.wait()

        # ======================================
        # DONE
        # ======================================

        title_label.config(
            text="Comparison Completed"
        )

        status_label.config(
            text="Opening Final PDF..."
        )

        progress.stop()

        root.update()

        time.sleep(1.5)

        root.destroy()

    except Exception as e:

        progress.stop()

        status_label.config(
            text=f"Error: {str(e)}"
        )


# ==========================================
# THREAD
# ==========================================

thread = threading.Thread(
    target=run_comparison
)

thread.start()

root.mainloop()