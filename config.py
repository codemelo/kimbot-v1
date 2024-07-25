import os
from dotenv import load_dotenv


load_dotenv()

TG_API_ID = os.getenv('TELEGRAM_API_ID')
TG_API_HASH = os.getenv('TELEGRAM_API_HASH')
TG_PHONE_NUMBER = os.getenv('TELEGRAM_PHONE_NUMBER')
TG_CHANNEL_IDS = [int(i) for i in os.getenv('TELEGRAM_CHANNEL_IDS').split(',')]

BYBIT_KEY_TESTNET = os.getenv('BYBIT_KEY_TESTNET')
BYBIT_SECRET_TESTNET = os.getenv('BYBIT_SECRET_TESTNET')

DATABASE_URL = os.getenv('DATABASE_URL')

DEPOSIT_PERCENTAGE = 10
SL_RISK_FACTOR = 0.877

JSON_TEMPLATE = '{"side":"SHORT","symbol":"ETHUSD","leverage":50,"entry_low":"3445.8","entry_high":"3469.9","target_points":[{"price":"3435.4","percentage":20},{"price":"3431.3","percentage":20},{"price":"3425.7","percentage":24},{"price":"3414.7","percentage":14},{"price":"3400.9","percentage":12},{"price":"3387.1","percentage":10}],"stop_loss":"3518.2"}'