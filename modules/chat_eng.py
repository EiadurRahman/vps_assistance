from modules.handle_json import *
from difflib import get_close_matches


def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base['questions']:
        if q['question'] == question:
            return q['answer']
    return None

def update_knowledge_base(question: str, answer: str, knowledge_base_path: str, knowledge_base: dict):
    knowledge_base['questions'].append({
        "question": question,
        "answer": answer
    })
    save_database(knowledge_base_path, knowledge_base)
    return "Answer added to the knowledge base."

def chatbot(question: str, new_answer: str = None) -> str:
    knowledge_base_path = 'data/data_base.json'
    knowledge_base: dict = load_database(knowledge_base_path)

    questions = [q["question"] for q in knowledge_base["questions"]]
    best_match: str | None = find_best_match(question, questions)

    if best_match:
        answer: str | None = get_answer_for_question(best_match, knowledge_base)
        if answer:
            return f' {answer}'
        else:
            return "Found a match but no answer available."

    else:
        if new_answer:
            return update_knowledge_base(question, new_answer, knowledge_base_path, knowledge_base)
        else:
            return " I don't have an answer in my database. Please provide the correct answer or type 'skip'."


if __name__ == '__main__':
    while True:
        user_input = input('you: ')
        if user_input.lower() == 'quit':
            break
        response = chatbot(user_input)
        if "I don't have an answer" in response:
            pass
