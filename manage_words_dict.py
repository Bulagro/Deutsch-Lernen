import json

def translate_old_dict():
    with open('worte.json', 'r') as worte_file:
        worte = json.load(worte_file)
        words = {}

        for i, w in enumerate(worte.items()):
            words[i] = {
                'points' : 0,
                'de'     : [w[0]],
                'es'     : w[1][1],
            }

        with open('words.json', 'w') as words_file:
            words_file.write(json.dumps(words, indent=4, sort_keys=True))

def merge_same_meanigns_into_same_entry():
    pass
