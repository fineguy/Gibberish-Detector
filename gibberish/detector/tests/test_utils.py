from ..utils import delete_duplicate_characters, delete_punctuation, expand_contractions, \
    filter_non_alphabetic_characters, get_words_iter, is_not_abbreviation, is_not_interjection, is_not_person_name, \
    is_non_english_word


def test_delete_duplicate_characters():
    empty_str = ''
    text1 = 'aaaaaa'
    text2 = 'aabbaa'

    assert delete_duplicate_characters(empty_str) == ''
    assert delete_duplicate_characters(text1) == 'a'
    assert delete_duplicate_characters(text2) == 'aba'


def test_delete_punctuation():
    empty_str = ''
    text1 = ','
    text2 = 'a!b'

    assert delete_punctuation(empty_str) == ''
    assert delete_punctuation(text1) == ' '
    assert delete_punctuation(text2) == 'a b'


def test_expand_contractions():
    empty_str = ''
    text1 = 'i\'ll do'
    text2 = 'no'
    text3 = 'We’ve seen'

    assert expand_contractions(empty_str) == ''
    assert expand_contractions(text1) == 'i will do'
    assert expand_contractions(text2) == 'no'
    assert expand_contractions(text3) == 'We have seen'


def test_filter_non_alphabetic_characters():
    empty_str = ''
    text1 = '123'
    text2 = 'Abcd'

    assert filter_non_alphabetic_characters(empty_str) == ''
    assert filter_non_alphabetic_characters(text1) == ''
    assert filter_non_alphabetic_characters(text2) == 'Abcd'


def test_get_words_iter():
    empty_str = ''
    text1 = '  \t '
    text2 = ' a b c'

    assert list(get_words_iter(empty_str)) == []
    assert list(get_words_iter(text1)) == []
    assert list(get_words_iter(text2)) == ['a', 'b', 'c']


def test_is_not_abbreviation():
    empty_str = ''
    text1 = 'lol'
    text2 = 'maybe'
    text3 = 'abcd'
    text4 = 'plzzzz'

    assert is_not_abbreviation(empty_str)
    assert not is_not_abbreviation(text1)
    assert is_not_abbreviation(text2)
    assert is_not_abbreviation(text3)
    assert not is_not_abbreviation(text4)


def test_is_not_interjection():
    empty_str = ''
    text1 = 'hiiii'
    text2 = 'maybe'
    text3 = 'abcd'
    text4 = 'oof'

    assert is_not_interjection(empty_str)
    assert not is_not_interjection(text1)
    assert is_not_interjection(text2)
    assert is_not_interjection(text3)
    assert not is_not_interjection(text4)


def test_is_not_person_name():
    empty_str = ''
    text1 = 'Tom'
    text2 = 'maybe'
    text3 = 'mary'

    assert is_not_person_name(empty_str)
    assert not is_not_person_name(text1)
    assert is_not_person_name(text2)
    assert not is_not_person_name(text3)


def test_is_non_english_word():
    text1 = 'abcd'
    text2 = 'maybe'
    text3 = 'возможно'
    text4 = 'hola'

    assert is_non_english_word(text1)
    assert not is_non_english_word(text2)
    assert is_non_english_word(text3)
    assert is_non_english_word(text4)
