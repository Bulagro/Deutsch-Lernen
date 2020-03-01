import unittest
import aw_ref as a

class AddWordsRefactoredTest(unittest.TestCase):
    def test_read_word_list(self):
        self.assertEqual(type(a.read_word_list()), type({}))
        self.assertFalse(a.read_word_list('.json'))

    def test_search_word(self):
        prev_words = a.read_word_list()
        self.assertEqual(a.search_word('hübsch', prev_words, {}), ['guapo'])
        self.assertEqual(a.search_word('babt', prev_words, {}), None)

    def test_add_new_word(self):
        word_list = {}
        a.add_word(['deutsch'], ['alemán'], {}, word_list)
        self.assertEqual(word_list, {'deutsch':[0, ['alemán']]})

    def test_add_not_new_word(self):
        word_list = {'der Ehemann':[0, ['el marido']]}
        expected_word_list = {'der Ehemann':[0, ['el marido', 'el esposo']]}
        a.add_word(['der Ehemann'], ['el esposo'], {}, word_list)
        self.assertEqual(word_list, expected_word_list)
    
    def test_add_new_word_to_words_to_add_dict(self):
        word_list = {'der Ehemann':[0, ['el marido']]}
        words_to_add = {}
        words_to_add_expected = {'der Ehemann':[0, ['el marido', 'el esposo']]}
        a.add_word(['der Ehemann'], ['el esposo'], word_list, words_to_add)
        self.assertEqual(words_to_add, words_to_add_expected)

if __name__ == '__main__':
    unittest.main()

