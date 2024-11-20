import json
import os

def create_config():
    path = 'config/config.json'
    if not os.path.exists(path):
        os.makedirs('config', exist_ok=True)
        json_body = {"offset": 0,"api":None,"chat_id":None}
        with open(path, 'w') as file:
            json.dump(json_body, file, indent=2)

def single_element(element, data=None,path='config/config.json'):
    'grabs or update a single element from a json file'
    if not os.path.exists(path):
        print("Config file does not exist. Creating default config.")
        create_config()

    with open(path, 'r') as file:
        config = json.load(file)
        
    if data is not None:
        config[element] = data  # Update or add the element with new data
        with open(path, 'w') as file:
            json.dump(config, file, indent=2)
        return f"{element} updated to {data}"
    else:
        return config.get(element, f"{element} not found in config")  # Return element if it exists

def update_offset():
    offset = single_element('offset')
    single_element('offset',int(offset)+1)
    print('updating ofset')

# chatbot part 

def load_database(file_path: str) -> dict:  # Changed return type to dict
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data  # Return the dict directly, not a JSON string

def save_database(file_path: str, data: dict) -> None:
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)