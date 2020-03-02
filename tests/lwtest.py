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

    def test_compare_words(self):
        words_dict = l.read_words_file()
        compare_result = l.compare_words('guapo', 'hübsch', words_dict)
        self.assertTrue(compare_result)
        
        compare_result = l.compare_words('feo', 'hübsch', words_dict)
        self.assertFalse(compare_result)

    def test_increase_word_score(self):
        words = {'hübsch':[0, ['guapo']]}
        expected_score = 1
        l.modify_word_score('hübsch', words, 1)
        self.assertEqual(words['hübsch'][0], expected_score)

    def test_decrease_word_score(self):
        words = {'hübsch':[1, ['guapo']]}
        expected_score = 0
        l.modify_word_score('hübsch', words, -1)
        self.assertEqual(words['hübsch'][0], expected_score)

        words = {'hübsch':[0, ['guapo']]}
        expected_score = 0
        l.modify_word_score('hübsch', words, -1)
        self.assertEqual(words['hübsch'][0], expected_score)

if __name__ == "__main__":
    unittest.main()