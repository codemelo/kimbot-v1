from models import Position
import ollama
import json
import config


def encapsulate_position(tg_msg_obj):
    tg_msg_id = tg_msg_obj.id
    tg_channel_id = tg_msg_obj.chat_id
    timestamp = tg_msg_obj.date
    obj = _extract_json(tg_msg_obj.raw_text)
    position = Position(
        tg_msg_id=tg_msg_id,
        tg_channel_id=tg_channel_id,
        side=obj['side'],
        symbol=obj['symbol'],
        leverage=obj['leverage'],
        entry_low=obj['entry_low'],
        entry_high=obj['entry_high'],
        stop_loss=obj['stop_loss'],
        timestamp_utc=timestamp
    )

    for tp in obj['target_points']:
        position.add_target_point(tp['price'], tp['percentage'])

    return position

def _extract_json(text):
    result = _get_llama_response(text)
    json_obj = None
    bracket_count = 0
    start_index = -1
    
    for i, char in enumerate(result):
        if char == '{':
            if bracket_count == 0:
                start_index = i
            bracket_count += 1
        elif char == '}':
            bracket_count -= 1
            if bracket_count == 0 and start_index != -1:
                json_str = result[start_index:i+1]
                try:
                    json_obj = json.loads(json_str)
                except json.JSONDecodeError:
                    pass  # Not a valid JSON object
                start_index = -1
    
    return json_obj

def _get_llama_response(text):
    json_template = config.JSON_TEMPLATE
    prompt = f"Extract the position side, symbol, leverage, entry low, entry high, target points with their respective percentages, and stop loss. Return all the data as json. All numerical values should be floats. Here is example json for you to adhere to as a template:\n\n{json_template} \n\nHere is the text for you to extract from:\n{text}"
    response = ollama.generate(
        model='llama3',
        prompt=prompt
    )
    return response['response']
