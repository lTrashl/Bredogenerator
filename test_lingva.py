import unittest
import os
import sys
import re
import console
import lingva
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))


class TestLingva(unittest.TestCase):
    def test_NgramsTextParser(self):
        raw_data = console.read_data_source('./warandpeace')
        text_parser = lingva.NgramsTextParser(raw_data)
        with self.subTest('split text to sentences'):
            data = text_parser.split_to_sentences()
            self.assertTrue(str(type(data)) == "<class 'list'>")
            self.assertTrue(all([str(type(x)) == "<class 'str'>" for x in data]))
        with self.subTest('data was parsed'):
            text_parser.parse_text()
            self.assertTrue(len([keys for keys in text_parser.weight_dict]) > 0)
        with self.subTest('check correct run chain generation'):
            word_regex = re.compile('[\w]+|[.;?!]')
            for x in text_parser.generate_chains():
                self.assertRegex(x, word_regex)

    def test_NonsenseGenerator(self):
        raw_data = console.read_data_source('./warandpeace')
        gener = lingva.NonsenseGenerator(raw_data)
        text = gener.generate()
        splited = text.split('.')

        self.assertTrue(len(splited) == 6 and all([len(x.split()) > 4 for x in splited[:-1]]))


    def test_parse_sentence_length(self):
        self.assertEqual(4,4)

if __name__ == '__main__':
    unittest.main()