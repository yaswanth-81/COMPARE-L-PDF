import fitz
from difflib import SequenceMatcher


def extract_words(doc):

    pages = []

    for page in doc:

        words = page.get_text("words")

        word_data = []

        for w in words:

            x0, y0, x1, y1, text, *_ = w

            word_data.append({
                "text": text,
                "bbox": (x0, y0, x1, y1)
            })

        pages.append(word_data)

    return pages


def apply_text_diff(doc1, doc2):

    pages1 = extract_words(doc1)
    pages2 = extract_words(doc2)

    for page_num in range(min(len(pages1), len(pages2))):

        page = doc1[page_num]

        words1 = pages1[page_num]
        words2 = pages2[page_num]

        text1 = [w["text"] for w in words1]
        text2 = [w["text"] for w in words2]

        matcher = SequenceMatcher(None, text1, text2)

        for opcode in matcher.get_opcodes():

            tag, i1, i2, j1, j2 = opcode

            if tag == "equal":
                continue

            # print(f"\n[{tag.upper()}] Page {page_num+1}")

            changed_words = words1[i1:i2]

            for word in changed_words:

                x0, y0, x1, y1 = word["bbox"]

                rect = fitz.Rect(x0, y0, x1, y1)

                highlight = page.add_highlight_annot(rect)

                highlight.update()

                # print(word["text"])

    print("\nText diff applied.")

    return doc1