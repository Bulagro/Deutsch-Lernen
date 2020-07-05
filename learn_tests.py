import learn
import unittest, json


total_words, complete_words_list = learn.get_words()

class TestGetWords(unittest.TestCase):
    def test_get_first_100_words(self):
        w = learn.select_words(100)

        expected_words_list = [
            complete_words_list[str(i)] for i in range(100)
        ]

        self.assertEqual(100, len(w))
        self.assertEqual(expected_words_list, w)

if __name__ == "__main__":
    unittest.main()
