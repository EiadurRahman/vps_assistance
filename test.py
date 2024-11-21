import modules.tgm as tgm
import modules.handle_json as handle_json

api_token = handle_json.single_element('api')
chat_id = handle_json.single_element('chat_id')

bot = tgm.Bot(api_token, chat_id)
output = bot.get_update()

while not output['result']:
    output = bot.get_update()
    print('wating for chat id',end='\r')

print('\n break')
