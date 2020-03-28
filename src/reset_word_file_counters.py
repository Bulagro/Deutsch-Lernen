import json
from random import randint
from learn import WORDS_FILE_PATH

word_dict = None

with open(WORDS_FILE_PATH, 'r') as f:
    word_dict = json.load(f)

for w in word_dict.keys():
    word_dict[w][0] = 0

with open(WORDS_FILE_PATH, 'w') as f:
    output = json.dumps(word_dict, sort_keys=True, indent=4)
    f.write(output)
