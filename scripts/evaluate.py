import pandas as pd
from pipeline import process_image

def evaluate_model(model, test_dir, ground_truth_csv):
    """Evaluate the model on the test set."""
    ground_truth = pd.read_csv(ground_truth_csv)
    correct = 0
    total = len(ground_truth)

    for index, row in ground_truth.iterrows():
        image_path = row['image_path']
        actual_plate = row['plate_number']
        predicted_plate = process_image(model, image_path)
        if predicted_plate == actual_plate:
            correct += 1

    accuracy = correct / total
    with open('evaluation/results.txt', 'w') as f:
        f.write(f"Accuracy: {accuracy * 100:.2f}%\n")
    print(f"Accuracy: {accuracy * 100:.2f}%")

if __name__ == "__main__":
    # Example usage
    model = load_model('models/trained_model.pt')
    evaluate_model(model, 'data/test', 'data/ground_truth.csv')