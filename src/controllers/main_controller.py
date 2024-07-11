from src.models import Position, TargetPoint
from src.services import TelegramClient, MessageHandler, BybitClient
from src.data import DataManager
from utils import config


class MainController:
    def __init__(self):
        self.data = None
        self.bybit = None
        self.msg = None
        self.tg = None

    async def initialize(self):
        # self.data = DataManager()
        # self.bybit = BybitClient(config.BYBIT_API_KEY, config.BYBIT_API_SECRET)
        self.bybit = BybitClient(config.BYBIT_API_KEY_TESTNET, config.BYBIT_API_SECRET_TESTNET)
        self.msg = MessageHandler(self.bybit)

        self.tg = TelegramClient(
            config.TG_API_ID,
            config.TG_API_HASH,
            config.TG_PHONE_NUMBER,
            self.msg
        )
        await self.tg.set_channels(config.TG_CHANNEL_IDS)

        pass

    async def start_telegram_listener(self):
        await self.tg.start_telegram_listener()
