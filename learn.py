import json


def get_words(WORDS_FILE='words.json'):
    """ Return the ammount of words and a the loaded dictionary from words.json """

    with open(WORDS_FILE, 'r') as f:
        words = json.load(f)

        return(len(words), words)


def select_words(WORDS_FILE='words.json', WORDS_PER_SESSION=100):
    """ Returns a list with WORDS_PER_SESSION words. """

    _, w = get_words(WORDS_FILE)

    words_list = []
    min_points = 0
    while len(words_list) < WORDS_PER_SESSION:
        for word in w:
            if w[word]['points'] <= min_points:
                words_list.append(w[word])

                if len(words_list) == WORDS_PER_SESSION:
                    break
            else:
                min_points += 1

    return words_list


def compare_words(a: str, b: str):
    """ Returns whether two strings are equal (True), similar (i) or differently (False) written. """

    def count_letters(s: str):
        return {l : s.count(l) for l in sorted(set(s))}

    if count_letters(a) != count_letters(b):
        return False

    else:
        a, b = list(a), list(b)
        for i in range(len(a)):
            if b[i] != a[i] and i < len(b) - 1:
                b[i], b[i + 1] = b[i + 1], b[i]

                if a == b:
                    return i
                else:
                    return False

    return True


def main():
    pass
