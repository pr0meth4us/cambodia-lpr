import requests
import os
import io
from PIL import Image

# Configuration (replace with environment variables in production)
CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'
REDIRECT_URI = 'your_redirect_uri'
AUTH_CODE = 'your_auth_code'

def get_access_token():
    """Exchange authorization code for an access token."""
    token_url = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
    payload = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': AUTH_CODE,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code'
    }
    response = requests.post(token_url, data=payload)
    return response.json()['access_token']

def list_files(access_token, folder_path):
    """List files in the specified OneDrive folder."""
    headers = {'Authorization': f'Bearer {access_token}'}
    url = f'https://graph.microsoft.com/v1.0/me/drive/root:{folder_path}:/children'
    response = requests.get(url, headers=headers)
    return response.json()['value']

def download_image(file, output_dir):
    """Download the image to the specified directory."""
    download_url = file['@microsoft.graph.downloadUrl']
    img_data = requests.get(download_url).content
    output_path = os.path.join(output_dir, file['name'])
    with open(output_path, 'wb') as f:
        f.write(img_data)
    print(f"Downloaded {file['name']} to {output_path}")

def retrieve_images_from_onedrive(folder_path, output_dir):
    """Retrieve images from OneDrive and save to local directory."""
    access_token = get_access_token()
    files = list_files(access_token, folder_path)
    os.makedirs(output_dir, exist_ok=True)
    for file in files:
        if file['name'].endswith(('.jpg', '.png')):
            download_image(file, output_dir)

if __name__ == "__main__":
    # Example usage
    retrieve_images_from_onedrive('/LicensePlateImages', 'data/raw_images')