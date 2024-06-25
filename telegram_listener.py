import os
from dotenv import load_dotenv
from telethon import TelegramClient, events

# Load environment variables from .env file
load_dotenv()

api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')
phone_number = os.getenv('TELEGRAM_PHONE_NUMBER')
channel_ids = os.getenv('TELEGRAM_CHANNEL_IDS').split(',')  # Split comma-separated channel IDs
channel_ids = [int(channel_id) for channel_id in channel_ids]  # Convert to list of integers

# Create the client and connect
client = TelegramClient('session_name', api_id, api_hash)

async def start_telegram_listener():
    # Log in to Telegram
    await client.start(phone_number)

    # Ensure you're authorized
    if not await client.is_user_authorized():
        await client.send_code_request(phone_number)
        code = input('Enter the code: ')
        await client.sign_in(phone_number, code)

    # Get the channel entities using channel IDs
    channels = []
    for channel_id in channel_ids:
        channel = await client.get_entity(channel_id)
        channels.append(channel)

    # Fetch and process messages for each channel
    for channel in channels:
        @client.on(events.NewMessage(chats=channel))
        async def handler(event):
            message = event.message.message
            process_message(message, channel)

    print('Listening for new messages...')
    await client.run_until_disconnected()

def process_message(message: str, channel) -> None:
    print(f"Processed message from {channel.title}: {message}")

# Make the client accessible from other modules
telegram_client = client
