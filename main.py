import asyncio
from telegram_listener import start_telegram_listener, get_channels_with_substring, filter_past_messages

def main():
    #asyncio.run(start_telegram_listener())
    #asyncio.run(get_channels_with_substring("TEST"))
    asyncio.run(filter_past_messages('INFORMATION'))

if __name__ == '__main__':
    main()