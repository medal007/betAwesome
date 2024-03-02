import os
import re
import threading

from telethon.sync import TelegramClient, events
from googletrans import Translator
import asyncio
from datetime import datetime
import ssl
import time

from selenium import webdriver

from datetime import datetime, timedelta


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
from selenium.common.exceptions import TimeoutException

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


def type_amount(driver, path, value=""):
    enter_field = driver.find_element("xpath", path)
    enter_field.clear()
    enter_field.send_keys(Keys.BACKSPACE)  # Simulate backspace
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

#Disable comment for Demo Account
#url = "https://pocketoption.com/en/cabinet/demo-quick-high-low/"

url = "https://pocketoption.com/en/cabinet/quick-high-low/"

type_field(driver, "//input[@placeholder='Email *']", "tmedal007@gmail.com")

type_field(driver, "//input[@placeholder='Password *']", "M2d1l@119500")

click(driver, "//button[normalize-space()='Sign In']")

time.sleep(8)

driver.get(url)

time.sleep(2)

click(driver, "//div[@class='block__control control js-tour-block--expiration-inputs']//a")

api_id = '19692955'
api_hash = '28879afa9679b80fdb5e55810f322808'
phone_number = '+23278672866'

client = TelegramClient('session_name', api_id, api_hash)

import time


def check_dynamic_value(driver, max_attempts=1):
    attempts = 0
    while attempts < max_attempts:
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='centered']"))
            )
            dynamic_value = element.text
        except TimeoutException:
            dynamic_value = "1"

        try:
            dynamic_value = float(dynamic_value.replace('$', '').strip())
            dynamic_value = int(dynamic_value)
        except ValueError:
            dynamic_value = 0

        if dynamic_value > 0:
            result = "Won"
        else:
            result = "Lost"

        return result

        attempts += 1  # Increment attempts
        #time.sleep(1)  # Wait before the next attempt

    # If max_attempts is reached without success, log or handle the failure
    print("Maximum attempts reached without success")
    return None

level = 0


async def handle_new_messages(event):
    try:
        global last_processed_message_id
        global level

        channel_id = event.chat_id
        message_id = event.message.id

        # Proceed with message processing
        print(f"Channel ID: {channel_id}")
        print(f"Channel Name: {event.chat.title}")
        print(f"Channel Message: {event.message.message}")
        message = event.message.message

        if "SESSION" in message and "STARTED" in message:
            print("A Session has Started Let's go !!!")

        # Extract asset
        asset_match = re.search(r'[\U0001F1E6-\U0001F1FF]+ ([A-Z&/]+)', message, re.IGNORECASE)
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

        expiration = expiration.replace("M", "")

        print("Asset:", asset)
        print("Expiration:", expiration)
        print("Entry:", entry1)
        print("Signal:", signal)
        print("Level 1:", level1)
        print("Level 2:", level2)
        print("Level 3:", level3)

        click(driver, "//span[@class='current-symbol current-symbol_cropped']")
        type_field(driver, "//input[@placeholder='Search']", asset)

        click(driver, "//div[@id='modal-root']//li[1]//a[1]")
        time.sleep(5)
        driver.get(url)

        if level == 0:
            type_amount(driver, "//input[@value='$2']", "2")
            level = 0

        if level == 1:
            type_amount(driver, "//input[@value='$4']", "2")
            level = 0

        if level == 2:
            type_amount(driver, "//input[@value='$8']", "2")
            level = 0

        if level == 3:
            type_amount(driver, "//input[@value='$16']", "2")
            level = 0


        # Get the current time in UTC with seconds
        utc_now_with_seconds = datetime.utcnow()

        # Calculate the time difference for UTC-4 (4 hours behind UTC) with seconds
        utc_minus_4_with_seconds = utc_now_with_seconds - timedelta(hours=4)

        # Convert time_utc_minus_4 to datetime object
        time_utc_minus_4_with_seconds_obj = utc_minus_4_with_seconds.strftime('%H:%M:%S')

        # Convert entry time to datetime object without seconds
        entry1_obj = datetime.strptime(entry1, '%H:%M')

        # Calculate the time difference
        time_difference = entry1_obj - datetime.strptime(time_utc_minus_4_with_seconds_obj, '%H:%M:%S')

        # Extract the total seconds from the timedelta object
        seconds_difference = abs(time_difference.total_seconds())

        print(f"Seconds difference: {seconds_difference}")

        time.sleep(int(seconds_difference))

        if "HIGH" in signal:
            click(driver, "//a[@class='btn btn-call']//span[@class='switch-state-block__item']")
        elif "LOW" in signal:
            click(driver, "//a[@class='btn btn-put']//span[@class='switch-state-block__item']")

        seconds_next = int(expiration) * 60

        time.sleep(int(seconds_next) - 1)

        checkwin = check_dynamic_value(driver)  # Call the function
        print(checkwin)

        if "Lost" in checkwin:
            level = 1

            type_amount(driver, "//input[@value='$2']", "4")

            time.sleep(2)

            if "HIGH" in signal:
                click(driver, "//a[@class='btn btn-call']//span[@class='switch-state-block__item']")
            elif "LOW" in signal:
                click(driver, "//a[@class='btn btn-put']//span[@class='switch-state-block__item']")

            seconds_next = int(expiration) * 60

            time.sleep(int(seconds_next) - 1)

            checkwin = check_dynamic_value(driver)  # Call the function
            print(checkwin)

            if "Lost" in checkwin:
                level = 2
                type_amount(driver, "//input[@value='$4']", "8")

                time.sleep(2)
                if "HIGH" in signal:
                    click(driver, "//a[@class='btn btn-call']//span[@class='switch-state-block__item']")
                elif "LOW" in signal:
                    click(driver, "//a[@class='btn btn-put']//span[@class='switch-state-block__item']")

                seconds_next = int(expiration) * 60

                time.sleep(int(seconds_next) - 1)

                checkwin = check_dynamic_value(driver)  # Call the function
                print(checkwin)

                if "Lost" in checkwin:
                    level = 3
                    type_amount(driver, "//input[@value='$8']", "16")

                    time.sleep(2)
                    if "HIGH" in signal:
                        click(driver, "//a[@class='btn btn-call']//span[@class='switch-state-block__item']")
                    elif "LOW" in signal:
                        click(driver, "//a[@class='btn btn-put']//span[@class='switch-state-block__item']")

                    seconds_next = int(expiration) * 60

                    time.sleep(int(seconds_next) - 1)

                    checkwin = check_dynamic_value(driver)  # Call the function
                    print(checkwin)

    except Exception as e:
        print(f"Error processing message: {e}")

async def main():
    try:
        await client.start(phone_number)

        # Replace the channel IDs in the list with the ones you want to monitor
        channel_ids_to_monitor = ['2074799242']

        for channel_id in channel_ids_to_monitor:
            client.add_event_handler(handle_new_messages, events.NewMessage(incoming=True, chats=int(channel_id)))

        # Run the client until Ctrl+C is pressed
        await client.run_until_disconnected()

    except Exception as e:
        print(f"Error during execution: {e}")


if __name__ == '__main__':
    asyncio.run(main())
