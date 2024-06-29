class TradeInfo:
    def __init__(self):
        self._position_type = None
        self._symbol = None
        self._leverage = None
        self._deposit_percentage = None
        self._entry_low = None
        self._entry_high = None
        self._target_points = None
        self._stop_loss = None

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
        return self._entry_low

    @entry_low.setter
    def entry_low(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("entry_low must be a number")
        self._entry_low = value

    @property
    def entry_high(self):
        return self._entry_high

    @entry_high.setter
    def entry_high(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("entry_high must be a number")
        self._entry_high = value

    @property
    def target_points(self):
        return self._target_points

    @target_points.setter
    def target_points(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("target_points must be a number")
        self._target_points = value

    @property
    def stop_loss(self):
        return self._stop_loss

    @stop_loss.setter
    def stop_loss(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("stop_loss must be a number")
        self._stop_loss = value
