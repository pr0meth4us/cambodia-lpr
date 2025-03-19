from detect import load_model, detect_plate
from ocr import read_plate

def process_image(model, image_path):
    """Detect and read the license plate from the image."""
    boxes = detect_plate(model, image_path)
    if len(boxes) == 0:
        return "No plate detected"
    plate_box = boxes[0]
    plate_text = read_plate(image_path, plate_box)
    return plate_text

if __name__ == "__main__":
    # Example usage
    model = load_model('models/trained_model.pt')
    result = process_image(model, 'data/test/test_image.jpg')
    print("Pipeline result:", result)