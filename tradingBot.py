import os
import re

from telethon.sync import TelegramClient, events
from googletrans import Translator
import asyncio
from datetime import datetime
import ssl
import time

from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

# Create an instance of the webdriver
from selenium.common import ElementNotVisibleException, ElementNotSelectableException
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

current_time = datetime.now()

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE


options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')
#options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

driver.get("https://pocketoption.com/en/login")

# Wait for the page to fully load
driver.implicitly_wait(50)

print("Pocket Option Selenium Client Initiated")

wait = WebDriverWait(driver, timeout=50, poll_frequency=1,
                     ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException])

driver.maximize_window()

def type_field(driver, path, value=""):
    enter_field = driver.find_element("xpath", path)
    enter_field.clear()
    enter_field.send_keys(value)
    return enter_field

def click(driver, path):
    # Find the login button and click it
    click_button = driver.find_element("xpath", path)
    click_button.click()
    return click_button

def select_text(driver, path, text=""):
    select_text = driver.find_element("xpath", path)
    selected = Select(select_text)
    selected.select_by_visible_text(text)
    return select_text



type_field(driver, "//input[@placeholder='Email *']", "tmedal007@gmail.com")

type_field(driver, "//input[@placeholder='Password *']", "M2d1l@119500")

click(driver, "//button[normalize-space()='Sign In']")

time.sleep(10)

driver.get("https://pocketoption.com/en/cabinet/demo-quick-high-low/")

api_id = '19692955'
api_hash = '28879afa9679b80fdb5e55810f322808'
phone_number = '+23278672866'

client = TelegramClient('session_name', api_id, api_hash)

async def handle_new_messages(event):
    try:
        print(f"Channel ID: {event.chat_id}")
        print(f"Channel Name: {event.chat.title}")
        print(f"Channel Message: {event.message.message}")

        message = event.message.message

        if "SESSION" in message and "STARTED" in message:
            print("A Session has Started Let's go !!!")

        # Extract asset
        asset_match = re.search(r'[🇳🇿🇬🇧🇦🇷🇦🇺🇪🇺]+ ([A-Za-z/]+)(?: [🇯🇵🇺🇸🇬🇧🇦🇷🇦🇺🇪🇺🇭🇺]+)?(?: OTC)?', message, re.IGNORECASE)
        asset = asset_match.group(1) if asset_match else None

        # Extract expiration
        expiration_match = re.search(r'Expiration (\d+M)', message)
        expiration = expiration_match.group(1) if expiration_match else None

        # Extract entry
        entry_match = re.search(r'Entry at (\d{2}:\d{2})', message)
        entry1 = entry_match.group(1) if entry_match else None

        # Extract signal (HIGHER or LOWER)
        signal_match = re.search(r'(HIGHER|LOWER)', message)
        signal = signal_match.group(1) if signal_match else None

        # Extract levels
        levels = re.findall(r'level at (\d{2}:\d{2})', message)

        # Assign to variables
        level1 = levels[0] if levels else None
        level2 = levels[1] if len(levels) > 1 else None
        level3 = levels[2] if len(levels) > 2 else None

        print("Asset:", asset)
        print("Expiration:", expiration)
        print("Entry:", entry1)
        print("Signal:", signal)
        print("Level 1:", level1)
        print("Level 2:", level2)
        print("Level 3:", level3)

    except Exception as e:
        print(f"Error processing message: {e}")


async def main():
    try:
        await client.start(phone_number)

        # Replace the channel IDs in the list with the ones you want to monitor
        channel_ids_to_monitor = ['1995228403']

        for channel_id in channel_ids_to_monitor:
            client.add_event_handler(handle_new_messages, events.NewMessage(incoming=True, chats=int(channel_id)))

        # Run the client until Ctrl+C is pressed
        await client.run_until_disconnected()

    except Exception as e:
        print(f"Error during execution: {e}")


if __name__ == '__main__':
    asyncio.run(main())
