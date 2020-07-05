import json

# Select n number of words (that's a session).
# display them in a given direction (zB. german -> spanish)
# update

def get_words(WORDS_PER_SESSION=100):
    with open('words.json', 'r') as f:
        words = json.load(f)
        total = words['total']
        del words['total']

        return(total, words)

def select_words(WORDS_PER_SESSION=100):
    """ Returns a list with WORDS_PER_SESSION words. """

    t, w = get_words()

    words_list = []
    min_points = 0
    while len(words_list) < WORDS_PER_SESSION:
        for word in w:
            if word == 'total': break

            if w[word]['points'] <= min_points:
                words_list.append(w[word])

                if len(words_list) == WORDS_PER_SESSION:
                    break
            else:
                min_points += 1

    return words_list

def main():
    pass
