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

    def test_get_char_from_num(self):
        self.assertEqual(get_char_from_num(0), 'a')
        self.assertEqual(get_char_from_num(1), 'b')
        self.assertEqual(get_char_from_num(12), 'm')
        self.assertEqual(get_char_from_num(24), 'y')
        self.assertEqual(get_char_from_num(25), 'z')
        self.assertRaises(ValueError, get_char_from_num, -1)
        self.assertRaises(ValueError, get_char_from_num, 26)
        self.assertRaises(ValueError, get_char_from_num, 97)

    def test_get_num_from_char(self):
        self.assertEqual(get_num_from_char('a'), 0)
        self.assertEqual(get_num_from_char('b'), 1)
        self.assertEqual(get_num_from_char('m'), 12)
        self.assertEqual(get_num_from_char('y'), 24)
        self.assertEqual(get_num_from_char('z'), 25)
        self.assertEqual(get_num_from_char('a'), 0)
        self.assertRaises(ValueError, get_num_from_char, 'A')
        self.assertRaises(ValueError, get_num_from_char, '{')
        self.assertRaises(ValueError, get_num_from_char, 'Z')
        self.assertRaises(TypeError, get_num_from_char, '')
        self.assertRaises(TypeError, get_num_from_char, 'hi')


if __name__ == '__main__':
    unittest.main()
