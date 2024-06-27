from pybit.unified_trading import HTTP
from dotenv import load_dotenv
import os

load_dotenv()

# Replace these with your actual API key and secret
API_KEY = os.getenv('BYBIT_API_KEY')
API_SECRET = os.getenv('BYBIT_API_SECRET')


# def get_available_symbols():
#     # Initialize the API client
#     session = HTTP(api_key=API_KEY, api_secret=API_SECRET)

#     # Get the list of available symbols
#     symbols_info = 3
#     available_symbols = [symbol['name'] for symbol in symbols_info['result']]

#     return available_symbols


def is_valid_symbol(symbol_to_check, available_symbols):
    if symbol_to_check in available_symbols:
        return True
    else:
        return False

# def is_valid_symbol(symbol):
#     url = "https://api.bybit.com/v2/public/symbols"
#     response = requests.get(url)
#     if response.status_code == 200:
#         data = response.json()
#         symbols = [item['name'] for item in data['result']]
#         return symbol in symbols
#     else:
#         print(f"Failed to fetch data: {response.status_code}")
#         return False
