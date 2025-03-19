import cv2
from yolov5 import YOLOv5  # Adjust import based on your YOLO version

def load_model(model_path):
    """Load the trained YOLO model."""
    return YOLOv5(model_path)

def detect_plate(model, image_path):
    """Detect license plates and return bounding boxes."""
    img = cv2.imread(image_path)
    results = model(img)
    boxes = results.xyxy[0].numpy()  # [x1, y1, x2, y2, confidence, class]
    return boxes

if __name__ == "__main__":
    # Example usage
    model = load_model('models/trained_model.pt')
    boxes = detect_plate(model, 'data/test/test_image.jpg')
    print("Detected boxes:", boxes)