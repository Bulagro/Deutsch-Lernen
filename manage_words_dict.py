import json

def change_point_counter(P: int):
    words = json.load(open('words.json', 'r'))
    for w in words:
        words[w]['points'] = P

    with open('words.json', 'w') as f:
        f.write(json.dumps(words, indent=4))


def add_word_to_dict(de: list, es: list, WORDS_FILE='words.json'):
    words = json.load(open(WORDS_FILE, 'r'))

    word_id = str(len(words))
    word_dict_entry = {
        "de": de,
        "es": es,
        "points" : 0,
    }

    words[word_id] = word_dict_entry

    with open(WORDS_FILE, 'w') as w:
        w.write(json.dumps(words, indent=4))


def remove_points_var_from_json():
    words = json.load(open('words.json', 'r'))

    for w in words:
        del words[w]['points']

    with open('words.json', 'w') as w:
        w.write(json.dumps(words, indent=4))

