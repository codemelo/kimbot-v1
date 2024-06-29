class TradeInfo:
    def __init__(self, position_type=None, symbol=None, leverage=None, deposit_percentage=None):
        self.position_type = position_type
        self.symbol = symbol
        self.leverage = leverage
        self.deposit_percentage = deposit_percentage

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return (f"TradeInfo(position_type={self.position_type}, symbol={self.symbol}, leverage={self.leverage}, "
                f"deposit_percentage={self.deposit_percentage}")
