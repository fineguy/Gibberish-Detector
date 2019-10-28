import re
import string


ACCEPTED_CHARS = string.ascii_lowercase + ' '
CHAR_TO_IDX = {char: idx for idx, char in enumerate(ACCEPTED_CHARS)}
ALLOWED_LINE_PATTERN = re.compile('[^{}]'.format(ACCEPTED_CHARS))
