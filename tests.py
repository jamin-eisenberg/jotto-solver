import unittest
from main import *

class Tester(unittest.TestCase):
    def test_get_allwords_and_guesses(self):
        self.assertEqual(get_allwords_and_guesses("exampleWords.txt", "example.txt", 4),
                        (sorted(['have', 'slip', 'coup', 'sows', 'suds', 'dost', 'rods', 'dons', 'dogs']),
                         {'have': 0, 'slip': 1, 'coup': 1, 'sows': 2, 'suds': 2, 'dost': 3, 'rods': 3, 'dons': 3, 'dogs': 4}))
        self.assertRaises(ValueError, get_allwords_and_guesses, "exampleWordsBad.txt", "example.txt", 4)
        self.assertRaises(FileNotFoundError, get_allwords_and_guesses, "exampleordsBad.txt", "example.txt", 4)
        self.assertRaises(FileNotFoundError, get_allwords_and_guesses, "exampleWordsBad.txt", "exmple.txt", 4)


    def test_binary_search(self):
        self.assertEqual(binary_search(1, []), -1)
        self.assertEqual(binary_search('', []), -1)
        self.assertEqual(binary_search(1, [1]), 0)
        self.assertEqual(binary_search(1, [0]), -1)
        self.assertEqual(binary_search(2, [1, 2, 3]), 1)
        self.assertEqual(binary_search("hello", ["goodbye", "hello", "former", "raise"]), 1)
        self.assertEqual(binary_search("hello", ["goodbye", "hell", "former", "raise"]), -1)


if __name__ == '__main__':
    unittest.main()
