from bybit_client import get_available_symbols, is_valid_symbol

def process_message(message):
    #print(f"Received message from {channel.title}: {message}")
    
    if not message.startswith('INFORMATION'):
        print("INVALID MESSAGE")
        return
    

    # Extract the substring starting from 'INFORMATION' to 'deposit'
    start = message.find("INFORMATION")
    end = message.find("deposit") + len("deposit")

    # Extracted substring
    substring = message[start:end]

    # Separate the substrings by using whitespace as the delimiter
    substrings = substring.split()


    position_type = None
    symbol = substrings[2]
    leverage = None
    deposit_percentage = None

    for i, s in enumerate(substrings):
        if s == 'SHORT' or s == 'LONG':  # Position type
            position_type = s
        elif (i > 0 and i < len(substrings) - 1 and substrings[i-1] == 'using' and substrings[i+1] == 'Leverage'):  # Leverage
            num_str = extract_num_str(s)
            if num_str is not None and num_str in s:
                leverage = num_str
        elif '%' in s:
            num_str = extract_num_str(s)
            if num_str is not None and num_str in s:
                deposit_percentage = num_str
        

    errors = []
    available_bybit_symbols = get_available_symbols()
    # Check if any of the variables are None
    if position_type is None:
        errors.append("position_type is None")
    if symbol is None or not is_valid_symbol(symbol, available_bybit_symbols):
        errors.append("symbol is not valid")
    if leverage is None:
        errors.append("leverage is None")
    if deposit_percentage is None:
        errors.append("deposit_percentage is None")

    # Check if position_type is either 'SHORT' or 'LONG'
    if position_type not in ['SHORT', 'LONG']:
        errors.append("position_type is not 'SHORT' or 'LONG'")

    if errors:
        raise ValueError("Validation errors: " + ", ".join(errors))
    
    # Print extracted information
    print("---------------------------------------------------------------------------------------------")
    print(f"Position: {position_type}")
    print(f"Symbol: {symbol}")
    print(f"Leverage: {leverage}")
    print(f"Percentage: {deposit_percentage}")

    x = 0

def extract_num_str(str):
    num_str = ''
    for char in str:
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
    # print(f"Position: {position}")
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