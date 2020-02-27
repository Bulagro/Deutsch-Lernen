"""
# Temporal file to add words while I make my server (oh yes, it's happening).
# Add color.
# Redo in other language to add realtime key support.
# Multiple commands per line.

TODO:
- Word acuracy counter. (worte.json)
- Refactor pls

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

filename = '/home/cristiangotchev/Documents/code/Python/Deutsch/worte.json'

prev_words = {}
new_words = {}
logger = []
to_log = False

def print_logger():
    global logger

    for i in range(len(logger)):
        print(f'{i}: {logger[i]}')

def print_words():

    if len(new_words) > 0:
        print('Pending: ')
        for de, es in new_words.items():
            print(f' - {de}: {", ".join(es)}')
    
    if len(prev_words) > 0:
        print('In File:')
        for de, es in prev_words.items():
            print(f' - {de}: {", ".join(es)}')

def search_word(word):
    global new_words, prev_words

    for w in new_words.keys():
        if word == w:
            return new_words[w]
    
    for w in prev_words.keys():
        if word == w:
            return prev_words[w]

    return None

def remove_word(word):
    global new_words, prev_words

    if word in new_words.keys():
        del new_words[word]
        logger.append(f'Successfully removed \'{word}\' from new_words.')
        print('Done.')
        return True
    
    elif word in prev_words.keys():
        del prev_words[word]
        logger.append(f'Successfully removed \'{word}\' from prev_words.')
        print('Done.')
        return True

    else:
        print(f'{word} not found.')
        return False

def read_words():
    global prev_words

    try:
        with open(filename, 'r+') as w:
            try:
                prev_words = json.load(w)
                logger.append(f'\'{filename}\' successfuly open.')
                return True

            except json.JSONDecodeError:
                logger.append('Empty file: Creating initial config.')
                json.dump({}, w)
                return True

    except FileNotFoundError:
        logger.append(f'Unable to open \'{filename}\'. Please create \'{filename}\' to continue.')
        return False

def add_word(de_words, es_words):
    global prev_words, new_words, logger
    
    for word in de_words:
        if word in prev_words.items():
            logger.append(f'Skipping repeated word: {word}')
            continue

        new_words[word] = [0, es_words]
        logger.append(f'Added: {word}:{es_words}.')
        print('Done.')

    return None

def merge_word_lists():
    global prev_words, new_words

    prev_words.update(new_words)

    with open(filename, 'w') as f:
        l = json.dumps(prev_words, sort_keys=True, indent=4)
        f.write(l)
        
        logger.append(f'Successfully added new words to \'{filename}\'.')
        print('Done.')
    
    new_words.clear()
    return None

def parse_words():
    global to_log

    while True:
        print('>> ', end='')
        words = str(input()).split(':')

        if words[0] == 'help':
            print(help_msg)
            continue
            
        elif 'remove' in words[0]:
            w = words[0].replace('remove', '').strip()
            remove_word(w)
            continue
    
        elif 'search' in words[0]:
            s = words[0].replace('search', '').strip()
            r = search_word(s)
            result = ', '.join(r) if r != None else None 
            print(f'{s}: {result}')
            continue

        elif words[0] == 'confirm':
            merge_word_lists()
            continue

        elif words[0] == 'log':
            print_logger()
            continue

        elif words[0] == 'list':
            print_words()
            continue
        
        elif words[0] == 'clear':
            os.system('clear||cls')
            continue

        elif words[0] == 'exit':
            merge_word_lists()
            return None

        if len(words) != 2:
            print('Unknown command. Try \'help\'')
            continue

        de_words = [word for word in list(map(lambda w: w.strip(), words[0].split(','))) if word != '']
        es_words = [word for word in list(map(lambda w: w.strip(), words[1].split(','))) if word != '']

        add_word(de_words, es_words)
    
    return None


if __name__ == '__main__':
    if not read_words():
        print_logger()
        exit()
    
    parse_words()