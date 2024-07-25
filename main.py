from telegram_client import TelegramClient
from bybit_client import BybitClient
from message_controller import MessageController
from database import PositionRepository
import config
import asyncio


async def main():
    bybit_client = BybitClient(config.BYBIT_KEY_TESTNET, config.BYBIT_SECRET_TESTNET)
    position_repo = PositionRepository()
    mc = MessageController(bybit_client, position_repo)
    tg = TelegramClient(config.TG_API_ID, config.TG_API_HASH, config.TG_PHONE_NUMBER, mc)
    
    await tg.set_channels(config.TG_CHANNEL_IDS)
    await tg.start_telegram_listener()

if __name__ == '__main__':
    asyncio.run(main())
