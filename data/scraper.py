import os
import time
import requests
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

SAVE_DIR = "downloaded_photos"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

chrome_options = Options()
chrome_options.add_argument("--start-maximized")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

def handle_captcha():
    """Detect and manually solve the CAPTCHA challenge."""
    try:
        print("Checking for CAPTCHA challenge...")
        # Wait for CAPTCHA input field to be present
        captcha_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='captcha_response']"))
        )
        captcha_image = driver.find_element(By.CSS_SELECTOR, "img[src*='captcha']")
        captcha_url = captcha_image.get_attribute("src")
        print(f"CAPTCHA Image URL: {captcha_url}")

        response = requests.get(captcha_url, stream=True)
        captcha_path = os.path.join(SAVE_DIR, "captcha.jpg")
        with open(captcha_path, "wb") as f:
            f.write(response.content)
        print(f"CAPTCHA saved to {captcha_path}")

        captcha_text = input("Enter the CAPTCHA text from the image: ")
        captcha_input.send_keys(captcha_text)

        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        print("CAPTCHA submitted. Waiting for login confirmation...")
        time.sleep(5)
    except Exception as e:
        print(f"Error handling CAPTCHA: {e}")

def handle_login_modal(email, password):
    """Handle the login popup by waiting for the login form and entering credentials."""
    try:
        print("Waiting for login popup to appear...")
        login_form = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "login_popup_cta_form"))
        )
        email_field = login_form.find_element(By.CSS_SELECTOR, "input[name='email']")
        email_field.clear()
        email_field.send_keys(email)
        print("Email entered.")

        password_field = login_form.find_element(By.CSS_SELECTOR, "input[name='pass']")
        password_field.clear()
        password_field.send_keys(password)
        print("Password entered.")

        login_button = login_form.find_element(By.XPATH, ".//div[@aria-label='Accessible login button']")
        login_button.click()
        print("Login button clicked.")

        WebDriverWait(driver, 15).until(EC.invisibility_of_element(login_form))
        print("Login successful!")

        # Check if a CAPTCHA challenge appears (if so, handle it)
        try:
            handle_captcha()
        except Exception:
            # If no CAPTCHA, move on
            pass

    except Exception as e:
        print(f"Error during login: {e}")

def download_image(img_url, idx):
    """Download an image from a URL."""
    try:
        response = requests.get(img_url, stream=True)
        if response.status_code == 200:
            filename = os.path.join(SAVE_DIR, f"photo_{idx}.jpg")
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"Downloaded: {filename}")
        else:
            print(f"Failed to download {img_url}: Status {response.status_code}")
    except Exception as e:
        print(f"Error downloading {img_url}: {e}")

def scroll_and_download_photos(url):
    """Load the page, log in, then scroll continuously and download images concurrently."""
    driver.get(url)
    print(f"Loading page: {url}")
    time.sleep(3)

    handle_login_modal("", "")
    time.sleep(5)

    downloaded_urls = set()
    img_counter = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        last_height = driver.execute_script("return document.body.scrollHeight")
        scroll_attempts = 0
        max_scroll_attempts = 10

        while scroll_attempts < max_scroll_attempts:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            new_height = driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                scroll_attempts += 1
            else:
                scroll_attempts = 0

            last_height = new_height
            print(f"Scrolling... Current page height: {new_height}")

            image_elements = driver.find_elements(By.TAG_NAME, "img")
            print(f"Found {len(image_elements)} images so far.")

            for img in image_elements:
                img_url = img.get_attribute("src")
                if img_url and "fbcdn.net" in img_url and img_url not in downloaded_urls:
                    downloaded_urls.add(img_url)
                    img_counter += 1
                    executor.submit(download_image, img_url, img_counter)

        executor.shutdown(wait=True)
        print("Scrolling finished and all images downloaded.")

if __name__ == "__main__":
    target_url = "https://www.facebook.com/trafficspy/photos"
    scroll_and_download_photos(target_url)
    driver.quit()
    print("Scraping completed!")
