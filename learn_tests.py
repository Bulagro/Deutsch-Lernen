import learn
import unittest, sqlite3


connection = sqlite3.connect('words.sqlite3')
cursor = connection.cursor()

class TestGetWords(unittest.TestCase):
    def test_get_words_returns_list_of_first_word_only(self):
        actual = learn.get_words(2, 'es', cursor)
        expected = [
            learn.Word(['salir', 'partir'], 0, ['abfahren'], 0)
        ]

        self.assertEqual(actual, expected)

    def test_get_words_first_two_words(self):
        actual = learn.get_words(3, 'de', cursor)
        expected = [
            learn.Word(['salir', 'partir'], 0, ['abfahren'], 0),
            learn.Word(['recoger'], 0, ['abholen'], 0),
        ]

        self.assertEqual(actual, expected)

    def test_ignore_word_with_small_id_when_lang_score_is_bigger(self):
        # Set es_score of 'abholen'::'recoger' to 1.
        # Don't commit, this is only temporal.
        cursor.execute('UPDATE words SET es_score=1 WHERE id=3;')

        actual = learn.get_words(3, 'es', cursor)
        expected = [
            learn.Word(['salir', 'partir'], 0, ['abfahren'], 0),
            learn.Word(['emplear'], 0, ['anstellen'], 0),
        ]

        self.assertEqual(actual, expected)

        # Revert all changes in this transaction, to prevent interference with other tests.
        cursor.execute('ROLLBACK;')


class TestCompareWords(unittest.TestCase):
    def test_compare_almost_equal_words(self):
        actual = learn.compare_words('hola', 'ohla')
        expected = 0

        self.assertEqual(expected, actual)

        actual = learn.compare_words('Pudín', 'Puídn')
        expected = 2

        self.assertEqual(expected, actual)

    def test_compare_different_words(self):
        actual = learn.compare_words('adiós', 'hola')

        self.assertFalse(actual)

    def test_compare_equal_words(self):
        actual = learn.compare_words('manzana', 'manzana')

        self.assertTrue(actual)

    def test_empty_strings(self):
        actual = learn.compare_words('', '')

        self.assertTrue(actual)


class TestUpdateDatabaseFromClassList(unittest.TestCase):
    def test_update_one_word(self):
        words_list = [
            learn.Word(['salir', 'partir'], 1, ['abfahren'], 0)
        ]

        expected = [(1, 1, 1, 0), (2, 1, 1, 0)]
        learn.update_database_from_class_list(words_list, cursor, connection, False)

        actual = cursor.execute('SELECT es_id, es_score, de_id, de_score FROM words WHERE id < 3;').fetchall()

        self.assertEqual(expected, actual)
        cursor.execute('ROLLBACK;')

    def test_update_two_consecutive_words(self):
        words_list = [
            learn.Word(['salir', 'partir'], 1, ['abfahren'], 0),
            learn.Word(['recoger'], 2, ['abholen'], 0),
        ]

        expected = [(1, 1, 1, 0), (2, 1, 1, 0), (3, 2, 2, 0)]
        learn.update_database_from_class_list(words_list, cursor, connection, False)

        actual = cursor.execute('SELECT es_id, es_score, de_id, de_score FROM words WHERE id < 4;').fetchall()

        self.assertEqual(expected, actual)
        cursor.execute('ROLLBACK;')


if __name__ == "__main__":
    unittest.main()
