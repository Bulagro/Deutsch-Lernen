import json

def change_point_counter(P: int):
    words = json.load(open('words.json', 'r'))
    for w in words:
        words[w]['points'] = P

    with open('words.json', 'w') as f:
        f.write(json.dumps(words, indent=4, sort_keys=True))

# change_point_counter(1)
