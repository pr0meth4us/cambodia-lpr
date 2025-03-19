from yolov5 import YOLOv5  # Adjust import based on your YOLO version

def train_model(data_yaml, epochs=50, batch_size=16):
    """Train the YOLO model on the provided dataset."""
    model = YOLOv5('models/yolov5s.pt')  # Load pre-trained model
    model.train(data=data_yaml, epochs=epochs, batch_size=batch_size)
    model.save('models/trained_model.pt')
    print("Training completed and model saved.")

if __name__ == "__main__":
    # Example usage
    train_model('cambodian_plates.yaml')