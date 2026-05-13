import fitz
import os
import sys

from text_diff import apply_text_diff
from image_diff import apply_image_diff
from cosmetic_diff import apply_cosmetic_diff




PDF1 = sys.argv[1]
PDF2 = sys.argv[2]

import os

modified_name = os.path.splitext(
    os.path.basename(PDF2)
)[0]

output_folder = os.path.dirname(PDF2)

OUTPUT = os.path.join(
    output_folder,
    f"{modified_name}_diff.pdf"
)


def main():

    print("\n===================================")
    print("PDF DIFFERENCE DETECTION STARTED")
    print("===================================")

    # Open PDFs
    doc1 = fitz.open(PDF1)
    doc2 = fitz.open(PDF2)

    # ==========================================
    # TEXT DIFFERENCE
    # ==========================================

    print("\nRunning Text Difference Detection...\n")

    doc1 = apply_text_diff(doc1, doc2)

    print("\nText Difference Completed.")

    # ==========================================
    # IMAGE DIFFERENCE
    # ==========================================

    print("\nRunning Image Difference Detection...\n")

    doc1 = apply_image_diff(doc1, doc2)

    print("\nImage Difference Completed.")

    # ==========================================
    # COSMETIC DIFFERENCE
    # ==========================================

    print("\nRunning Cosmetic Difference Detection...\n")

    doc1 = apply_cosmetic_diff(doc1, doc2)

    print("\nCosmetic Difference Completed.")

    # ==========================================
    # SAVE FINAL PDF
    # ==========================================

    doc1.save(OUTPUT)

    print("\n===================================")
    print("FINAL PDF GENERATED SUCCESSFULLY")
    print("===================================")

    print(f"\nSaved Output:\n{OUTPUT}")
    os.startfile(OUTPUT)


if __name__ == "__main__":
    main()