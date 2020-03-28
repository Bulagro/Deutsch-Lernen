import json
from random import choice
from os import system
from learn import WORDS_FILE_PATH, read_words_file

WORD_LIST_BUFFER = 10

def select_word(words_dict:dict, word_list:list):
    selected_word = choice(list(words_dict.keys()))
    while select_word in word_list:
        selected_word = choice(list(words_dict.keys()))
    
    return selected_word

def update_word_list(words_dict:dict, word_list:list):
    while len(word_list) < WORD_LIST_BUFFER:
        word_list.append(select_word(words_dict, word_list))

def get_word_meanings(words_dict:dict, word_key:str):
    return ', '.join(words_dict[word_key][1])

def cycle_array(word_list:list):
    for i in range(1, WORD_LIST_BUFFER):
        word_list[i-1] = word_list[i]

def main():
    words_dict = read_words_file()
    word_list = []
    update_word_list(words_dict, word_list)

    while True:
        system("cls||clear")

        first_word = word_list[0]
        print(f"DE: {first_word}\nES: {get_word_meanings(words_dict, first_word)}")
        input("")
        
        cycle_array(word_list)
        word_list.pop()
        update_word_list(words_dict, word_list)


if __name__ == "__main__":
    main()
