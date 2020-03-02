"""
TODO:
    - Display word in a prettier way.
    - Keep track of what words I already know.
    - Add color.
    - Remove random
    - function to select most mistaken words.
"""
import json
from os import system

WORDS_FILE_PATH = '/home/cristiangotchev/Documents/code/Python/Deutsch-Lernen/worte.json'

def read_words_file(file=WORDS_FILE_PATH):
    words_in_file = None
    with open(file, 'r') as f:
        words_in_file = json.loads(f.read())
    
    return words_in_file

def select_words(words_in_file:dict, WORD_COUNT:int=50):
    words_list = [] # Contains each dictionary key.
    lowest_count = 0

    for word in words_in_file.keys():
        word_data = words_in_file[word]
        if word_data[0] <= lowest_count:
            if len(words_list) < WORD_COUNT:
                words_list.append(word)
            else:
                break
    
    return words_list
