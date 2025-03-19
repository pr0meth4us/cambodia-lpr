# Cambodian License Plate Recognition
A project to detect and recognize Cambodian license plates using YOLO and OCR, with OneDrive integration for image retrieval.

## Setup
1. Clone the repository: `git clone <repo-url>`
2. Install dependencies: `pip install -r requirements.txt`
3. Configure `config.yaml` with your paths and parameters.
4. Set up OneDrive API credentials in `onedrive_api.py`.

## Usage
- Retrieve images: `python scripts/onedrive_api.py`
- Preprocess data: `python scripts/preprocess.py`
- Train model: `python scripts/train.py`
- Run pipeline: `python scripts/pipeline.py`