class Position:
    def __init__(self, tg_msg_id, tg_channel_id, side, symbol, leverage, 
                 entry_low, entry_high, stop_loss, timestamp_utc):
        self.tg_msg_id = tg_msg_id
        self.tg_channel_id = tg_channel_id
        self.side = side
        self.symbol = symbol
        self.leverage = float(leverage)
        self.entry_low = float(entry_low)
        self.entry_high = float(entry_high)
        self.stop_loss = float(stop_loss)
        self.timestamp_utc = timestamp_utc
        self.target_points = []

    def add_target_point(self, price: float, percentage: float):
        target_number = len(self.target_points) + 1
        tp = TargetPoint(target_number, price, percentage)
        self.target_points.append(tp)

class TargetPoint:
    def __init__(self, target_number: int, price: float, percentage: float):
        self.target_number = target_number
        self.price = float(price)
        self.percentage = float(percentage)
