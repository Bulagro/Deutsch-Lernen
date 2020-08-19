import json, sqlite3

def change_point_counter(P: int):
    words = json.load(open('words.json', 'r'))
    for w in words:
        words[w]['points'] = P

    with open('words.json', 'w') as f:
        f.write(json.dumps(words, indent=4))


def add_word_to_dict(de: list, es: list, words_file='words.json'):
    words = json.load(open(words_file, 'r'))

    word_id = str(len(words))
    word_dict_entry = {
        "de": de,
        "es": es,
    }

    words[word_id] = word_dict_entry

    with open(words_file, 'w') as w:
        w.write(json.dumps(words, indent=4))


def remove_points_var_from_json():
    words = json.load(open('words.json', 'r'))

    for w in words:
        del words[w]['points']

    with open('words.json', 'w') as w:
        w.write(json.dumps(words, indent=4))


def update_database(words_json='words.json', database='words.sqlite3'):
    # es: id, meaning
    # de: id, meaning
    # words: id, es_id, de_id, es_score, de_score

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
                ids[lang] = [n[0] for n in _ids]

        for i in ids['es']:
            for j in ids['de']:
                c.execute(f"""
                INSERT INTO words (es_id, es_score, de_id, de_score)
                VALUES ({i}, 0, {j}, 0);
                """)

    conn.commit()
