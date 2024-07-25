from data_extractor import encapsulate_position


class MessageController():
    def __init__(self, bybit_client, position_repo):
        self.bybit = bybit_client
        self.repo = position_repo

    def process_message(self, tg_msg_obj):
        msg_str = tg_msg_obj.raw_text
        if msg_str.startswith("INFORMATION"):
            position = encapsulate_position(tg_msg_obj)
            #self.repo.add(position)
            self.bybit.place_trade(position)
        elif 'Manually Cancelled' in msg_str:
            symbol = msg_str.split('#')[1].split('/')[0]
            self.bybit.close_position(symbol + "USDT")
        else:
            print("Non-actionable message received.")


