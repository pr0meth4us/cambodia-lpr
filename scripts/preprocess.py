import cv2
import os
import numpy as np
from utils.helpers import load_config

def resize_image(image_path, size=(224, 224)):
    """Resize an image to the specified dimensions."""
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Failed to load image: {image_path}")
    return cv2.resize(img, size)

def normalize_image(image):
    """Normalize pixel values to the range [0, 1]."""
    return image / 255.0

def preprocess_images(input_dir, output_dir, size=(224, 224)):
    """Preprocess all images in the input directory and save to the output directory."""
    os.makedirs(output_dir, exist_ok=True)
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.jpg', '.png')):
            img_path = os.path.join(input_dir, filename)
            try:
                img = resize_image(img_path, size)
                img_normalized = normalize_image(img)
                output_path = os.path.join(output_dir, filename)
                # Save as uint8 for compatibility
                cv2.imwrite(output_path, (img_normalized * 255).astype(np.uint8))
                print(f"Preprocessed {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    config = load_config('config.yaml')
    input_dir = config['paths']['raw_images']
    output_dir = config['paths']['processed_images']
    preprocess_images(input_dir, output_dir)