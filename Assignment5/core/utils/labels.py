import csv
import os
from .iou import calculate_iou

def process_labels(ground_truth_dir: str, predict_dir: str, output_csv: str) -> None:
    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["image_name", "confidence_value", "IoU_value"])

        # Collect all ground truth files
        gt_files = [f for f in os.listdir(ground_truth_dir) if f.endswith('.txt')]

        for gt_file in gt_files:
            image_name = gt_file.replace('.txt', '')

            # Read ground truth boxes once
            gt_path = os.path.join(ground_truth_dir, gt_file)
            with open(gt_path, 'r') as f:
                ground_truth_data = [list(map(float, line.strip().split()[1:5])) for line in f.readlines()]

            # Check for the corresponding prediction file
            pred_path = os.path.join(predict_dir, gt_file)
            if os.path.exists(pred_path):
                with open(pred_path, 'r') as f:
                    predict_data = [line.strip().split() for line in f.readlines()]

                if not predict_data:
                    # No predictions, write IoU and confidence as 0
                    writer.writerow([image_name, 0, 0])
                    continue

                # Instead of averaging, find the highest confidence prediction
                highest_confidence = 0
                highest_iou = 0

                # Process each predicted box
                for pred_values in predict_data:
                    confidence = float(pred_values[-1])
                    pred_box = list(map(float, pred_values[1:5]))  # Predicted box
                    # Calculate IoU against all ground truth boxes and keep the maximum IoU
                    max_iou = max(calculate_iou(pred_box, gt_box) for gt_box in ground_truth_data)

                    # Update highest confidence prediction if current is higher
                    if confidence > highest_confidence:
                        highest_confidence = confidence
                        highest_iou = max_iou

                # Write the highest confidence prediction to the CSV
                writer.writerow([image_name, highest_confidence, highest_iou])

            else:
                # If no prediction file, write IoU and confidence as 0
                writer.writerow([image_name, 0, 0])
