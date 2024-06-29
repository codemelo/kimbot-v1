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

    def _extract_main_info(self, msg_str, trade_info):
        # Extract the substring starting from 'INFORMATION' to 'deposit'
        start = msg_str.find("INFORMATION")
        end = msg_str.find("deposit") + len("deposit")
        substring = msg_str[start:end]  # Extracted substring
        substrings = substring.split()  # Separate the substrings by using whitespace as the delimiter

        position_type = None
        symbol = substrings[2]
        leverage = None
        deposit_percentage = None

        for i, s in enumerate(substrings):
            if s in ['SHORT', 'LONG']:
                position_type = s
            elif 0 < i < len(substrings) - 1 and substrings[i - 1] == 'using' and substrings[i + 1] == 'Leverage':
                num_str = extract_num_str(s)
                if num_str is not None and num_str in s:
                    leverage = num_str
            elif '%' in s:
                num_str = extract_num_str(s)
                if num_str is not None and num_str in s:
                    deposit_percentage = num_str

        trade_info.update(
            position_type=position_type,
            symbol=symbol,
            leverage=leverage,
            deposit_percentage=deposit_percentage
        )

        self._validate_trade_info(trade_info)

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
        entry_start = float(entry_values[0])
        entry_end = float(entry_values[1])

        # Print the extracted values
        print("ENTRY BETWEEN Start Value:", entry_start)
        print("ENTRY BETWEEN End Value:", entry_end)

    def _validate_trade_info(self, trade_info):
        errors = []
        # Check if any of the variables are None
        if trade_info.position_type is None or trade_info.position_type == '':
            errors.append("position_type is None")
        if trade_info.symbol is None or trade_info.symbol == '':
            errors.append("symbol is None")
        if trade_info.leverage is None or trade_info.leverage == '':
            errors.append("leverage is None")
        if trade_info.deposit_percentage is None or trade_info.deposit_percentage == '':
            errors.append("deposit_percentage is None")

        # Check if position_type is either 'SHORT' or 'LONG'
        if trade_info.position_type not in ['SHORT', 'LONG']:
            errors.append(f"position_type {trade_info.position_type} is not 'SHORT' or 'LONG'")
        if trade_info.symbol.endswith('USD'):
            trade_info.symbol += 'T'  # Convert inverse pair to USDT Perp
        if not self.bybit.is_valid_symbol(trade_info.symbol):
            errors.append(f"Symbol {trade_info.symbol} does not exist for trading on bybit")
        if not trade_info.leverage.isdigit():
            errors.append(f"leverage {trade_info.leverage} is not a digit")
        if not trade_info.deposit_percentage.isdigit():
            errors.append(f"Deposit percentage {trade_info.deposit_percentage} is not a digit")

        if errors:
            raise ValueError("Validation errors: " + ", ".join(errors))

        return True


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

    # # Extract entry range
    # entry_pattern = re.compile(r"ENTRY BETWEEN: \$?([\d.]+) - \$?([\d.]+)")
    # entry_match = entry_pattern.search(message)
    # if entry_match:
    #     entry_low, entry_high = entry_match.groups()
    # else:
    #     raise ValueError("Failed to extract entry range")

    # # Extract target points
    # targets_pattern = re.compile(r"\) \$?([\d.]+) - (\d+%)")
    # targets_matches = targets_pattern.findall(message)
    # # targets will be a list of tuples with the structure: (float, str)
    # targets = [(float(t[0]), t[1]) for t in targets_matches]

    # # Extract stop loss
    # stop_loss_pattern = re.compile(r"STOP LOSS: \$?([\d.]+)")
    # stop_loss_match = stop_loss_pattern.search(message)
    # if stop_loss_match:
    #     stop_loss = stop_loss_match.group(1)
    # else:
    #     raise ValueError("Failed to extract stop loss")

    # Print extracted information
    # print("---------------------------------------------------------------------------------------------")
    # print(f"TradeInfo: {position}")
    # print(f"Pair: {pair}")
    # print(f"Exchange: {exchange}")
    # print(f"Leverage: {leverage}")
    # print(f"Percentage: {percentage}")
    # print(f"Entry Low: {entry_low}")
    # print(f"Entry High: {entry_high}")
    # print(f"Targets: {targets}")
    # print(f"Stop Loss: {stop_loss}")

    # # Create result dictionary
    # result = {
    #     "direction": information_match.group(1).upper(),
    #     "symbol": information_match.group(2),
    #     "exchange": information_match.group(3),
    #     "leverage": f"X{information_match.group(4)}",
    #     "deposit_percentage": int(information_match.group(5)),
    #     "entry_between": {
    #         "min": int(entry_match.group(1)),
    #         "max": int(entry_match.group(2)),
    #     },
    #     "target_points": target_points,
    #     "stop_loss": int(stop_loss_match.group(1)),
    # }

    # print(result)
