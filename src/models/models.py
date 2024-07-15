class Position:
    def __init__(self, position_id=None, tg_msg_id=None, tg_channel_id=None, side=None, symbol=None, leverage=None, entry_low=None,
                 entry_high=None, stop_loss=None, stopped=None, datetime=None):
        self.position_id = position_id
        self.tg_msg_id = tg_msg_id
        self.tg_channel_id = tg_channel_id
        self.side = side
        self.symbol = symbol
        self.leverage = leverage
        self.entry_low = entry_low
        self.entry_high = entry_high
        self.stop_loss = stop_loss
        self.stopped = stopped
        self.datetime = datetime
        self.target_points = []

    def add_target_point(self, price: float, percentage: float):
        target_number = len(self.target_points) + 1
        tp = TargetPoint(target_number, price, percentage)
        self.target_points.append(tp)


class TargetPoint:
    def __init__(self, target_number: int, price: float, percentage: float):
        self.target_number = target_number
        self.price = price
        self.margin_percentage = percentage
