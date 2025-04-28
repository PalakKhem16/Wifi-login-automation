import subprocess
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

def connect_to_wifi(ssid):
    connect_command = f'netsh wlan connect name="{ssid}"'
    subprocess.run(connect_command, shell=True)
    time.sleep(5)
    print(f"📡 Connected to Wi-Fi: {ssid}!")

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

USERNAME = "23ucs055"
PASSWORD = "2ZGnqfmZ"

wifi_ssid = "GH"
connect_to_wifi(wifi_ssid)

driver_path = "C:\\chromedriver-win64\\chromedriver.exe"

chrome_options = Options()
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
chrome_options.accept_insecure_certs = True

service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

url = "https://172.22.2.6/connect/PortalMain"
print("🌐 Opening Wi-Fi portal...")
driver.get(url)

wait = WebDriverWait(driver, 10)
time.sleep(2)

try:
    print("⌨️ Typing username...")
    username_field = wait.until(EC.presence_of_element_located((By.ID, "LoginUserPassword_auth_username")))
    username_field.clear()
    username_field.send_keys(USERNAME)

    print("🔑 Typing password...")
    password_field = wait.until(EC.presence_of_element_located((By.ID, "LoginUserPassword_auth_password")))
    password_field.clear()
    password_field.send_keys(PASSWORD)

    print("🖱️ Clicking login button...")
    login_button = wait.until(EC.element_to_be_clickable((By.ID, "UserCheck_Login_Button_span")))
    login_button.click()

    WebDriverWait(driver, 10).until(EC.invisibility_of_element((By.ID, "LoginUserPassword_auth_username")))

    success_keywords = ["internet", "access", "granted", "portal", "connected"]
    page_loaded = False

    for keyword in success_keywords:
        try:
            WebDriverWait(driver, 5).until(
                EC.text_to_be_present_in_element((By.TAG_NAME, "body"), keyword)
            )
            page_loaded = True
            break
        except:
            continue

    if page_loaded:
        print("✅ Login successful! Portal access granted.")
    else:
        print("⚠️ Login form disappeared but success text not detected. Assuming login success.")

except Exception as e:
    print(f"❌ Login may have failed or something went wrong: {e}")

finally:
    driver.quit()
    print("🛑 Browser closed.")
