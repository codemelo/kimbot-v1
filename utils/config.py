import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    TG_API_ID = os.getenv('TELEGRAM_API_ID')
    TG_API_HASH = os.getenv('TELEGRAM_API_HASH')
    TG_PHONE_NUMBER = os.getenv('TELEGRAM_PHONE_NUMBER')
    TG_CHANNEL_IDS = [int(i) for i in os.getenv('TELEGRAM_CHANNEL_IDS').split(',')]

    BYBIT_API_KEY = os.getenv('BYBIT_API_KEY')
    BYBIT_API_SECRET = os.getenv('BYBIT_API_SECRET')
    BYBIT_API_KEY_TESTNET = os.getenv('BYBIT_API_KEY_TESTNET')
    BYBIT_API_SECRET_TESTNET = os.getenv('BYBIT_API_SECRET_TESTNET')

    DATABASE_URL = os.getenv('DATABASE_URL')

    DEPOSIT_PERCENTAGE = 10
    SL_RISK_FACTOR = 0.877
