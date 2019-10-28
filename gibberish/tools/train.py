import argparse
import os

from gibberish.config import MODEL_FILE_PATH, DATA_DIR
from gibberish.detector.markov_chain_model import MCMGibberishDetector
from gibberish.logger import get_logger

_logger = get_logger(__name__)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model', choices=['mcm'], help='Model name')
    parser.add_argument('-i', '--input', help='File with phrases', required=True)
    parser.add_argument('-o', '--output', default=MODEL_FILE_PATH, help='Output file for string log probabilities')
    parser.add_argument('--bad', default=os.path.join(DATA_DIR, 'bad.txt'), help='File with non-acceptable phrases')
    parser.add_argument('--good', default=os.path.join(DATA_DIR, 'good.txt'), help='File with acceptable phrases')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    if args.model == 'mcm':
        detector = MCMGibberishDetector()
        detector.train(args.input, args.bad, args.good)
        detector.save(args.output)
    else:
        raise ValueError('No {} gibberish detector implemented'.format(args.model))
