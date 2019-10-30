from ..model import HeuristicsGibberishDetector


def test_model():
    empty_str = ''
    text1 = 'abcdabcdabcdabcdabcd'
    text2 = 'Definitely not gibberish!'
    text3 = 'lol, ty; ttyl'

    detector = HeuristicsGibberishDetector(min_text_length=10)

    assert not detector.is_gibberish(empty_str)
    assert detector.is_gibberish(text1)
    assert not detector.is_gibberish(text2)
    assert not detector.is_gibberish(text3)
