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
    words = json.load(open('words.json', 'r'))

    while True:
        total_keys = len(words.keys())
        done = True
        for i in range(total_keys):
            if str(i) in words.keys():
                es_meanings = words[str(i)]['es']

                for j in range(i + 1, total_keys):
                    if str(j) in words.keys():
                        if words[str(j)]['es'] == es_meanings and i != j:
                            words[str(i)]['de'] += words[str(j)]['de']
                            words.pop(str(j))
                            done = False
                            print(f'Remove entry {j} (same meaning as {i})')
                            break

            if not done:
                break

        if done:
            with open('words.json', 'w') as f:
                f.write(json.dumps(words, indent=4, sort_keys=True))
            return True


# translate_old_dict()
# merge_same_meanigns_into_same_entry()
