import os
import asyncio
from telethon.sync import TelegramClient, events

api_id = '19692955'
api_hash = '28879afa9679b80fdb5e55810f322808'
phone_number = '+23278672866'

client = TelegramClient('session_name', api_id, api_hash)

async def handle_new_messages(event):
    try:
        # Check if the message is from a channel and if you are an admin
        if event.chat and event.chat.admin_rights:
            print(f"Channel ID: {event.chat_id}")
            print(f"Channel Name: {event.chat.title}")
    except Exception as e:
        print(f"Error processing message: {e}")

async def main():
    try:
        await client.start(phone_number)

        # Handle all incoming messages without specifying specific channel IDs
        client.add_event_handler(handle_new_messages, events.NewMessage(incoming=True))

        # Run the client until Ctrl+C is pressed
        await client.run_until_disconnected()

    except Exception as e:
        print(f"Error during execution: {e}")

if __name__ == '__main__':
    asyncio.run(main())
