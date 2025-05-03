import pandas as pd


def calculate_iou(
    box1: tuple[float, float, float, float], box2: tuple[float, float, float, float]
) -> float:
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2

    xi1 = max(x1 - w1 / 2, x2 - w2 / 2)
    yi1 = max(y1 - h1 / 2, y2 - h2 / 2)
    xi2 = min(x1 + w1 / 2, x2 + w2 / 2)
    yi2 = min(y1 + h1 / 2, y2 + h2 / 2)

    inter_area = max(0, xi2 - xi1) * max(0, yi2 - yi1)
    box1_area = w1 * h1
    box2_area = w2 * h2
    union_area = box1_area + box2_area - inter_area

    return inter_area / (union_area + 1e-16)


def check_IOU(csv_file: str, threshold: float = 0.9) -> bool:
    df = pd.read_csv(csv_file)
    count_above_threshold = (df["IoU_value"] > threshold).sum()
    percentage = count_above_threshold / len(df)

    # Check if 80% or more of the test images meet the IoU condition
    if percentage >= 0.8:
        return True
    else:
        return False
