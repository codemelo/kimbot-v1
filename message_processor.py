import re

def process_message(message):
    #print(f"Received message from {channel.title}: {message}")
    
    if not message.startswith('INFORMATION'):
        print("INVALID MESSAGE")
        return
    
    # Extract the main information
    info_pattern = re.compile(r"INFORMATION: (LONG|SHORT) (\w+) on (\w+) exchange using (\D*\d+\D*) Leverage with (\d+%) of your deposit")
    info_match = info_pattern.search(message)

    if info_match:
        position, pair, exchange, leverage, percentage = info_match.groups()
    else:
        raise ValueError("Failed to extract main information")

    # Extract entry range
    entry_pattern = re.compile(r"ENTRY BETWEEN: \$?([\d.]+) - \$?([\d.]+)")
    entry_match = entry_pattern.search(message)
    if entry_match:
        entry_low, entry_high = entry_match.groups()
    else:
        raise ValueError("Failed to extract entry range")

    # Extract target points
    targets_pattern = re.compile(r"\) \$?([\d.]+) - (\d+%)")
    targets_matches = targets_pattern.findall(message)
    # targets will be a list of tuples with the structure: (float, str)
    targets = [(float(t[0]), t[1]) for t in targets_matches]

    # Extract stop loss
    stop_loss_pattern = re.compile(r"STOP LOSS: \$?([\d.]+)")
    stop_loss_match = stop_loss_pattern.search(message)
    if stop_loss_match:
        stop_loss = stop_loss_match.group(1)
    else:
        raise ValueError("Failed to extract stop loss")

    # Print extracted information
    print("---------------------------------------------------------------------------------------------")
    print(f"Position: {position}")
    print(f"Pair: {pair}")
    print(f"Exchange: {exchange}")
    print(f"Leverage: {leverage}")
    print(f"Percentage: {percentage}")
    print(f"Entry Low: {entry_low}")
    print(f"Entry High: {entry_high}")
    print(f"Targets: {targets}")
    print(f"Stop Loss: {stop_loss}")



    
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