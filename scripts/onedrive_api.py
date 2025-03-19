import requests
import os
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'
REDIRECT_URI = 'http://localhost:8000'  # Local server for redirect
TOKEN_FILE = 'onedrive_token.json'  # File to store tokens

# Global variable to store the auth code
auth_code = None

class OAuthHandler(BaseHTTPRequestHandler):
    """Handle the redirect from Microsoft to capture the auth code."""
    def do_GET(self):
        global auth_code
        query = urlparse(self.path).query
        params = parse_qs(query)
        auth_code = params.get('code', [None])[0]
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Authorization successful! You can close this window.")

def start_local_server():
    """Start a local server to capture the auth code."""
    server = HTTPServer(('localhost', 8000), OAuthHandler)
    server.handle_request()  # Handle one request and stop
    return auth_code

def get_auth_code():
    """Open browser and get auth code automatically."""
    auth_url = (
        f"https://login.microsoftonline.com/common/oauth2/v2.0/authorize?"
        f"client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}"
        f"&scope=Files.Read.All offline_access"
    )
    webbrowser.open(auth_url)
    return start_local_server()

def get_access_token(auth_code=None, refresh_token=None):
    """Obtain or refresh an access token."""
    token_url = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
    if auth_code:  # Initial token request
        payload = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'code': auth_code,
            'redirect_uri': REDIRECT_URI,
            'grant_type': 'authorization_code'
        }
    elif refresh_token:  # Refresh token request
        payload = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'refresh_token': refresh_token,
            'grant_type': 'refresh_token'
        }
    else:
        raise ValueError("Either auth_code or refresh_token must be provided")

    response = requests.post(token_url, data=payload)
    if response.status_code != 200:
        raise Exception(f"Failed to get token: {response.text}")
    tokens = response.json()
    # Save tokens to file
    with open(TOKEN_FILE, 'w') as f:
        import json
        json.dump(tokens, f)
    return tokens['access_token'], tokens.get('refresh_token')

def load_tokens():
    """Load existing tokens from file if available."""
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as f:
            import json
            return json.load(f)
    return None

def list_files(access_token, folder_path):
    """List files in the specified OneDrive folder."""
    headers = {'Authorization': f'Bearer {access_token}'}
    url = f'https://graph.microsoft.com/v1.0/me/drive/root:{folder_path}:/children'
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to list files: {response.text}")
    return response.json()['value']

def download_image(file, output_dir):
    """Download an image from OneDrive to the output directory."""
    download_url = file['@microsoft.graph.downloadUrl']
    img_data = requests.get(download_url).content
    output_path = os.path.join(output_dir, file['name'])
    with open(output_path, 'wb') as f:
        f.write(img_data)
    print(f"Downloaded {file['name']} to {output_path}")

def retrieve_images_from_onedrive(folder_path, output_dir):
    """Retrieve all images from a OneDrive folder."""
    os.makedirs(output_dir, exist_ok=True)

    # Check for existing tokens
    tokens = load_tokens()
    if tokens and 'refresh_token' in tokens:
        access_token, refresh_token = get_access_token(refresh_token=tokens['refresh_token'])
    else:
        # Get new auth code and tokens
        auth_code = get_auth_code()
        access_token, refresh_token = get_access_token(auth_code=auth_code)

    files = list_files(access_token, folder_path)
    for file in files:
        if file['name'].lower().endswith(('.jpg', '.png')):
            download_image(file, output_dir)

if __name__ == "__main__":
    retrieve_images_from_onedrive('/LicensePlateImages', 'data/raw_images')