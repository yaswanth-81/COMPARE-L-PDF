import fitz


def extract_spans(doc):

    pages = []

    for page in doc:

        text_dict = page.get_text("dict")

        spans = []

        for block in text_dict["blocks"]:

            if "lines" not in block:
                continue

            for line in block["lines"]:

                for span in line["spans"]:

                    text = span["text"].strip()

                    if not text:
                        continue

                    spans.append({
                        "text": text,
                        "font": span["font"],
                        "size": round(span["size"], 1),
                        "color": span["color"],
                        "flags": span["flags"],
                        "bbox": span["bbox"]
                    })

        pages.append(spans)

    return pages


def apply_cosmetic_diff(doc1, doc2):

    pages1 = extract_spans(doc1)
    pages2 = extract_spans(doc2)

    for page_num in range(min(len(pages1), len(pages2))):

        page = doc1[page_num]

        spans1 = pages1[page_num]
        spans2 = pages2[page_num]

        print(f"\n========== PAGE {page_num + 1} ==========")

        # Create lookup dictionary for PDF2
        lookup2 = {}

        for s in spans2:

            text = s["text"]

            if text not in lookup2:
                lookup2[text] = []

            lookup2[text].append(s)

        for s1 in spans1:

            text = s1["text"]

            if text not in lookup2:
                continue

            matched = False

            for s2 in lookup2[text]:

                cosmetic_changed = False
                reasons = []

                # FONT FAMILY
                if s1["font"] != s2["font"]:

                    cosmetic_changed = True

                    reasons.append(
                        f"Font: {s1['font']} -> {s2['font']}"
                    )

                # FONT SIZE
                if abs(s1["size"] - s2["size"]) > 0.5:

                    cosmetic_changed = True

                    reasons.append(
                        f"Size: {s1['size']} -> {s2['size']}"
                    )

                # COLOR
                if s1["color"] != s2["color"]:

                    cosmetic_changed = True

                    reasons.append("Color Changed")

                # STYLE FLAGS
                if s1["flags"] != s2["flags"]:

                    cosmetic_changed = True

                    reasons.append("Style Changed")

                if cosmetic_changed:

                    x0, y0, x1, y1 = s1["bbox"]

                    rect = fitz.Rect(x0, y0, x1, y1)

                    # BLUE rectangle
                    page.draw_rect(
                        rect,
                        color=(0, 0, 1),
                        width=1.5
                    )

                    print("\nCosmetic Difference Found")
                    print("Text :", text)
                    print("Reasons :")

                    for r in reasons:
                        print("-", r)

                    matched = True
                    break

            if matched:
                continue

    print("\nCosmetic diff applied.")

    return doc1