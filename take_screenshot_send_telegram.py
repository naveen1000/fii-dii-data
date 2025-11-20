#!/usr/bin/env python3
"""Take a screenshot of an element by XPath and send it to Telegram via bot API.

Usage:
  - Set environment variables `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`,
    or pass `--token` and `--chat` on the command line.
  - Run: `python take_screenshot_send_telegram.py`
"""
from __future__ import annotations
import os
import time
import argparse
import requests
import platform
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

URL = "https://web.sensibull.com/fii-dii-data"
XPATH = '//*[@id="radix-4-content-summary"]/div/div/div[2]'

def create_driver(headless=False, window_size=(1366, 900)):
    options = Options()
    # if headless:
    #     # Use new headless mode where available
    #     options.add_argument("--headless=new")

    #common options
    #options.add_argument(f"--window-size={window_size[0]},{window_size[1]}")
    #options.add_argument("--disable-gpu")
    #options.add_argument("--no-sandbox")
    #options.add_argument("--disable-dev-shm-usage")
    # Optional: reduce detection surface
    #options.add_argument("--disable-blink-features=AutomationControlled")

    system = platform.system()
    print(f"Detected OS: {system}")
    # For Windows
    if system == "Windows":
        CHROME_DATA_PATH = "user-data-dir=C:\\Users\\naveen.simma\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
        options.add_argument(CHROME_DATA_PATH)
        options.add_argument('--profile-directory=Profile 1')
        service = Service("D:\\projects\\Wapp\\chromedriver.exe")
    
    # For Ubuntu
    elif system == "Linux":
        CHROME_UBUNTU_USER_DATA_PATH = "/home/ubuntu/snap/chromium/common/chromium"
        UBUNTU_PROFILE_DIRECTORY = "Profile 1"
        options.add_argument(f"user-data-dir={CHROME_UBUNTU_USER_DATA_PATH}")
        options.add_argument(f"--profile-directory={UBUNTU_PROFILE_DIRECTORY}")
        options.binary_location = "/usr/bin/chromium-browser"
        service = Service("/usr/bin/chromedriver")

    driver = webdriver.Chrome(service=service, options=options)
    return driver



def screenshot_element_bytes(url: str, xpath: str, timeout: int = 20) -> bytes:

    driver = create_driver(headless="False")

    try:
        driver.get(url)

        wait = WebDriverWait(driver, timeout)
        time.sleep(15)  # Give the page some time to load additional content/scripts
        el = wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))

        # Scroll element into view and give the browser a moment to render
        driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'center'});", el)
        time.sleep(0.5)

        # Selenium 4: get PNG bytes directly from element
        png_bytes = el.screenshot_as_png
        return png_bytes
    finally:
        driver.quit()


def send_photo_bytes(bot_token: str, chat_id: str, png_bytes: bytes, caption: str | None = None) -> dict:
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    files = {"photo": ("element.png", png_bytes, "image/png")}
    data = {"chat_id": chat_id}
    if caption:
        data["caption"] = caption

    resp = requests.post(url, data=data, files=files, timeout=60)
    resp.raise_for_status()
    return resp.json()


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Screenshot XPath element and send to Telegram")
    p.add_argument("--url", default=URL, help="Page URL")
    p.add_argument("--xpath", default=XPATH, help="XPath of element")
    p.add_argument("--token", help="Telegram bot token (or set TELEGRAM_BOT_TOKEN env var)")
    p.add_argument("--chat", help="Telegram chat ID (or set TELEGRAM_CHAT_ID env var)")
    p.add_argument("--timeout", type=int, default=20, help="Element wait timeout seconds")
    p.add_argument("--caption", default=None, help="Optional caption for Telegram photo")
    return p.parse_args()


def main() -> None:
    args = parse_args()

    bot_token = "6868135069:AAGmILI1EvYaHdYitntNIl3Bo8Nmm13caiA"
    chat_id = "582942300"
    if not bot_token or not chat_id:
        raise SystemExit("Provide Telegram bot token and chat id via args or TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID env vars")

    print(f"Loading page and capturing element: {args.xpath}")
    png = screenshot_element_bytes(args.url, args.xpath, timeout=args.timeout)
    print(f"Captured {len(png)} bytes, sending to Telegram chat {chat_id}...")

    result = send_photo_bytes(bot_token, chat_id, png, caption=args.caption)
    print("Telegram response:", result)


if __name__ == "__main__":
    main()
