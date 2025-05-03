import os
import random
import shutil
from pathlib import Path
from typing import Tuple, List, Optional


def split_dataset(
    source_dir: str = "data/converted",
    output_dir: str = "data/split_dataset",
    train_sample_size: int = 400,
    test_sample_size: int = 40,
    val_size: int = 40,
    random_seed: Optional[int] = None
) -> Tuple[List[str], List[str], List[str]]:
    """
    Randomly split dataset into train, test, and validation sets,
    maintaining the correspondence between images and their annotation files.

    Works with a directory structure where:
    - source_dir/images/train/ - contains training images
    - source_dir/images/test/ - contains test images
    - source_dir/labels/train/ - contains training annotations
    - source_dir/labels/test/ - contains test annotations

    Args:
        source_dir: Base directory containing 'images' and 'labels' folders with train/test subfolders
        output_dir: Directory where split dataset will be saved
        train_sample_size: Number of samples to take from train folder (if available)
        test_sample_size: Number of samples to take from test folder for test set (if available)
        val_size: Number of samples to take from test folder for validation set (if available)
        random_seed: Optional seed for random number generator

    Returns:
        Tuple of lists containing filenames for train, test, and validation sets
    """
    if random_seed is not None:
        random.seed(random_seed)

    # Source directories
    train_images_dir = os.path.join(source_dir, "images", "train")
    test_images_dir = os.path.join(source_dir, "images", "test")
    train_labels_dir = os.path.join(source_dir, "labels", "train")
    test_labels_dir = os.path.join(source_dir, "labels", "test")

    # Create output directory structure
    output_images_dir = os.path.join(output_dir, "images")
    output_labels_dir = os.path.join(output_dir, "labels")

    for split in ["train", "test", "val"]:
        os.makedirs(os.path.join(output_images_dir, split), exist_ok=True)
        os.makedirs(os.path.join(output_labels_dir, split), exist_ok=True)

    # Function to get available images with matching labels
    def get_matching_files(img_dir, label_dir):
        # Get list of image files
        image_files = [f for f in os.listdir(img_dir)
                      if os.path.isfile(os.path.join(img_dir, f)) and
                      any(f.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.bmp', '.JPG'])]

        # Get list of annotation files
        label_files = [f for f in os.listdir(label_dir)
                     if os.path.isfile(os.path.join(label_dir, f))]

        # Get base names of label files without extension
        label_bases = [os.path.splitext(f)[0] for f in label_files]

        # Filter images that have corresponding labels
        matched_images = []
        for img in image_files:
            img_base = os.path.splitext(img)[0]
            if img_base in label_bases:
                matched_images.append(img)

        return matched_images

    # Get images with matching labels
    train_matched_images = get_matching_files(train_images_dir, train_labels_dir)
    test_matched_images = get_matching_files(test_images_dir, test_labels_dir)

    print(f"Found {len(train_matched_images)} training images with matching labels")
    print(f"Found {len(test_matched_images)} test images with matching labels")

    # Check if we have enough images
    if len(train_matched_images) < train_sample_size:
        raise ValueError(f"Not enough training images with labels. Requested: {train_sample_size}, Available: {len(train_matched_images)}")

    if len(test_matched_images) < (test_sample_size + val_size):
        raise ValueError(f"Not enough test images with labels. Requested: {test_sample_size + val_size}, Available: {len(test_matched_images)}")

    # Shuffle and sample images
    random.shuffle(train_matched_images)
    random.shuffle(test_matched_images)

    train_files = train_matched_images[:train_sample_size]
    test_files = test_matched_images[:test_sample_size]
    val_files = test_matched_images[test_sample_size:test_sample_size + val_size]

    # Function to copy files to destination
    def copy_files(image_files, src_img_dir, src_label_dir, dst_split):
        for img_file in image_files:
            # Get base filename without extension
            base_name = os.path.splitext(img_file)[0]

            # Source paths
            img_src = os.path.join(src_img_dir, img_file)

            # Find corresponding label file
            label_file = None
            for ext in ['.txt', '.xml', '.json']:
                potential_label = base_name + ext
                if os.path.exists(os.path.join(src_label_dir, potential_label)):
                    label_file = potential_label
                    break

            if label_file is None:
                print(f"Warning: No annotation file found for {img_file}. Skipping.")
                continue

            label_src = os.path.join(src_label_dir, label_file)

            # Destination paths
            img_dst = os.path.join(output_images_dir, dst_split, img_file)
            label_dst = os.path.join(output_labels_dir, dst_split, label_file)

            # Copy files
            shutil.copy2(img_src, img_dst)
            shutil.copy2(label_src, label_dst)

    # Copy files to respective directories
    copy_files(train_files, train_images_dir, train_labels_dir, "train")
    copy_files(test_files, test_images_dir, test_labels_dir, "test")
    copy_files(val_files, test_images_dir, test_labels_dir, "val")

    print(f"Dataset split complete:")
    print(f"  - Training: {len(train_files)} images")
    print(f"  - Testing: {len(test_files)} images")
    print(f"  - Validation: {len(val_files)} images")

    return train_files, test_files, val_files
