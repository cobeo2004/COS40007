import pandas as pd
import os

def convert_to_yolo(csv_path: str, output_dir: str):
    """
    Convert bounding box annotations from CSV format to YOLO format.

    Args:
        csv_path (str): Path to the CSV file containing bounding box annotations
        output_dir (str): Directory to save the YOLO format annotation files
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Read the CSV file
    df = pd.read_csv(csv_path)

    # Group by filename
    grouped = df.groupby('filename')

    # Process each image
    for filename, group in grouped:
        # Create annotation filename (same as image filename but with .txt extension)
        annotation_filename = os.path.splitext(filename)[0] + '.txt'
        annotation_path = os.path.join(output_dir, annotation_filename)

        # Get image dimensions
        width = group['width'].iloc[0]
        height = group['height'].iloc[0]

        # Open file for writing
        with open(annotation_path, 'w') as f:
            # Process each bounding box
            for _, row in group.iterrows():
                # Extract bounding box coordinates
                xmin, ymin, xmax, ymax = row['xmin'], row['ymin'], row['xmax'], row['ymax']

                # Convert to YOLO format
                # 1. Calculate center coordinates
                x_center = (xmin + xmax) / 2
                y_center = (ymin + ymax) / 2

                # 2. Calculate width and height
                bbox_width = xmax - xmin
                bbox_height = ymax - ymin

                # 3. Normalize by image dimensions
                x_center /= width
                y_center /= height
                bbox_width /= width
                bbox_height /= height

                # 4. Write to file (class_id = 0 for Graffiti)
                f.write(f"0 {x_center:.6f} {y_center:.6f} {bbox_width:.6f} {bbox_height:.6f}\n")

    print(f"The conversion process is completed. YOLO format for {csv_path} saved to {output_dir}")
