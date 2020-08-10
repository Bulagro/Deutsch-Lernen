import json

def change_point_counter(P: int):
    words = json.load(open('words.json', 'r'))
    for w in words:
        words[w]['points'] = P

    with open('words.json', 'w') as f:
        f.write(json.dumps(words, indent=4, sort_keys=True))


def add_word_to_dict(de: list, es: list, words_file='words.json'):
    words = json.load(open(words_file, 'r'))

    word_id = str(len(words))
    word_dict_entry = {
        "de": de,
        "es": es,
        "points" : 0,
    }

    words[word_id] = word_dict_entry

    with open(words_file, 'w') as w:
        w.write(json.dumps(words, indent=4))
