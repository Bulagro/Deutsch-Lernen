"""
Two dictionaries: One contains every word in worte.json, the other, every word that's registered
but not yet written in the file.

"""

import json, sys, os

class MissingValue(Exception):
    def __init__(self):
        self.message = 'Missing word.'

class InvalidSyntax(Exception):
    def __init__(self, msg):
        self.message = 'Invalid syntax: ' + msg

help_msg = """Adding words:
 - WordInDE : WordInES
 - DE1, DE2,.. : ES1, ES2,..
Other:
 - help                 display help
 - remove WordInDE      remove a word
 - search WordInDe      displays the word (if present)
 - confirm              add the newly added words to 'worte.json'
 - list                 list every word in 'worte.json'
 - log                  log every action
 - clear                clear the screen
 - exit                 exit """

WORDS_FILE_PATH = '/home/cristiangotchev/Documents/code/Python/Deutsch-Lernen/worte.json'
log = []


def print_log():
    global log

    for i in range(len(log)):
        print(f'{i}: {log[i]}')

def print_words(words_already_in_file:dict, words_to_add:dict):
    """ Prints every registered word. """
    if len(words_to_add) > 0:
        print('Pending: ')
        for word in words_to_add.items():
            de = word[0]
            es = word[1][1]
            print(f' - {de}: {", ".join(es)}')
    
    if len(words_already_in_file) > 0:
        print('In File:')
        for word in words_already_in_file.items():
            de = word[0]
            es = word[1][1]
            print(f' - {de}: {", ".join(es)}')

def search_word(word:str, words_already_in_file:dict, words_to_add:dict):
    """ Searches for a given word. Returns a list with all of it's meanings (if found)
        else returns None.
    """
    # A copy is necessary to prevent overriting data.
    total_words = words_already_in_file.copy()
    total_words.update(words_to_add)
    
    for w in total_words.keys():
        if word == w:
            return total_words[w][1]

    return None

def remove_word(word:str, words_already_in_file:dict, words_to_add:dict):
    """ Removes a word from the registry. """
    if word in words_to_add.keys():
        del words_to_add[word]
        log.append(f'Successfully removed \'{word}\' from words_to_add.')
        return True
    
    elif word in words_already_in_file.keys():
        del words_already_in_file[word]
        log.append(f'Successfully removed \'{word}\' from words_already_in_file.')
        return True

    else:
        print(f'{word} not found.')
        return False

def read_word_list(file=WORDS_FILE_PATH):
    """ Saves the contents of worte.json to memory. """
    global log
    try:
        with open(file, 'r') as w:
            try:
                word_list = json.load(w)
                log.append(f'\'{file}\' successfuly open.')
                return word_list

            # The file doesn't contain any json.
            except json.JSONDecodeError:
                log.append('Empty file: Creating initial config.')
                json.dump({}, w)
                return False

    except FileNotFoundError:
        log.append(f'Unable to open \'{file}\'. Please create \'{file}\' to continue.')
        return False

def add_word(de_words:list, es_words:list, words_already_in_file:dict, words_to_add:dict):
    """ Registers a new word. """
    global log
    for word in de_words:
        # If the word isn't registered - add it.
        if search_word(word, words_already_in_file, words_to_add) == None:
            words_to_add[word] = [0, es_words]
            log.append(f'Added: {word}:{es_words}.')
        
        # The word is registered - add a new meaning.
        else:
            word_meanings = words_to_add[word][1]
            word_meanings += list(set(es_words) - set(word_meanings))
            log.append(f'Updated meanings for {word} -> {word_meanings}.')

    return None

def merge_word_lists(words_already_in_file:dict, words_to_add:dict, file=WORDS_FILE_PATH):
    global log
    words_already_in_file.update(words_to_add)

    # This is done to write readable json to the file.
    with open(file, 'w') as word_file:
        l = json.dumps(words_already_in_file, sort_keys=True, indent=4)
        word_file.write(l)
        log.append(f'Successfully added new words to \'{file}\'.')
    
    words_to_add.clear()
    return None

def main(): # Main
    words_already_in_file = {}
    words_to_add = {}

    words_already_in_file = read_word_list()
    if not words_already_in_file:
        print_log()
        exit()

    while True:
        print('>> ', end='')
        words = str(input()).split(':')

        if words[0] == 'help':
            print(help_msg)
            continue
            
        elif 'remove' in words[0]:
            w = words[0].replace('remove', '').strip()
            remove_word(w, words_already_in_file, words_to_add)
            continue
    
        elif 'search' in words[0]:
            s = words[0].replace('search', '').strip()
            r = search_word(s, words_already_in_file, words_to_add)
            result = ', '.join(r) if r != None else None 
            print(f'{s}: {result}')
            continue

        elif words[0] == 'confirm':
            merge_word_lists(words_already_in_file, words_to_add)
            continue

        elif words[0] == 'log':
            print_log()
            continue

        elif words[0] == 'list':
            print_words(words_already_in_file, words_to_add)
            continue
        
        elif words[0] == 'clear':
            os.system('clear||cls')
            continue

        elif words[0] == 'exit':
            merge_word_lists(words_already_in_file, words_to_add)
            return None

        if len(words) != 2:
            print('Unknown command. Try \'help\'')
            continue

        de_words = [word for word in list(map(lambda w: w.strip(), words[0].split(','))) if word != '']
        es_words = [word for word in list(map(lambda w: w.strip(), words[1].split(','))) if word != '']

        add_word(de_words, es_words, words_already_in_file, words_to_add)
    
    return None


if __name__ == '__main__':    
    main()
    
# :)