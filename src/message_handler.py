from models.trade_info import TradeInfo


class MessageHandler:
    def __init__(self, bybit_client):
        self.bybit = bybit_client

    def process_message(self, msg_str):
        if not msg_str.startswith('INFORMATION'):
            print("INVALID MESSAGE")
            return

        trade_info = TradeInfo()
        self._extract_main_info(msg_str, trade_info)
        self._extract_entry_range(msg_str, trade_info)
        self._extract_target_points(msg_str, trade_info)
        self._extract_stop_loss(msg_str, trade_info)

        self.bybit.place_trade(trade_info)

        return trade_info

    def _extract_main_info(self, msg_str, trade_info):
        # Extract the substring starting from 'INFORMATION' to 'deposit'
        start = msg_str.find("INFORMATION")
        end = msg_str.find("deposit") + len("deposit")
        substring = msg_str[start:end]  # Extracted substring
        substrings = substring.split()  # Separate the substrings by using whitespace as the delimiter

        trade_info.symbol = substrings[2]
        for i, s in enumerate(substrings):
            if s.upper() in ['SHORT', 'LONG']:
                trade_info.position_type = s.upper()
            elif (0 < i < len(substrings) - 1
                  and substrings[i - 1].lower() == 'using' and substrings[i + 1].lower() == 'leverage'):
                num_str = extract_num_str(s)
                if num_str is not None and num_str in s:
                    trade_info.leverage = num_str
            elif '%' in s:
                num_str = extract_num_str(s)
                if num_str is not None and num_str in s:
                    trade_info.deposit_percentage = num_str

    def _extract_entry_range(self, msg_str, trade_info):
        # Step 1: Find the start index of "ENTRY BETWEEN"
        start = msg_str.find("ENTRY BETWEEN")

        # Step 2: Find the end index of the line
        end = msg_str.find("\n", start)

        # Step 3: Extract the substring containing "ENTRY BETWEEN" values
        entry_between_str = msg_str[start:end]

        # Step 4: Extract the values after "ENTRY BETWEEN:"
        entry_values_str = entry_between_str.split(":")[1].strip()
        entry_values_str = entry_values_str.replace("$", "").replace(" ", "")
        entry_values = entry_values_str.split("-")
        entry_low = float(entry_values[0])
        entry_high = float(entry_values[1])

        trade_info.entry_range = (entry_low, entry_high)

    def _extract_target_points(self, msg_str, trade_info):
        # Step 1: Find the start index of "TARGET POINTS"
        start = msg_str.find("TARGET POINTS:")

        # Step 2: Find the end index of the section (next section or end of string)
        stop_loss_start = msg_str.find("STOP LOSS", start)
        end = stop_loss_start if stop_loss_start != -1 else len(msg_str)

        # Step 3: Extract the substring containing "TARGET POINTS" values
        target_points_str = msg_str[start:end].strip()

        # Step 4: Split the lines containing target points
        lines = target_points_str.split("\n")

        # Step 5: Iterate over the lines and extract the target points
        for line in lines:
            if ')' in line and '-' in line:
                parts = line.split(')')
                price_part = parts[1].split('-')[0].strip().replace("$", "")
                percentage_part = parts[1].split('-')[1].strip().replace("%", "")
                price = float(price_part)
                percentage = int(percentage_part)
                trade_info.add_target_point(price, percentage)

    def _extract_stop_loss(self, msg_str, trade_info):
        # Step 1: Find the start index of "STOP LOSS"
        start = msg_str.find("STOP LOSS:")

        # Step 2: Find the end index of the line
        end = msg_str.find("\n", start)
        if end == -1:  # In case "STOP LOSS" is at the end of the string without a newline character
            end = len(msg_str)

        # Step 3: Extract the substring containing "STOP LOSS" value
        stop_loss_str = msg_str[start:end]

        # Step 4: Extract the value after "STOP LOSS:"
        stop_loss_value_str = stop_loss_str.split(":")[1].strip()
        stop_loss_value_str = stop_loss_value_str.replace("$", "").replace(" ", "")
        stop_loss_value = float(stop_loss_value_str)

        trade_info.stop_loss = stop_loss_value


def extract_num_str(s):
    num_str = ''
    for char in s:
        if char.isdigit():
            num_str += char
        elif num_str:  # if we already have a number and encounter a non-numeric character
            break

    if num_str:
        return num_str
    else:
        return None
