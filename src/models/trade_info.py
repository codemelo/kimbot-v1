class TradeInfo:
    def __init__(self):
        self._position_type = None
        self._symbol = None
        self._leverage = None
        self._deposit_percentage = None
        self._entry_range = None
        self._target_points = []
        self._stop_loss = None

    def __str__(self):
        target_points_str = "\n".join([f"{i+1}) ${tp.price} - {tp.percentage}%" for i, tp in enumerate(self.target_points)])
        entry_range_str = f"${self.entry_low} - ${self.entry_high}" if self.entry_range else "N/A"
        return (f"Position Type: {self.position_type}\n"
                f"Symbol: {self.symbol}\n"
                f"Leverage: {self.leverage}x\n"
                f"Deposit Percentage: {self.deposit_percentage}%\n"
                f"Entry Range: {entry_range_str}\n"
                f"Target Points:\n{target_points_str}\n"
                f"Stop Loss: ${self.stop_loss}")

    @property
    def position_type(self):
        return self._position_type

    @position_type.setter
    def position_type(self, value):
        if not value or value.upper() not in ["LONG", "SHORT"]:
            raise ValueError(f"Value {value} not valid for position_type. Must be 'LONG' or 'SHORT'")
        self._position_type = value.upper()

    @property
    def symbol(self):
        return self._symbol

    @symbol.setter
    def symbol(self, value):
        if not value:
            raise ValueError(f"Value {value} for symbol not valid.")
        if value.endswith('USD'):
            value += 'T'  # Convert inverse pair to USDT Perp
        self._symbol = value

    @property
    def leverage(self):
        return self._leverage

    @leverage.setter
    def leverage(self, value):
        if not value or int(value) <= 0:
            raise ValueError(f"Value {value} for leverage is not valid. Must be a positive integer")
        self._leverage = int(value)

    @property
    def deposit_percentage(self):
        return self._deposit_percentage

    @deposit_percentage.setter
    def deposit_percentage(self, value):
        if not value or int(value) <= 0:
            raise ValueError(f"Value {value} for deposit_percentage is not valid. Must be a positive integer")
        self._deposit_percentage = int(value)

    @property
    def entry_low(self):
        return self._entry_range[0]

    @property
    def entry_high(self):
        return self._entry_range[1]

    @property
    def entry_range(self):
        return self._entry_range

    @entry_range.setter
    def entry_range(self, value):
        if isinstance(value, tuple) and len(value) == 2 and isinstance(value[0], float) and isinstance(value[1], float):
            if value[0] > value[1]:
                raise ValueError("First value must be less than second value in entry_range tuple")
            self._entry_range = value
        else:
            raise ValueError("entry_range must be a tuple with two float elements")

    @property
    def target_points(self):
        return self._target_points

    def add_target_point(self, price: float, percentage: float):
        tp = TargetPoint(price, percentage)
        self.target_points.append(tp)

    @property
    def stop_loss(self):
        return self._stop_loss

    @stop_loss.setter
    def stop_loss(self, value):
        if not isinstance(value, float):
            raise ValueError("stop_loss must be a float")
        self._stop_loss = value


class TargetPoint:
    def __init__(self, price: float, percentage: float):
        self.price = float(price)
        self.percentage = float(percentage)
