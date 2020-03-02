import json
from random import randint

word_dict = None
filename = '/home/cristiangotchev/Documents/code/Python/Deutsch-Lernen/worte.json'

with open(filename, 'r') as f:
    word_dict = json.load(f)

for w in word_dict.keys():
    word_dict[w][0] = 0

with open(filename, 'w') as f:
    output = json.dumps(word_dict, sort_keys=True, indent=4)
    f.write(output)
