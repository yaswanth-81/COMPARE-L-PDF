import sys

ORIGINAL_FILE = r"Y:\DRDO DAY 2 TASK\PROJECT\selected_original.txt"

pdf_path = sys.argv[1]

with open(ORIGINAL_FILE, "w", encoding="utf-8") as f:
    f.write(pdf_path)

print("Original PDF selected:")
print(pdf_path)