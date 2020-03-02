"""
TODO:
    - Display word in a prettier way.
    - Add color.
"""
import json
from os import system

WORDS_FILE_PATH = '/home/cristiangotchev/Documents/code/Python/Deutsch-Lernen/worte.json'

def read_words_file(file=WORDS_FILE_PATH):
    """ Saves the contents of 'file' to memory. """
    words_in_file = None
    with open(file, 'r') as f:
        words_in_file = json.loads(f.read())
    
    return words_in_file

def select_words(words_dict:dict, WORD_COUNT:int=50):
    """ Returns a list with the 'WORD_COUNT' number of words with
        the lowest score.
    """
    words_list = [] # Contains each dictionary key.
    lowest_count = 0

    while len(words_list) < WORD_COUNT:
        for word in words_dict.keys():
            word_data = words_dict[word]
            if word_data[0] <= lowest_count:
                if len(words_list) < WORD_COUNT:
                    words_list.append(word)
                else:
                    break
        else:
            lowest_count += 1
    
    return words_list

def compare_words(inpt:str, word_key:str, words_dict:dict):
    return True if inpt in words_dict[word_key][1] else False

def modify_word_score(word_key:str, words_dict:dict, value:int):
    if value > 0:
        words_dict[word_key][0] += 1
        if words_dict[word_key][0] == 100:
            words_dict[word_key][0] = 0
    else:
        words_dict[word_key][0] = words_dict[word_key][0]-1 if words_dict[word_key][0]-1 > 0 else 0

    return True

def re_write_words_file(words_dict:dict, file=WORDS_FILE_PATH):
    with open(file, 'w') as word_file:
        output = json.dumps(words_dict, sort_keys=True, indent=4)
        word_file.write(output)

def main():
    words_dict = read_words_file()
    word_key_list = select_words(words_dict, 3)
    word_index = 0

    while True:
        word = word_key_list[word_index]
        
        system('cls||clear')
        print(f'\n {word}, {word_key_list}', end='\n\n')
        
        usr_input = str(input('>> '))

        if usr_input == 'exit':
            re_write_words_file(words_dict)
            return None
        
        compare_result = compare_words(usr_input, word, words_dict)
        if compare_result:
            
            word_index += 1
            modify_word_score(word, words_dict, 1)

            if word_index == len(word_key_list):
                word_key_list = select_words(words_dict, 3)
                word_index = 0
            continue
        else:
            modify_word_score(word, words_dict, -1)
            print('A: ' + ', '.join(words_dict[word][1]), end='')
            input('')

if __name__ == "__main__":
    main()