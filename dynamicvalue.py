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
from selenium.common import ElementNotVisibleException, ElementNotSelectableException, NoSuchElementException, \
    TimeoutException
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

print("Pocket Option Dynamic Win Check Client Initiated")

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

url = "https://pocketoption.com/en/cabinet/demo-quick-high-low/"

type_field(driver, "//input[@placeholder='Email *']", "tmedal007@gmail.com")

type_field(driver, "//input[@placeholder='Password *']", "M2d1l@119500")

click(driver, "//button[normalize-space()='Sign In']")

time.sleep(10)

driver.get(url)


# Function to continuously check for a particular XPath
async def check_dynamic_value(driver):
    while True:
        try:
            # Wait until the desired element is located
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='centered']"))
            )
            dynamic_value = element.text
        except TimeoutException:
            try:
                # If the first XPath fails, try the second XPath
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@class='centered price-up']"))
                )
                dynamic_value = element.text
            except TimeoutException:
                # If both XPaths fail, set dynamic_value to "0" and continue the loop
                dynamic_value = "0"
                continue

        # Convert dynamic_value to an integer
        try:
            dynamic_value = float(dynamic_value.replace('$', '').strip())  # Remove "$" and any leading/trailing spaces
            dynamic_value = int(dynamic_value)  # Convert to integer
        except ValueError:
            # If conversion fails, set dynamic_value to 0
            dynamic_value = 0

        # Determine result based on dynamic value
        result = "Won" if dynamic_value > 0 else "Lost"

        return result

        await asyncio.sleep(0)  # Non-blocking sleep to allow other tasks to run

async def main():
    try:
        # Start the function to check for the dynamic value
        await check_dynamic_value(driver)

    except Exception as e:
        print(f"Error during execution: {e}")

if __name__ == '__main__':
    asyncio.run(main())
