import os
from dotenv import load_dotenv
from telethon import TelegramClient, events
import logging
import asyncio
from message_processor import process_message

# Load environment variables from .env file
load_dotenv()

api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')
phone_number = os.getenv('TELEGRAM_PHONE_NUMBER')
channel_ids = os.getenv('TELEGRAM_CHANNEL_IDS').split(',')  # Split comma-separated channel IDs
channel_ids = [int(channel_id) for channel_id in channel_ids]  # Convert to list of integers

# Set up logging
logging.basicConfig(level=logging.INFO)

# Create the client and connect
client = TelegramClient('session_name', api_id, api_hash)

async def start_telegram_listener():
    while True:
        try:
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
                    process_message(message)

            print('Listening for new messages...')
            await client.run_until_disconnected()
        except (OSError, asyncio.TimeoutError) as e:
            logging.warning(f"Connection error: {e}. Reconnecting in 5 seconds...")
            await asyncio.sleep(5)  # Wait for 5 seconds before reconnecting

async def get_channels_with_substring(substring):
    await client.start(phone_number)
    
    # Get all dialogs (conversations)
    dialogs = await client.get_dialogs()
    
    # Filter channels with the given substring
    channels = [dialog for dialog in dialogs if dialog.is_channel and substring.lower() in dialog.title.lower()]
    
    for channel in channels:
        print(f'Channel: {channel.title} (ID: {channel.id})')

async def filter_past_messages(substring):
    await client.start(phone_number)

    # Get the channel entities using channel IDs
    channels = []
    for channel_id in channel_ids:
        channel = await client.get_entity(channel_id)
        channels.append(channel)

    problematic_messages = []
    # Filter past messages for each channel
    for c in channels:
        async for m in client.iter_messages(c):
            if m.message is not None and m.message.startswith(substring):
                #print(f'Channel: {channel.title}, Message: {m.message}')
                try:
                    process_message(m.message)
                except ValueError as e:
                    print(f'Error: {e}')
                    problematic_messages.append(m)
                except IndexError as e:
                    problematic_messages.append(m)


# Make the client accessible from other modules
telegram_client = client
