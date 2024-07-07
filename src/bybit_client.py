import time
from decimal import Decimal, ROUND_UP
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

        # Fetch instrument info to get qtyStep
        instrument_info = self.session.get_instruments_info(
            category="linear",
            symbol=trade_info.symbol
        )
        qty_step = Decimal(instrument_info['result']['list'][0]['lotSizeFilter']['qtyStep'])

        # Calculate order value based on deposit percentage
        usdt_balance = Decimal(self.get_balance("USDT"))
        order_value = usdt_balance * (Decimal(trade_info.deposit_percentage) / Decimal(100))

        # Calculate the leveraged order value
        leveraged_order_value = order_value * Decimal(trade_info.leverage)

        # Calculate the raw quantity using the leveraged order value
        current_price = Decimal(str(self.get_current_price(trade_info.symbol)))
        raw_quantity = leveraged_order_value / current_price

        # Round down to the nearest multiple of qtyStep
        order_quantity = raw_quantity.quantize(qty_step, rounding=ROUND_UP)

        # Calculate the actual amount from balance being used
        actual_balance_used = order_quantity * current_price / Decimal(trade_info.leverage)

        # Determine order side
        order_side = None
        if trade_info.position_type == "LONG":
            order_side = "Buy"
        elif trade_info.position_type == "SHORT":
            order_side = "Sell"

        # Determine order price based on current price and entry range
        current_price = self.get_current_price(trade_info.symbol)
        if current_price < trade_info.entry_low:
            order_price = trade_info.entry_low
            main_order_type = "Limit"
        elif current_price > trade_info.entry_high:
            order_price = trade_info.entry_high
            main_order_type = "Limit"
        else:
            order_price = current_price
            main_order_type = "Market"

        # Place main order
        main_order = self.session.place_order(
            category="linear",
            symbol=trade_info.symbol,
            side=order_side,
            orderType=main_order_type,
            qty=str(order_quantity),
            price=str(order_price),
            timeInForce="GTC",
            stopLoss=str(trade_info.stop_loss)
        )

        print(f"Asset: {trade_info.symbol}"
              f"\nOrder quantity: {order_quantity}"
              f"\nOrder price: {order_price}"
              f"\nCurrent Price: {current_price}")
        print("\n----------------------------------------------------------------------------------\n")

        print(f"Main order placed by {main_order_type}: \n{main_order}")

        # Wait for the main order to be filled before placing take profit orders
        order_id = main_order['result']['orderId']
        while True:
            try:
                order_status = self.session.get_order_history(
                    category="linear",
                    symbol=trade_info.symbol,
                    orderId=order_id
                )
                if order_status['result']['list'][0]['orderStatus'] == 'Filled':
                    break
                time.sleep(5)  # Wait for 5 seconds before checking again
            except IndexError as e:
                time.sleep(5)

        # Determine order side for take profit
        tp_side = None
        if order_side == "Buy":
            tp_side = "Sell"
        elif order_side == "Sell":
            tp_side = "Buy"

        total_tp_quantity = Decimal('0')
        tp_orders = []

        for i, tp in enumerate(trade_info.target_points):
            tp_quantity = order_quantity * (Decimal(tp.percentage) / Decimal(100))
            tp_quantity = tp_quantity.quantize(qty_step, rounding=ROUND_UP)

            if tp_quantity > Decimal('0'):
                total_tp_quantity += tp_quantity
                tp_orders.append((tp_quantity, tp.price))
            else:
                print(f"Skipping take profit order {i + 1} due to insufficient quantity")

        # Adjust if total exceeds order quantity
        if total_tp_quantity > order_quantity:
            excess = total_tp_quantity - order_quantity
            for i in range(len(tp_orders)):
                if tp_orders[i][0] > excess:
                    tp_orders[i] = (tp_orders[i][0] - excess, tp_orders[i][1])
                    break
                excess -= tp_orders[i][0]
                tp_orders[i] = (Decimal('0'), tp_orders[i][1])

        # Place the adjusted take profit orders
        for i, (tp_quantity, tp_price) in enumerate(tp_orders):
            if tp_quantity > Decimal('0'):
                tp_order = self.session.place_order(
                    category="linear",
                    symbol=trade_info.symbol,
                    side=tp_side,
                    orderType="Limit",
                    qty=str(tp_quantity),
                    price=str(tp_price),
                    timeInForce="GTC",
                    reduceOnly=True
                )
                print(f"Take profit order {i + 1} placed: \n{tp_order}")

        print("All orders placed successfully")

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
