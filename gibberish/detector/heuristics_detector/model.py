from gibberish.detector.abstract_model import AbstractGibberishDetector
from gibberish.detector.utils import expand_contractions, delete_punctuation, filter_non_alphabetic_characters, \
    get_words_iter, is_not_abbreviation, is_not_interjection, is_not_person_name, is_non_english_text

from .config import MIN_TEXT_LENGTH


class HeuristicsGibberishDetector(AbstractGibberishDetector):
    def __init__(self, min_text_length=MIN_TEXT_LENGTH):
        self._min_text_length = min_text_length

    def is_gibberish(self, text):
        text = text.strip()

        # Ignore text that includes links to files because they're hard to match
        if len(text) < self._min_text_length or 'http' in text or 'data:image/jpeg' in text:
            return False

        text = expand_contractions(text)

        text = delete_punctuation(text)

        text = filter_non_alphabetic_characters(text)

        words_iter = get_words_iter(text)
        words_iter = filter(is_not_abbreviation, words_iter)
        words_iter = filter(is_not_interjection, words_iter)
        words = list(filter(is_not_person_name, words_iter))

        if len(words) == 0:
            return False

        if is_non_english_text(words):
            return True

        return False
