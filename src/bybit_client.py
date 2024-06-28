from pybit.unified_trading import HTTP


class BybitClient:
    def __init__(self, api_key, api_secret):
        self.session = HTTP(api_key=api_key, api_secret=api_secret)
        self.symbols = None

    def get_symbols(self):
        if self.symbols is not None:
            return self.symbols

        try:
            resp = self.session.get_tickers(category="linear")['result']['list']
            symbols = [elem['symbol'] for elem in resp]
            return symbols
        except Exception as e:
            print(e)

    def is_valid_symbol(self, symbol):
        if self.symbols is None:
            self.symbols = self.get_symbols()

        if symbol in self.symbols:
            return True
        else:
            return False

    def search_symbols_by_substring(self, substring):
        if self.symbols is None:
            self.symbols = self.get_symbols()

        matches = []
        for s in self.symbols:
            if substring in s:
                matches.append(s)

        return matches
