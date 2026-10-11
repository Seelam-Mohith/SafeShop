import os


class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'shopsafe-dev-key')
    LOG_FILE = os.path.join('logs', 'legitimate_access.jsonl')
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
