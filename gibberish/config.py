import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, 'data')

MODEL_FILE_PATH = os.path.join(DATA_DIR, 'model.pkl')
ALLOWED_INTERJECTIONS_FILE_PATH = os.path.join(DATA_DIR, 'allowed_interjections.txt')
ALLOWED_ABBREVIATIONS_FILE_PATH = os.path.join(DATA_DIR, 'allowed_abbreviations.txt')
CONTRACTIONS_FILE_PATH = os.path.join(DATA_DIR, 'contractions.tsv')
