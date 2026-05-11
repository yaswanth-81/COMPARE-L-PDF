import fitz
import cv2
import numpy as np

from skimage.metrics import structural_similarity as ssim


def extract_images(doc):

    all_images = []

    for page_index in range(len(doc)):

        page = doc[page_index]

        image_list = page.get_images(full=True)

        page_images = []

        for img_index, img in enumerate(image_list):

            xref = img[0]

            base_image = doc.extract_image(xref)

            image_bytes = base_image["image"]

            np_img = np.frombuffer(image_bytes, dtype=np.uint8)

            image = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

            rects = page.get_image_rects(xref)

            bbox = rects[0] if rects else None

            page_images.append({
                "image": image,
                "bbox": bbox
            })

        all_images.append(page_images)

    return all_images


def apply_image_diff(doc1, doc2):

    images1 = extract_images(doc1)
    images2 = extract_images(doc2)

    for page_num in range(min(len(images1), len(images2))):

        page = doc1[page_num]

        imgs1 = images1[page_num]
        imgs2 = images2[page_num]

        max_imgs = max(len(imgs1), len(imgs2))

        print(f"\nProcessing Page {page_num + 1}")

        for i in range(max_imgs):

            if i >= len(imgs1):

                print("New image added")
                continue

            if i >= len(imgs2):

                print("Image removed")

                bbox = imgs1[i]["bbox"]

                if bbox:

                    page.draw_rect(
                        bbox,
                        color=(1, 0, 0),
                        width=3
                    )

                continue

            img1 = imgs1[i]["image"]
            img2 = imgs2[i]["image"]

            if img1 is None or img2 is None:
                continue

            # Resize to same size
            h = min(img1.shape[0], img2.shape[0])
            w = min(img1.shape[1], img2.shape[1])

            img1 = cv2.resize(img1, (w, h))
            img2 = cv2.resize(img2, (w, h))

            gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
            gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

            # Ensure same size
            gray2 = cv2.resize(gray2, (gray1.shape[1], gray1.shape[0]))

            h, w = gray1.shape
            min_dim = min(h, w)

            # Skip extremely tiny images
            if min_dim < 3:
                continue

            # Dynamic win_size
            win_size = min(7, min_dim)

            if win_size % 2 == 0:
                win_size -= 1

            score, _ = ssim(gray1, gray2, full=True, win_size=win_size)

            print(f"Image {i+1} Similarity:", round(score, 4))

            # If images differ
            if score < 0.95:

                bbox = imgs1[i]["bbox"]

                if bbox:

                    page.draw_rect(
                        bbox,
                        color=(1, 0, 0),
                        width=3
                    )

                    print("Image difference detected")

    print("\nImage diff applied.")

    return doc1
