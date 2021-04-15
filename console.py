import argparse
import lingva
import os
import sys
import random

def configure_parser():
    parser = argparse.ArgumentParser(description='''Usage: console.py -l warandpeace -s 10 - will generate you ten
     nonsense sentences''')
    parser.add_argument('-l', '--learn', nargs=1, required= True , type=str, help='pass the path to file which contains'
                                                                                  'learn data.')
    parser.add_argument('-s', '--sentences', nargs='+', type=int,action=parse_sentence_length(),
                        required=True,
                        help='the necessary number of nonsense sentences that you want to generate.')
    parser.add_argument('-n', '--ngrams', type=int, help= 'it\'s a minimal desired size of sentences')
    return parser


def parse_sentence_length():
    class RequiredLength(argparse.Action):
        def __call__(self, parser, args, values, option_string=None):
            if not 1 <= len(values) <= 2:
                msg = 'argument "{f}" requires number or range length 2 arguments'.format(
                    f=self.dest)
                raise argparse.ArgumentTypeError(msg)
            if len(values) == 1:
                values = values[0]
            else:
                values = random.randint(*values)
            setattr(args, self.dest, values)

    return RequiredLength


def read_data_source(file_path):
    if os.path.isfile(file_path):
        with open(file_path, 'rt') as data:
            return data.read()
    else:
        print('File:{} not found'.format(file_path))
        exit(1)

if __name__ == '__main__':
    arg_parser = configure_parser()
    namespace = arg_parser.parse_args(sys.argv[1:])
    raw_text = read_data_source(namespace.learn[0])
    d = lingva.NonsenseGenerator(raw_text)

    if namespace.sentences:
        d.sentences_amount = namespace.sentences
    if namespace.ngrams:
        d.min_sentence_length = namespace.ngrams
    print(d.generate())
