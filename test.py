import modules.tgm as tgm
import modules.handle_json as handle_json
from modules.chat_eng import chatbot
from modules.task_eng import task_engine
import modules.differentiate as diffr

api_token = handle_json.single_element('api')
chat_id = handle_json.single_element('chat_id')

bot = tgm.Bot(api_token, chat_id)
bot.get_update()


def chat(msg:str)-> None:
    answer = chatbot(msg)
    bot.send_msg(answer)

    stored_message = None
    def recive():
        return bot.recive_msg() 
    
    if "I don't have an answer" in answer:
        bot.send_msg("Please provide the correct answer or type 'skip'.")
        while not stored_message:
            stored_message = recive()
        new_answer = stored_message[0][1] if stored_message else None
            
        if new_answer and new_answer.lower() != 'skip':
            confirmation = chatbot(msg, new_answer)
            bot.send_msg(confirmation)
        elif new_answer and new_answer.lower() == 'skip':
            bot.send_msg("You can always add information to my database later.")

def task(msg:str)->None:
    command = task_engine(msg)
    # something about task()
    bot.send_msg(command)

    stored_message = None
    def recive():
        return bot.recive_msg()
    
    if "I don't have a command" in command:
        bot.send_msg("Please provide the correct command or type 'skip'.")
        while not stored_message:
            stored_message = recive()
            print('wating for msg',end='\r')
        new_command = stored_message[0][1] if stored_message else None

        if new_command and new_command.lower() != 'skip':
            confirmation = task_engine(msg,new_command)
            bot.send_msg(confirmation)
        elif new_command and new_command.lower() == 'skip':
            bot.send_msg("You can always add command to my database later.")


while True:
    msg = bot.recive_msg()
    msg = msg[0][1] if msg else None

    if msg:
        if diffr.is_task(msg):
            task(msg)
        elif not diffr.is_task(msg):
            chat(msg)