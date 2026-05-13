import sys
import subprocess

modified_pdf = sys.argv[1]

with open(
    r"Y:\DRDO DAY 2 TASK\PROJECT\selected_original.txt",
    "r",
    encoding="utf-8"
) as f:

    original_pdf = f.read().strip()

print("Original PDF:")
print(original_pdf)

print("Modified PDF:")
print(modified_pdf)

subprocess.run([
    r"Y:\DRDO DAY 2 TASK\PROJECT\venv\Scripts\python.exe",

    r"Y:\DRDO DAY 2 TASK\PROJECT\main.py",

    original_pdf,
    modified_pdf
])

input("\nPress Enter to exit...")