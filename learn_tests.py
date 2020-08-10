import learn
import unittest, json


total_words, complete_words_list = learn.get_words()

class TestSelectWords(unittest.TestCase):
    def test_get_first_100_words(self):
        w = learn.select_words(WORDS_PER_SESSION=100)

        expected_words_list = [
            complete_words_list[str(i)] for i in range(100)
        ]

        self.assertEqual(expected_words_list, w)

    def test_get_more_words_than_actual_words_in_dict(self):
        from os import system

        # Temporary dictionary file
        with open('tmp_words.json', 'w') as f:
            new_dict = {
                i : { "de":"a", "es":"a", "points": 0 }
                for i in range(3)
            }

            f.write(json.dumps(new_dict))

        with open('tmp_words.json', 'r') as f:
            words_dict = json.load(f)
            selected_words = learn.select_words('tmp_words.json', 6)
            expected_words = [
                words_dict[str(i)] for i in range(3)
            ] * 2

            self.assertEqual(expected_words, selected_words)

        system('rm tmp_words.json')


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
