from pybit.unified_trading import HTTP

from src.models.trade_info import TradeInfo


class BybitClient:
    def __init__(self, api_key, api_secret):
        self.session = HTTP(
            testnet=True,
            api_key=api_key,
            api_secret=api_secret)

    def place_trade(self, trade_info: TradeInfo):

        try:
            current_leverage = self.get_current_leverage(trade_info.symbol)
        except Exception as e:
            print(f"Error getting current leverage: {e}")
            current_leverage = None

        # Set leverage only if it's different
        if current_leverage is None or float(current_leverage) != trade_info.leverage:
            leverage_str = str(trade_info.leverage)
            self.session.set_leverage(
                category="linear",
                symbol=trade_info.symbol,
                buyLeverage=leverage_str,
                sellLeverage=leverage_str
            )
            print(f"Leverage set to {leverage_str}")
        else:
            print(f"Leverage already set to {trade_info.leverage}")

        # Determine order price based on current price and entry range
        current_price = self.get_current_price(trade_info.symbol)
        if current_price < trade_info.entry_low:
            order_price = trade_info.entry_low
        elif current_price > trade_info.entry_high:
            order_price = trade_info.entry_high
        else:
            order_price = current_price

        # Calculate order quantity based on deposit percentage
        usdt_balance = self.get_balance("USDT")
        order_value = usdt_balance * (trade_info.deposit_percentage / 100)
        order_quantity = order_value / current_price

        print(f"Asset: {trade_info.symbol}"
              f"\nOrder quantity: {order_quantity}"
              f"\nOrder price: {order_price}"
              f"\nCurrent Price: {current_price}")

        # TODO place order, take profit targets, stop loss

    def get_balance(self, coin):
        response = self.session.get_wallet_balance(
            accountType="UNIFIED",
            coin=coin
        )

        balance = response['result']['list'][0]['coin'][0]['walletBalance']
        return float(balance)

    def get_account_info(self):
        return self.session.get_account_info()

    def get_current_leverage(self, symbol):
        try:
            response = self.session.get_positions(
                category="linear",
                symbol=symbol
            )

            if response["retCode"] == 0:
                positions = response["result"]["list"]
                if positions:
                    leverage = positions[0]["leverage"]
                    return float(leverage)
                else:
                    print(f"No position found for {symbol}")
                    return None
            else:
                print(f"Error: {response['retMsg']}")
                return None
        except Exception as e:
            print(f"An error occurred while getting leverage: {e}")
            return None

    def get_current_price(self, symbol):
        info = self.session.get_tickers(category="linear", symbol=symbol)
        return float(info['result']['list'][0]['lastPrice'])

    def get_symbols(self):
        try:
            resp = self.session.get_tickers(category="linear")['result']['list']
            symbols = [elem['symbol'] for elem in resp]
            return symbols
        except Exception as e:
            print(e)

    def is_valid_symbol(self, symbol):
        symbols = self.get_symbols()

        if symbol in symbols:
            return True
        else:
            return False

    def search_symbols_by_substring(self, substring):
        symbols = self.get_symbols()

        matches = []
        for s in symbols:
            if substring in s:
                matches.append(s)

        return matches
