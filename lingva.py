import re
from collections import Counter, defaultdict, deque
from itertools import islice


class NgramsTextParser:
    def __init__(self, raw_text):
        self.raw_text = raw_text
        self.word_mask = re.compile('[\w]+')
        self.simple_sentence_mask = re.compile('[\w\W]+?[.;?!]')
        self.weight_dict = defaultdict(Counter)
        self.sentences_list = []
        self.word_weights = Counter()
        self.separator = '.'

    def split_to_sentences(self):
        sentences = self.simple_sentence_mask.findall(self.raw_text)
        sentences = [x for x in sentences if not (('\r' in x) or ('\n' in x) or (x == '..'))]
        self.sentences_list = sentences
        return sentences

    def parse_text(self):
        words_list = [self.word_mask.findall(sentence) for sentence in self.sentences_list]
        for sentence in words_list:
            for current_word, next_word in zip(sentence, sentence[1:]):
                self.weight_dict[current_word.lower()][next_word.lower()] += 1

    def generate_chains(self):
        words_chains = dict(self.weight_dict)
        key_stack = deque((key for key in words_chains))
        while len(key_stack) > 0:
            current_key = key_stack.pop()
            key_stack.append(current_key)
            yield current_key
            try:
                for key in words_chains[current_key]:
                    key_stack.append(key)
                words_chains[current_key] = None
            except (KeyError, TypeError) as e:
                yield self.separator
                key_stack.pop()
                pass



class NonsenseGenerator:
    def __init__(self, raw_text):
        self.text_parser = NgramsTextParser(raw_text)
        self.text_parser.split_to_sentences()
        self.text_parser.parse_text()
        self.text_stack = []
        self.min_sentence_length = 5
        self.max_sentence_length = 1000
        self.sentences_amount = 5
        self.taboo_words = ['an', 'a', 'the', 'to', 'in', 'and', 'but', 'is', 'of']

    def generate_sentence_list(self):
        words_stack = []
        for word in self.text_parser.generate_chains():
            if word != self.text_parser.separator:
                words_stack.append(word)
            else:
                if words_stack[-1] in self.taboo_words:
                    words_stack.pop()
                if self.min_sentence_length <= len(words_stack) <= self.max_sentence_length:
                    yield words_stack
                    words_stack = []

    def generate(self, sentences_amount=5, min_sentence_length=5, max_sentence_length=1000, set_params=False):
        def join_words_lists_to_text(text_stack):
            return ". ".join([" ".join(word).capitalize() for word in text_stack]) + "."

        if set_params:
            self.sentences_amount = sentences_amount
            self.min_sentence_length = min_sentence_length
            self.max_sentence_length = max_sentence_length

        return join_words_lists_to_text(islice(self.generate_sentence_list(), self.sentences_amount))



if __name__ == "__main__":
    pass
