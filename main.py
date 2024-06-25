import asyncio
from telegram_listener import start_telegram_listener

def main():
    asyncio.run(start_telegram_listener())

if __name__ == '__main__':
    main()