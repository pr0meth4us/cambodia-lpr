import os
import subprocess

def check_labelimg_installed():
    """Check if LabelImg is installed."""
    try:
        subprocess.run(['labelimg', '--version'], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_labelimg_instructions():
    """Print instructions to install LabelImg."""
    print("LabelImg is not installed. Install it with:")
    print("  pip install labelImg")
    print("Then run it with: labelimg")

def annotate_images(image_dir, annotation_dir):
    """Guide the user to annotate images using LabelImg."""
    os.makedirs(annotation_dir, exist_ok=True)
    if not check_labelimg_installed():
        install_labelimg_instructions()
        return

    print("Opening LabelImg for annotation...")
    print(f"1. Load images from: {image_dir}")
    print(f"2. Save annotations to: {annotation_dir}")
    print("3. Draw bounding boxes around license plates and label them as 'plate'.")
    print("4. Save annotations in YOLO format (TXT files).")
    subprocess.run(['labelimg', image_dir, annotation_dir])

if __name__ == "__main__":
    config = load_config('config.yaml')
    image_dir = config['paths']['processed_images']
    annotation_dir = config['paths']['annotations']
    annotate_images(image_dir, annotation_dir)