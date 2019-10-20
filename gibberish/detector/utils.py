import itertools
import re
import string

import ahocorasick
import enchant
from names_dataset import NameDataset
from nltk.corpus import words as nltk_words

from gibberish.config import ALLOWED_INTERJECTIONS_FILE_PATH, ALLOWED_WORDS_FILE_PATH, CONTRACTIONS_FILE_PATH

# English dictionaries
_ENCHANT_DICT = enchant.Dict("en_US")
_NLTK_DICT = set(word.lower() for word in nltk_words.words())

# People names dictionaries
_NAMES_DATASET = NameDataset()

_PUNCTUATION_TRANSLATION_TABLE = str.maketrans({ch: ' ' for ch in string.punctuation})

# TODO: refactor to lazy resource loading
_CONTRACTION_TO_FULL_FORM = {}
with open(CONTRACTIONS_FILE_PATH, encoding='utf8') as fin:
    for line in fin:
        contraction, full_form = line.strip().split('\t')
        _CONTRACTION_TO_FULL_FORM[contraction.lower()] = full_form.lower()
_CONTRACTIONS_PATTERN = re.compile('({})'.format('|'.join(_CONTRACTION_TO_FULL_FORM.keys())))

_ALLOWED_INTERJECTIONS_SET = set()
with open(ALLOWED_INTERJECTIONS_FILE_PATH, encoding='utf8') as fin:
    for line in fin:
        _ALLOWED_INTERJECTIONS_SET.add(frozenset(line.strip()))

_ALLOWED_WORDS_SET = set()
with open(ALLOWED_WORDS_FILE_PATH, encoding='utf8') as fin:
    for line in fin:
        _ALLOWED_WORDS_SET.add(line.strip())


def _create_english_words_trie(min_word_len):
    """
    Creates a trie containing English words with at least `min_word_len` letters.
    Refer to https://en.wikipedia.org/wiki/Aho-Corasick_algorithm

    :param min_word_len:
    :return:
    """
    automaton = ahocorasick.Automaton()

    for word in _NLTK_DICT:
        if len(word) >= min_word_len:
            automaton.add_word(word.lower(), '')

    automaton.make_automaton()

    return automaton


def delete_duplicate_characters(word):
    return ''.join(ch for ch, _ in itertools.groupby(word))


def delete_punctuation(text):
    """
    Substitutes all punctuation marks with empty spaces.

    :param text:
    :return:
    """
    return text.translate(_PUNCTUATION_TRANSLATION_TABLE)


def expand_contractions(text):
    """
    Source: https://gist.github.com/nealrs/96342d8231b75cf4bb82

    :param text:
    :return:
    """
    def replace(match):
        return _CONTRACTION_TO_FULL_FORM[match.group(0)]

    return _CONTRACTIONS_PATTERN.sub(replace, text)


def filter_non_alphabetic_characters(text):
    return ''.join(ch for ch in text.lower() if ch == ' ' or ch in string.ascii_lowercase)


def get_words_iter(text):
    return filter(None, text.split(' '))


def is_not_allowed_word(word):
    if word in _ALLOWED_WORDS_SET or delete_duplicate_characters(word) in _ALLOWED_WORDS_SET:
        return False

    unique_letters = sorted(set(word))
    if unique_letters in _ALLOWED_INTERJECTIONS_SET:
        return False

    return True


def is_not_person_name(word):
    if _NAMES_DATASET.search_first_name(word) or _NAMES_DATASET.search_last_name(word):
        return False
    return True


def is_non_english_word(word):
    """
    Checks if the given word is present in English dictionaries or has an English word as a substring.

    :param word:
    :return:
    """
    # Create trie with English words
    if not hasattr(is_non_english_word, 'trie'):
        is_non_english_word.trie = _create_english_words_trie(4)

    normalized_word = delete_duplicate_characters(word)

    for w in [word, normalized_word]:
        if _ENCHANT_DICT.check(w) or _ENCHANT_DICT.check(w.capitalize()) or w in _NLTK_DICT:
            return False
        else:
            for _, _ in is_non_english_word.trie.iter(w):
                return False

    return True


def is_non_english_text(words, max_non_english_words_ratio=0.5):
    """
    Checks if the given text has more than `max_non_english_words_ratio` percentage of English words.

    :param words:
    :param max_non_english_words_ratio:
    :return:
    """
    non_english_words_num = sum(is_non_english_word(word) for word in words)

    if len(words) == 0 or non_english_words_num / len(words) > max_non_english_words_ratio:
        return True

    return False
