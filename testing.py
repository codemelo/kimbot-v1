import asyncio
from src.data import DataManager
from src.services import TelegramClient, MessageHandler
from utils import config

from datetime import datetime, timezone


async def main():
    data = DataManager()

    msg = MessageHandler()

    tg = TelegramClient(
        config.TG_API_ID,
        config.TG_API_HASH,
        config.TG_PHONE_NUMBER,
        msg
    )
    await tg.set_channels(config.TG_CHANNEL_IDS)

    messages = await tg.get_past_messages_starting_with("INFORMATION")

    for m in messages:
        p = msg.process_message(m)
        data.create_position(
            tg_msg_id=m.id,
            tg_channel_id=m.chat_id,
            side=p.side,
            symbol=p.symbol,
            leverage=p.leverage,
            entry_low=p.entry_low,
            entry_high=p.entry_high,
            stop_loss=p.stop_loss,
            datetime=m.date
        )
        print(f"Message {m.id} processed and saved...")

if __name__ == '__main__':
    asyncio.run(main())
