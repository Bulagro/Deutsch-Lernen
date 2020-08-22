from dataclasses import dataclass
import sqlite3


@dataclass
class Word():
    def __init__(self, es: str, es_score: int, de: str, de_score: int):
        self.es = es
        self.de = de
        self.es_score = es_score
        self.de_score = de_score

    def __eq__(self, other):
        if type(other) != type(self):
            return False

        return self.es == other.es and self.de == other.de

    def __repr__(self):
        return f'{self.es}::{self.de}'


def get_words(ammount: int, lang: str, cursor: sqlite3.Cursor):
    """ Returns a list of Word()s. """

    if lang not in ('es', 'de'): raise Exception(f'Language "{lang}" not supported.')

    words_raw = cursor.execute(f"""
    SELECT
     es.meaning AS es,
     es_score,
     de.meaning AS de,
     de_score
    FROM
     words
     INNER JOIN es ON es.id = words.es_id
     INNER JOIN de ON de.id = words.de_id
    ORDER BY {lang + '_score'}
    LIMIT 0, {ammount};
    """).fetchall()

    words = []
    word = None

    # Build words! (merge those that go together)
    for raw_word in words_raw:
        es, es_s, de, de_s = raw_word

        if not word:
            word = Word([es], es_s, [de], de_s)
        else:
            if es in word.es:
                word.de.append(de)
                word.de_score += de_s
            elif de in word.de:
                word.es.append(es)
                word.es_score += es_s
            else:
                words.append(word)
                word = Word([es], es_s, [de], de_s)
                continue

    if word:
        words.append(word)

    return words


def compare_words(a: str, b: str):
    """ Returns whether two strings are equal (True), similar (i) or differently (False) written. """

    def count_letters(s: str):
        return {l : s.count(l) for l in set(s)}

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
