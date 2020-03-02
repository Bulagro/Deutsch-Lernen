import unittest
import lw_ref as l

class LearnTest(unittest.TestCase):
    def test_select_words_lenght(self):
        words_dict = {
            'hallo' : [0, ['hola']],
            'tschüss' : [0, ['adiós']],
            'der Hund' : [0, ['el perro']],
            'die Mutter' : [0, ['la mamá']],
            'der Vater' : [0, ['el padre']],
            'Juan' : [0, ['Juan']],
        }
        expected_lenght = 3
        words_list = l.select_words(words_dict, 3)
        self.assertEqual(len(words_list), expected_lenght)

    def test_select_words_content(self):
        words_dict = {
            'hallo' : [0, ['hola']],
            'tschüss' : [0, ['adiós']],
            'der Hund' : [0, ['el perro']],
            'die Mutter' : [0, ['la mamá']],
            'der Vater' : [0, ['el padre']],
            'Juan' : [0, ['Juan']],
        }
        expected_words_list = ['hallo', 'tschüss', 'der Hund']
        words_list = l.select_words(words_dict, 3)
        self.assertEqual(words_list, expected_words_list)

    def test_select_words_content_2(self):
        words_dict = {
            'hallo' : [1, ['hola']],
            'tschüss' : [0, ['adiós']],
            'der Hund' : [0, ['el perro']],
            'die Mutter' : [0, ['la mamá']],
            'der Vater' : [0, ['el padre']],
            'Juan' : [0, ['Juan']],
        }
        expected_words_list = ['tschüss', 'der Hund', 'die Mutter']
        words_list = l.select_words(words_dict, 3)
        self.assertEqual(words_list, expected_words_list)

if __name__ == "__main__":
    unittest.main()