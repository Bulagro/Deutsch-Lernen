from dataclasses import dataclass
from sys import argv
from os import system
import sqlite3, json


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
        return f'{self.es}({self.es_score})::{self.de}({self.de_score})'


def update_database_from_json(words_json='words.json', database='words.sqlite3'):
    """ Reads some json file and fills the databse with it's information. """

    words_dict = json.load(open(words_json, 'r'))

    conn = sqlite3.connect(database)
    c = conn.cursor()

    # Clear previous database
    for table in ('words', 'es', 'de'):
        c.execute(f'DELETE FROM {table};')
        c.execute(f'DELETE FROM sqlite_sequence WHERE name="{table}";')

    for word_id in words_dict:
        ids = {
            'es' : [],
            'de' : [],
        }

        for lang in ('es', 'de'):
            for word in words_dict[word_id][lang]:
                c.execute(f'INSERT INTO {lang} (meaning) VALUES ("{word}");')
                _ids = c.execute(f'SELECT id FROM {lang} WHERE meaning = "{word}";').fetchall()
                ids[lang] += [n[0] for n in _ids]

        for i in ids['es']:
            for j in ids['de']:
                c.execute(f"""
                INSERT INTO words (es_id, es_score, de_id, de_score)
                VALUES ({i}, 0, {j}, 0);
                """)

    conn.commit()


def update_database_from_class_list(words_list: list, cursor: sqlite3.Cursor, connection: sqlite3.Connection, commit: bool):
    for word in words_list:
        for es in word.es:
            ids = [id[0] for id in cursor.execute(f'SELECT id FROM es WHERE meaning="{es}";').fetchall()]

            for id in ids:
                cursor.execute(f'UPDATE words SET es_score={word.es_score} WHERE es_id={id};')
                pass

        for de in word.de:
            ids = [id[0] for id in cursor.execute(f'SELECT id FROM de WHERE meaning="{de}";').fetchall()]

            for id in ids:
                cursor.execute(f'UPDATE words SET de_score={word.de_score} WHERE de_id={id};')
                pass

    if commit:
        connection.commit()


def reset_database(database='words.sqlite3'):
    connection = sqlite3.connect(database)
    cursor = connection.cursor()

    for lang in ('es', 'de'):
        cursor.execute(f'UPDATE words SET {lang}_score = 0;')

    connection.commit()


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


def main(ammount=10, lang='de'):
    other_lang = 'de' if lang == 'es' else 'es'

    connection = sqlite3.connect('words.sqlite3')
    cursor = connection.cursor()

    words_list = get_words(ammount, lang, cursor)

    for word in words_list:
        system('cls || clear') # This is temporal and only for the CLI.
        print(', '.join(eval(f'word.{other_lang}')), end='\n\n')

        user_input = input('> ')
        comparison = None

        if user_input == '.':
            break

        # Check user input
        for meaning in eval(f'word.{lang}'):
            comparison = compare_words(user_input, meaning)

            if comparison == True:
                if lang == 'es': word.es_score += 2
                else: word.de_score += 2
                break
            elif type(comparison) == int:
                if lang == 'es': word.es_score += 1
                else: word.de_score += 1
                break
        else:
            while not comparison:
                system('cls || clear')
                print(','.join(eval(f'word.{other_lang}')))
                print('Nope: ' + ', '.join(eval(f'word.{lang}')), end='\n\n')
                user_input = input('> ')

                for meaning in eval(f'word.{lang}'):
                    comparison = compare_words(user_input, meaning)
                    if comparison: break

    # Update database
    update_database_from_class_list(words_list, cursor, connection, False)
