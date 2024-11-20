from modules.handle_json import *
from modules.run_command import *
# from handle_json import *
from difflib import get_close_matches

def find_best_match(input_task: str, tasks: list[str]) -> str | None:
    matches: list = get_close_matches(input_task, tasks, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_commands(task: str, database: dict) -> str | None:
    for t in database['tasks']:
        if t['task'] == task:
            return t['command']

def update_task_command(task: str, command: str, task_database: dict, database_path=r'data\data_base.json') -> None:
    task_database['tasks'].append({
        "task": task,
        "command": command
    })
    save_database(database_path, task_database)

def task_engine(task: str, new_command: str = None) -> str:
    task_database_path: str = r'data\data_base.json'
    task_database: dict = load_database(task_database_path)

    tasks = [t['task'] for t in task_database['tasks']]
    best_match: str | None = find_best_match(task, tasks)

    if best_match:
        command: str | None = get_commands(best_match, task_database)
        if command:
            output = run(command)
            return output
        else:
            return "Found a match but no command for it"
    else:
        if new_command:
            update_task_command(task, new_command, task_database, task_database_path)
            return "Task and command added to the database."
        else:
            return "I don't have a command in my database. Please provide the correct command [run <task>] or type 'skip'."

if __name__ == '__main__':
    while True:
        user_input = input('you: ')
        if user_input.lower() == 'quit':
            break
        response = task_engine(user_input)
        print(response)
        if "I don't have a command" in response:
            input_command = input('new task : ')
            if not user_input.lower() == 'skip':
                confirmation = task_engine(user_input,input_command)
                print(confirmation)
            else:
                print('You can always add task and its command to my database later.')
