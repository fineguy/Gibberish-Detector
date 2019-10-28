import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, 'data')

MODEL_FILE_PATH = os.path.join(DATA_DIR, 'model.pkl')
ALLOWED_INTERJECTIONS_FILE_PATH = os.path.join(DATA_DIR, 'allowed_interjections.txt')
ALLOWED_WORDS_FILE_PATH = os.path.join(DATA_DIR, 'allowed_words.txt')
CONTRACTIONS_FILE_PATH = os.path.join(DATA_DIR, 'contractions.tsv')
