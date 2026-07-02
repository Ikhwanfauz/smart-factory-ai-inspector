from pathlib import Path
from collections import Counter
import random
import cv2
import matplotlib.pyplot as plt


DATASET_DIR = Path("data/raw/NEU-DET")

CLASS_NAMES = [
    "crazing",
    "inclusion",
    "patches",
    "pitted_surface",
    "rolled-in_scale",
    "scratches",
]


def count_images_and_labels():
    print("Dataset split summary")
    print("-" * 40)

    for split in ["train", "valid", "test"]:
        image_dir = DATASET_DIR / split / "images"
        label_dir = DATASET_DIR / split / "labels"

        images = list(image_dir.glob("*"))
        labels = list(label_dir.glob("*.txt"))

        print(f"{split}: {len(images)} images, {len(labels)} labels")


def count_classes():
    class_counter = Counter()

    for split in ["train", "valid", "test"]:
        label_dir = DATASET_DIR / split / "labels"

        for label_file in label_dir.glob("*.txt"):
            with open(label_file, "r", encoding="utf-8") as file:
                for line in file:
                    parts = line.strip().split()
                    if len(parts) >= 5:
                        class_id = int(parts[0])
                        class_counter[class_id] += 1

    print("\nClass distribution")
    print("-" * 40)

    for class_id, count in sorted(class_counter.items()):
        class_name = CLASS_NAMES[class_id]
        print(f"{class_id}: {class_name} = {count}")


def draw_sample_image(split="train"):
    image_dir = DATASET_DIR / split / "images"
    label_dir = DATASET_DIR / split / "labels"

    image_files = list(image_dir.glob("*"))
    image_path = random.choice(image_files)

    label_path = label_dir / f"{image_path.stem}.txt"

    image = cv2.imread(str(image_path))
    if image is None:
        raise ValueError(f"Could not read image: {image_path}")

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    height, width, _ = image.shape

    if label_path.exists():
        with open(label_path, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split()

                if len(parts) < 5:
                    continue

                class_id = int(parts[0])
                x_center = float(parts[1]) * width
                y_center = float(parts[2]) * height
                box_width = float(parts[3]) * width
                box_height = float(parts[4]) * height

                x1 = int(x_center - box_width / 2)
                y1 = int(y_center - box_height / 2)
                x2 = int(x_center + box_width / 2)
                y2 = int(y_center + box_height / 2)

                class_name = CLASS_NAMES[class_id]

                cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.putText(
                    image,
                    class_name,
                    (x1, max(y1 - 10, 20)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 0, 0),
                    2,
                )

    output_dir = Path("results")
    output_dir.mkdir(exist_ok=True)

    output_path = output_dir / "dataset_sample_with_bbox.png"

    plt.figure(figsize=(8, 8))
    plt.imshow(image)
    plt.axis("off")
    plt.title(f"Sample image from {split}: {image_path.name}")
    plt.savefig(output_path, bbox_inches="tight")
    plt.show()

    print(f"\nSample image saved to: {output_path}")


if __name__ == "__main__":
    count_images_and_labels()
    count_classes()
    draw_sample_image(split="train")