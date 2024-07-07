import asyncio
import os
from dotenv import load_dotenv

from src.models.trade_info import TradeInfo, TargetPoint
from telegram_client import TelegramClient
from bybit_client import BybitClient
from message_handler import MessageHandler


async def main():
    # asyncio.run(get_channels_with_substring("TEST"))
    # asyncio.run(filter_past_messages('INFORMATION'))

    load_dotenv()
    # bybit = setup_bybit()
    bybit = setup_bybit_testnet()
    msg = MessageHandler(bybit)
    tg = await setup_telegram(msg)

    # matches = bybit.search_symbols_by_substring(".")
    # print(matches)

    # await tg.filter_past_messages('INFORMATION')

    # await tg.start_telegram_listener()

    # trades = await backtest_past_messages(tg, msg)
    # check_validation(trades)

    # t = TradeInfo()
    # t.position_type = "SHORT"
    # t.symbol = "BTCUSDT"
    # t.leverage = 50
    # t.deposit_percentage = 10
    # t.entry_range = (53000.0, 59000.0)
    # t.add_target_point(57000, 50)
    # t.add_target_point(56900, 25)
    # t.add_target_point(56800, 25)
    # t.stop_loss = 60000.0
    #
    # print(bybit.get_current_price("BTCUSDT"))
    # bybit.place_trade(t)

    t = TradeInfo()
    t.position_type = "LONG"
    t.symbol = "ETHUSDT"
    t.leverage = 50
    t.deposit_percentage = 10
    t.entry_range = (2900.0, 3500.0)
    t.add_target_point(3100, 20)
    t.add_target_point(3150, 20)
    t.add_target_point(3200, 24)
    t.add_target_point(3300, 14)
    t.add_target_point(3350, 12)
    t.add_target_point(3400, 10)
    t.stop_loss = 3000.0

    # print(bybit.get_current_price("BTCUSDT"))
    bybit.place_trade(t)


async def backtest_past_messages(tg, msg):
    messages = await tg.get_past_messages("INFORMATION")
    trades = []
    errors = []
    for m in messages:
        try:
            trade = msg.process_message(m)
            trades.append(trade)
        except Exception as e:
            errors.append(e)
    return trades


def setup_bybit():
    bybit_api_key = os.getenv('BYBIT_API_KEY')
    bybit_api_secret = os.getenv('BYBIT_API_SECRET')

    bybit = BybitClient(bybit_api_key, bybit_api_secret)
    return bybit


def setup_bybit_testnet():
    bybit_api_key = os.getenv('BYBIT_API_KEY_TESTNET')
    bybit_api_secret = os.getenv('BYBIT_API_SECRET_TESTNET')

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


def check_validation(trades):
    errors = []

    for i, trade in enumerate(trades):
        if trade.position_type not in ["LONG", "SHORT"]:
            errors.append(f"Trade {i}: Invalid position_type '{trade.position_type}'. Must be 'LONG' or 'SHORT'.")
        if not isinstance(trade.deposit_percentage, (int, float)) or not (0 < trade.deposit_percentage <= 10):
            errors.append(
                f"Trade {i}: Invalid deposit_percentage '{trade.deposit_percentage}'. Must be a positive int or float no larger than 10.")
        if not isinstance(trade.leverage, (int, float)) or trade.leverage <= 0:
            errors.append(f"Trade {i}: Invalid leverage '{trade.leverage}'. Must be a positive int or float.")
        if trade.entry_range is None or not isinstance(trade.entry_low, float) or trade.entry_low <= 0:
            errors.append(f"Trade {i}: Invalid entry_low '{trade.entry_low}'. Must be a positive float.")
        if trade.entry_range is None or not isinstance(trade.entry_high, float) or trade.entry_high <= 0:
            errors.append(f"Trade {i}: Invalid entry_high '{trade.entry_high}'. Must be a positive float.")
        if trade.entry_range is None or trade.entry_low >= trade.entry_high:
            errors.append(
                f"Trade {i}: entry_low '{trade.entry_low}' must be less than entry_high '{trade.entry_high}'.")
        if not isinstance(trade.stop_loss, float) or trade.stop_loss <= 0:
            errors.append(f"Trade {i}: Invalid stop_loss '{trade.stop_loss}'. Must be a positive float.")

        if not trade.target_points:
            errors.append(f"Trade {i}: target_points is empty or not defined.")
        else:
            total_percentage = 0
            for j, tp in enumerate(trade.target_points):
                if not isinstance(tp.price, float) or tp.price <= 0:
                    errors.append(f"Trade {i}, Target Point {j}: Invalid price '{tp.price}'. Must be a positive float.")
                if not isinstance(tp.percentage, float) or tp.percentage <= 0:
                    errors.append(
                        f"Trade {i}, Target Point {j}: Invalid percentage '{tp.percentage}'. Must be a positive float.")
                total_percentage += tp.percentage
            if total_percentage != 100:
                errors.append(
                    f"Trade {i}: Target points percentages do not add up to 100. Total is {total_percentage}.")

    if errors:
        for error in errors:
            print(error)
    else:
        print("All trades are valid.")


if __name__ == '__main__':
    asyncio.run(main())
