import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag

# Download required NLTK data
nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')

def is_task(input_text: str) -> bool:
    """
    Determines if the input text is a task or a general query using NLTK.
    
    Args:
        input_text (str): The text to analyze.
        
    Returns:
        bool: True if it's a task, False if it's a normal chat or question.
    """
    # Preprocess input
    input_text = input_text.strip().lower()
    tokens = word_tokenize(input_text)
    
    # Define task-related keywords and patterns
    task_keywords = {"create", "build", "write", "generate", "implement", 
                     "code", "run", "calculate", "design", "extract", "fetch"}
    question_keywords = {"what", "why", "how", "when", "where", "who"}
    
    # POS tagging
    tagged_tokens = pos_tag(tokens)
    
    # Identify if input starts with a question word
    if tokens and tokens[0] in question_keywords:
        return False

    # Check for imperative sentences (verbs at the start)
    if tagged_tokens and tagged_tokens[0][1] in {"VB", "VBP"}:  # Verb, base form
        return True

    # Check for task-specific keywords
    if any(token in task_keywords for token in tokens):
        return True

    # Additional heuristic: long descriptive sentences with many nouns/adjectives are likely questions
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [token for token in tokens if token not in stop_words]
    noun_count = sum(1 for word, pos in tagged_tokens if pos.startswith("NN"))
    
    # If predominantly nouns/adjectives and no task-related context, treat as a question
    if noun_count > len(filtered_tokens) // 2:
        return False

    return False

# examples :
# print(is_task("What is Python?"))             # Output: False
# print(is_task("Create a function for me."))   # Output: True
# print(is_task("How do I learn programming?")) # Output: False
# print(is_task("Write a program to sort a list.")) # Output: True
# print(is_task("Fetch data from an API."))     # Output: True
