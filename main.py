import asyncio
from telegram_listener import start_telegram_listener, get_channels_with_substring

def main():
    asyncio.run(start_telegram_listener())
    #asyncio.run(get_channels_with_substring("TEST"))

if __name__ == '__main__':
    main()