import asyncio
import os
from dotenv import load_dotenv
from telegram_client import TelegramClient
from bybit_client import BybitClient
from message_handler import MessageHandler


async def main():
    # asyncio.run(get_channels_with_substring("TEST"))
    # asyncio.run(filter_past_messages('INFORMATION'))

    load_dotenv()
    bybit = setup_bybit()
    msg = MessageHandler(bybit)
    tg = await setup_telegram(msg)

    # await tg.filter_past_messages('INFORMATION')

    # await tg.start_telegram_listener()


def setup_bybit():
    bybit_api_key = os.getenv('BYBIT_API_KEY')
    bybit_api_secret = os.getenv('BYBIT_API_SECRET')

    bybit = BybitClient(bybit_api_key, bybit_api_secret)
    return bybit


async def setup_telegram(message_handler):
    tg_api_id = os.getenv('TELEGRAM_API_ID')
    tg_api_hash = os.getenv('TELEGRAM_API_HASH')
    phone_number = os.getenv('TELEGRAM_PHONE_NUMBER')

    tg = TelegramClient(tg_api_id, tg_api_hash, phone_number, message_handler)
    channel_ids = os.getenv('TELEGRAM_CHANNEL_IDS').split(',')  # Split comma-separated channel IDs
    channel_ids = [int(channel_id) for channel_id in channel_ids]  # Convert to list of integers
    await tg.set_channels_by_id(channel_ids)
    return tg


if __name__ == '__main__':
    asyncio.run(main())
