import os
import json
import modules.tgm as tgm
from modules.handle_json import single_element

def create_config()-> None:

    config = {"offset" : None,"api" : None,"chat_id" : None}

    os.makedirs('config',exist_ok=True)

    with open('config/config.json','w') as file:
        json.dump(config,file,indent=4)

def add_data_()-> None:
    api = input('bot api token : ')
    single_element("api",api)

    api_token = single_element('api')
    bot = tgm.Bot(api_token,None)
    output = bot.get_update()
    while not output['result']:
        output = bot.get_update()
        print('wating for chat id, send a meassage to the bot',end='\r')
    print('config.json created successfually ')


if __name__ == '__main__':
    create_config()
    add_data_()