import fitz
import os

from text_diff import apply_text_diff
from image_diff import apply_image_diff
from cosmetic_diff import apply_cosmetic_diff


PDF1 = "input/original.pdf"
PDF2 = "input/modified.pdf"

OUTPUT = "output/final_diff.pdf"

os.makedirs("output", exist_ok=True)


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


if __name__ == "__main__":
    main()