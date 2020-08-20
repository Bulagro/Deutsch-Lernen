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



if __name__ == "__main__":
    unittest.main()
