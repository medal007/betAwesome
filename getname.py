from telethon.sync import TelegramClient

api_id = '19692955'
api_hash = '28879afa9679b80fdb5e55810f322808'
phone_number = '+23278672866'

client = TelegramClient('session_name', api_id, api_hash)

async def get_channel_info():
    await client.start(phone_number)

    async for dialog in client.iter_dialogs():
        if dialog.is_channel and dialog.entity.broadcast:
            print("Channel ID:", dialog.entity.id)
            print("Channel Name:", dialog.entity.title)

    await client.disconnect()

with client:
    client.loop.run_until_complete(get_channel_info())
