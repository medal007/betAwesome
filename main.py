import os

from telethon.sync import TelegramClient, events
from googletrans import Translator
import asyncio
import pytesseract
from PIL import Image
import numpy as np
import cv2
import re
import spacy
from yandex.Translater import Translater

api_id = '19692955'
api_hash = '28879afa9679b80fdb5e55810f322808'
phone_number = '+23278672866'

client = TelegramClient('session_name', api_id, api_hash)
translator = Translator()

tr = Translater()
tr.set_key(
    'trnsl.1.1.20220417T164612Z.69086f111f56571a.4594f31ebe145f1f782c4f234099e31476bd2106')  # Api key found on https://translate.yandex.com/developers/keys

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


async def handle_new_messages(event):
    try:
        # Get the new message from the event
        message = event.message

        # Check if the message has any type of media
        if message.media:
            print(f"Channel ID: {event.chat_id}")
            print(f"Channel Name: {event.chat.title}")

            # Determine the type of media and handle accordingly
            if message.photo:
                # Download and save the full photo (largest size)
                file_path = f"photo_{message.id}.jpg"
                await message.download_media(file=file_path)
                print(f"Downloaded full photo: {file_path}")

                # Use OCR to extract text from the image
                extracted_text = ocr_from_image(file_path)
                image = cv2.imread(file_path)

                # Convert the image to grayscale
                gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                # Adaptive Thresholding
                thresholded_image = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                          cv2.THRESH_BINARY, 11, 2)

                # Morphological Operations
                kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
                processed_image = cv2.morphologyEx(gray_image, cv2.MORPH_OPEN, kernel, iterations=1)
                inverted_image = 255 - processed_image

                # OCR on the preprocessed image
                text = pytesseract.image_to_string(inverted_image, lang="rus", config='--psm 6')

                tr.set_text(text)
                tr.set_from_lang('ru')
                tr.set_to_lang('en')

                translated = tr.translate()
                print(translated)

                # Send the translated text to yourself
                await client.send_message('cyberjunk', translated)
                await client.send_message('medalljunk', translated)
                await client.send_message('skrillamonk', translated)

                # Handle other types of media (e.g., document, audio, video) here

                # After you are done with the image, delete it
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"Image file {file_path} deleted.")
                else:
                    print(f"The file {file_path} does not exist.")

    except Exception as e:
        print(f"Error processing message: {e}")


def ocr_from_image(file_path):
    try:
        # Open the image using Pillow
        with Image.open(file_path) as img:
            # Use pytesseract to perform OCR on the image
            pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
            extracted_text = pytesseract.image_to_string(img, lang='eng')
            return extracted_text.strip()

    except Exception as e:
        print(f"Error performing OCR: {e}")
        return ''


async def main():
    try:
        await client.start(phone_number)

        # Replace the channel IDs in the list with the ones you want to monitor
        channel_ids_to_monitor = ['-1001995228403', '1116567708', '1946566534', '1304721965', '1323146821', '1486351346']

        for channel_id in channel_ids_to_monitor:
            client.add_event_handler(handle_new_messages, events.NewMessage(incoming=True, chats=int(channel_id)))

        # Run the client until Ctrl+C is pressed
        await client.run_until_disconnected()

    except Exception as e:
        print(f"Error during execution: {e}")


if __name__ == '__main__':
    asyncio.run(main())
