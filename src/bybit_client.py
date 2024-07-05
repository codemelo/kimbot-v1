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
        order_quantity = round((order_value / current_price), 4)

        # TODO calculate qty properly using qtyStep
        #  https://stackoverflow.com/questions/76987446/params-error-qty-invalid-errcode-10001-being-returned-by-bybit-api

        print(f"Asset: {trade_info.symbol}"
              f"\nOrder quantity: {order_quantity}"
              f"\nOrder price: {order_price}"
              f"\nCurrent Price: {current_price}")

        # Determine order side
        order_side = None
        if trade_info.position_type == "LONG":
            order_side = "Buy"
        elif trade_info.position_type == "SHORT":
            order_side = "Sell"

        # Place main order
        main_order = self.session.place_order(
            category="linear",
            symbol=trade_info.symbol,
            side=order_side,
            orderType="Limit",
            qty=str(order_quantity),
            price=str(order_price),
            timeInForce="GTC",
            stopLoss=str(trade_info.stop_loss)
        )
        print(f"Main order placed: \n{main_order}")

        # Determine order side for take profit
        tp_side = None
        if order_side == "Buy":
            tp_side = "Sell"
        elif order_side == "Sell":
            tp_side = "Buy"

        remaining_qty = order_quantity
        for target in trade_info.target_points:
            tp_qty = round(order_quantity * (target.percentage / 100), 4)
            # TODO calculate qty properly using qtyStep
            remaining_qty -= tp_qty

            tp_order = self.session.place_order(
                category="linear",
                symbol=trade_info.symbol,
                side=tp_side,
                orderType="Limit",
                qty=str(tp_qty),
                price=str(target.price),
                timeInForce="GTC",
                triggerBy="LastPrice",
                reduceOnly=True
            )
            print(f"Take profit order placed: \n{tp_order}")

        if remaining_qty > 0:
            print(f"Warning: Remaining quantity {remaining_qty} not placed in take profit orders")

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

