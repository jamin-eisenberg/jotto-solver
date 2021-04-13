import unittest
from main import *

class Tester(unittest.TestCase):
    def test_get_allwords_and_guesses(self):
        self.assertEqual(get_allwords_and_guesses("exampleWords.txt", "example.txt", 4),
                        ([[2, 14, 20, 15], [3, 14, 6, 18], [3, 14, 13, 18],
                                 [3, 14, 18, 19], [7, 0, 21, 4], [17, 14, 3, 18],
                                 [18, 11, 8, 15], [18, 14, 22, 18], [18, 20, 3, 18]],
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

    def test_str_to_list_nums(self):
        self.assertEqual(str_to_list_nums(""), [])
        self.assertEqual(str_to_list_nums("a"), [0])
        self.assertEqual(str_to_list_nums("b"), [1])
        self.assertEqual(str_to_list_nums("m"), [12])
        self.assertEqual(str_to_list_nums("y"), [24])
        self.assertEqual(str_to_list_nums("z"), [25])
        self.assertEqual(str_to_list_nums("abmyz"), [0, 1, 12, 24, 25])
        self.assertEqual(str_to_list_nums("dogs"), [3, 14, 6, 18])
        self.assertRaises(ValueError, str_to_list_nums, "A")
        self.assertRaises(ValueError, str_to_list_nums, "{")
        self.assertRaises(ValueError, str_to_list_nums, "Z")
        self.assertRaises(ValueError, str_to_list_nums, "abracaDABra")

    def test_list_nums_to_str(self):
        self.assertEqual(list_nums_to_str([]), "")
        self.assertEqual(list_nums_to_str([0]), "a")
        self.assertEqual(list_nums_to_str([1]), "b")
        self.assertEqual(list_nums_to_str([12]), "m")
        self.assertEqual(list_nums_to_str([24]), "y")
        self.assertEqual(list_nums_to_str([25]), "z")
        self.assertEqual(list_nums_to_str([0, 1, 12, 24, 25]), "abmyz")
        self.assertEqual(list_nums_to_str([3, 14, 6, 18]), "dogs")
        self.assertRaises(ValueError, list_nums_to_str, [-1])
        self.assertRaises(ValueError, list_nums_to_str, [26])
        self.assertRaises(ValueError, list_nums_to_str, [1, 2, 4, 8, 16, 32, 64])

    def test_get_char_from_num(self):
        self.assertEqual(num_to_char(0), 'a')
        self.assertEqual(num_to_char(1), 'b')
        self.assertEqual(num_to_char(12), 'm')
        self.assertEqual(num_to_char(24), 'y')
        self.assertEqual(num_to_char(25), 'z')
        self.assertRaises(ValueError, num_to_char, -1)
        self.assertRaises(ValueError, num_to_char, 26)
        self.assertRaises(ValueError, num_to_char, 97)

    def test_get_num_from_char(self):
        self.assertEqual(char_to_num('a'), 0)
        self.assertEqual(char_to_num('b'), 1)
        self.assertEqual(char_to_num('m'), 12)
        self.assertEqual(char_to_num('y'), 24)
        self.assertEqual(char_to_num('z'), 25)
        self.assertRaises(ValueError, char_to_num, 'A')
        self.assertRaises(ValueError, char_to_num, '{')
        self.assertRaises(ValueError, char_to_num, 'Z')
        self.assertRaises(TypeError, char_to_num, '')
        self.assertRaises(TypeError, char_to_num, 'hi')

    def test_match_number(self):
        self.assertEqual(match_number("cats", "dogs"), 1)
        self.assertEqual(match_number("spool", "cools"), 4)
        self.assertEqual(match_number("Rose", "rats"), 2)
        self.assertEqual(match_number("dog", "cat"), 0)

    def test_lower_case_AZ(self):
        self.assertEqual(lower_case_AZ("cats"), True)
        self.assertEqual(lower_case_AZ("dogs"), True)
        self.assertEqual(lower_case_AZ("spool"), True)
        self.assertEqual(lower_case_AZ("sdpfwpfnx"), True)
        self.assertEqual(lower_case_AZ("Cats"), False)
        self.assertEqual(lower_case_AZ("Rose"), False)
        self.assertEqual(lower_case_AZ("dksoI"), False)
        self.assertEqual(lower_case_AZ("runner1"), False)
        self.assertEqual(lower_case_AZ("l3tter"), False)
        self.assertEqual(lower_case_AZ("not-a-word"), False)
        self.assertEqual(lower_case_AZ("runner;"), False)


if __name__ == '__main__':
    unittest.main()
