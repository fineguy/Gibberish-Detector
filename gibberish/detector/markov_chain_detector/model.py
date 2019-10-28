import pickle

import numpy as np
from nltk import ngrams

from gibberish.logger import get_logger
from gibberish.detector.abstract_model import AbstractTrainableGibberishDetector
from gibberish.detector.utils import read_lines

from .config import ACCEPTED_CHARS, CHAR_TO_IDX, ALLOWED_LINE_PATTERN

_logger = get_logger(__name__)


def _normalize(line):
    """
    Returns only the subset of chars from `ACCEPTED_CHARS`. This helps to keep the model relatively small by ignoring
    punctuation, infrequent symbols, etc.

    :param line:
    :return:
    """
    return ALLOWED_LINE_PATTERN.sub('', line.lower())


def _avg_transition_prob(normalized_line, log_probs_mat):
    """
    Returns the average transition probability in `normalized_line` using `log_probs_mat`.

    :param normalized_line:
    :param log_probs_mat:
    :return:
    """
    log_prob = 0.0
    transition_count = 0

    for transition_count, (char1, char2) in enumerate(ngrams(normalized_line, 2)):
        log_prob += log_probs_mat[CHAR_TO_IDX[char1]][CHAR_TO_IDX[char2]]

    return np.exp(log_prob / max(transition_count, 1))


def _read_normalized_lines(file_path=None):
    """
    Reads lines from file or input and normalizes them.

    :param file_path:
    :return:
    """
    for line in read_lines(file_path):
        yield _normalize(line)


class MCMGibberishDetector(AbstractTrainableGibberishDetector):
    def __init__(self):
        super().__init__()

        self._log_probs_mat = None
        self._prob_threshold = None

    def is_gibberish(self, text):
        if _avg_transition_prob(_normalize(text), self._log_probs_mat) >= self._prob_threshold:
            return False
        return True

    def save(self, model_path):
        with open(model_path, 'wb') as fout:
            pickle.dump({'matrix': self._log_probs_mat, 'threshold': self._prob_threshold}, fout)

    def load(self, model_path):
        with open(model_path, 'rb') as fin:
            model_data = pickle.load(fin)

        self._log_probs_mat = model_data['matrix']
        self._prob_threshold = model_data['threshold']

    def train(self, data_path, bad_phrases_file_path, good_phrases_file_path):
        self._log_probs_mat = self._calculate_log_probs_mat(data_path)
        self._prob_threshold = self._calculate_prob_threshold(self._log_probs_mat, bad_phrases_file_path,
                                                              good_phrases_file_path)

    @staticmethod
    def _calculate_log_probs_mat(data_path):
        """
        Calculates log-probabilities of transitions between characters.

        :return:
        """
        num_chars = len(ACCEPTED_CHARS)
        # Assume we have seen 10 of each character pair.  This acts as a kind of
        # prior or smoothing factor.  This way, if we see a character transition
        # live that we've never observed in the past, we won't assume the entire
        # string has 0 probability.
        counts = np.full((num_chars, num_chars), 10, dtype=np.uint32)

        # Count transitions from big text file, taken from http://norvig.com/spell-correct.html
        _logger.info('Calculating transition counts...')
        for line in _read_normalized_lines(data_path):
            for char1, char2 in ngrams(line, 2):
                counts[CHAR_TO_IDX[char1]][CHAR_TO_IDX[char2]] += 1
        _logger.info('Finished calculating transition counts.')

        # Normalize the counts so that they become log probabilities.
        # We use log probabilities rather than straight probabilities to avoid
        # numeric underflow issues with long texts.
        # This contains a justification:
        # http://squarecog.wordpress.com/2009/01/10/dealing-with-underflow-in-joint-probability-calculations/
        log_probs_mat = np.log(counts / counts.sum(axis=1)[:, np.newaxis])

        return log_probs_mat

    @staticmethod
    def _calculate_prob_threshold(log_probs_mat, bad_phrases_file_path, good_phrases_file_path):
        """
        Calculates probability threshold for discern between bad and good phrases.

        :param log_probs_mat: 2D np.array corresponding to log-probabilities of transitions between characters
        :param bad_phrases_file_path: path to file with example of bad phrases
        :param good_phrases_file_path: path to file with example of good phrases
        :return:
        """
        _logger.info('Calculating probability threshold.')

        # Find the probability of generating a few arbitrarily chosen good and bad phrases.
        bad_probs = [_avg_transition_prob(line, log_probs_mat) for line in
                     _read_normalized_lines(bad_phrases_file_path)]
        good_probs = [_avg_transition_prob(line, log_probs_mat) for line in
                      _read_normalized_lines(good_phrases_file_path)]

        # Assert that we actually are capable of detecting the junk.
        if min(good_probs) < max(bad_probs):
            error_msg = 'Failed to discern between good and bad phrases.'
            _logger.error(error_msg)
            raise ValueError(error_msg)

        # And pick a threshold halfway between the worst good and best bad inputs.
        prob_threshold = (min(good_probs) + max(bad_probs)) / 2

        return prob_threshold
