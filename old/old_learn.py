"""
TODO:
    - Display word in a prettier way.
    - Keep track of what words I already know.
    - Add color.
    - Remove random
    - function to select most mistaken words.
"""
import json
from random import choice, seed
from time import perf_counter
from os import system

WORDS_FILE_PATH = '/home/cristiangotchev/Documents/code/Python/Deutsch-Lernen/worte.json'
seed(perf_counter)

def main():
    words_in_file = None
    # Save all words to memory
    with open(WORDS_FILE_PATH, 'r') as f:
        words_in_file = json.load(f)

    new_word = choice(list(words_in_file.keys()))
    while True:
        system('cls||clear')
        word = new_word

        print(f'\n {word}', end='\n\n')
        inpt = str(input('>> '))

        if inpt == 'exit':
            return None

        # Do main loop
        for i in words_in_file[word][1]:
            if inpt == i:
                # counter +1
                new_word = choice(list(words_in_file.keys()))
                break
        else:
            print('A: ' + ', '.join(words_in_file[word][1]), end='')
            input('')

if __name__ == "__main__":
    main()
