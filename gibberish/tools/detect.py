import argparse

from gibberish.config import MODEL_FILE_PATH
from gibberish.detector.markov_chain_model import MCMGibberishDetector
from gibberish.detector.heuristics_model import HeuristicsGibberishDetector
from gibberish.detector.utils import read_lines
from gibberish.logger import get_logger

_logger = get_logger(__name__)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model', choices=['mcm', 'heuristics'], help='Model name')
    parser.add_argument('--model-path', default=MODEL_FILE_PATH, help='File with model')
    parser.add_argument('-i', '--input', help='File with phrases. If not provided then console input is read')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    if args.model == 'mcm':
        detector = MCMGibberishDetector()
        detector.load(args.model_path)
    elif args.model == 'heuristics':
        detector = HeuristicsGibberishDetector()
    else:
        raise ValueError('No {} gibberish detector implemented'.format(args.model))

    for line in read_lines(args.input):
        print('Received line: {}'.format(line))

        if detector.is_gibberish(line):
            print('Gibberish')
        else:
            print('Okay')
