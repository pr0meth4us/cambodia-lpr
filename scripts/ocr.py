import pytesseract
import cv2

def read_plate(image_path, box):
    """Extract text from the license plate using OCR."""
    img = cv2.imread(image_path)
    x1, y1, x2, y2 = map(int, box[:4])
    plate_img = img[y1:y2, x1:x2]
    text = pytesseract.image_to_string(plate_img, config='--psm 8')
    return text.strip()

if __name__ == "__main__":
    # Example usage (assumes boxes from detect.py)
    boxes = [[50, 50, 150, 100, 0.95, 0]]  # Dummy box [x1, y1, x2, y2, conf, class]
    plate_text = read_plate('data/test/test_image.jpg', boxes[0])
    print("Detected plate text:", plate_text)