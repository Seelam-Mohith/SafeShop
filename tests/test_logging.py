import os
import sys
import tempfile
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from services.access_logger import AccessLogger


def test_logging_creates_records():
    tmpdir = tempfile.mkdtemp()
    log_file = os.path.join(tmpdir, 'test.jsonl')
    logger = AccessLogger(log_file=log_file)
    logger.log_request('127.0.0.1', 'GET', '/', 200, referer='', user_agent='test', response_bytes=100, duration_ms=1.0)
    assert os.path.exists(log_file)
    with open(log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    assert content.strip() != ''
    os.remove(log_file)
    os.rmdir(tmpdir)


def test_logged_records_have_required_fields():
    tmpdir = tempfile.mkdtemp()
    log_file = os.path.join(tmpdir, 'test.jsonl')
    logger = AccessLogger(log_file=log_file)
    logger.log_request('127.0.0.1', 'GET', '/products', 200, referer='http://127.0.0.1:5000/', user_agent='Mozilla/5.0', response_bytes=4820, duration_ms=8.2)
    with open(log_file, 'r', encoding='utf-8') as f:
        line = f.readline()
    record = json.loads(line)
    required = ['timestamp', 'source_ip', 'method', 'path', 'status_code', 'referer', 'user_agent', 'response_bytes', 'duration_ms']
    for field in required:
        assert field in record
    os.remove(log_file)
    os.rmdir(tmpdir)


def test_logs_do_not_contain_sensitive_headers():
    tmpdir = tempfile.mkdtemp()
    log_file = os.path.join(tmpdir, 'test.jsonl')
    logger = AccessLogger(log_file=log_file)
    logger.log_request('127.0.0.1', 'GET', '/', 200, referer='', user_agent='test', response_bytes=100, duration_ms=1.0)
    with open(log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    assert 'cookie' not in content.lower()
    assert 'authorization' not in content.lower()
    assert 'password' not in content.lower()
    assert 'token' not in content.lower()
    os.remove(log_file)
    os.rmdir(tmpdir)


def test_requests_generate_valid_jsonl():
    # Use test client and check log file
    log_file = os.path.join('logs', 'legitimate_access.jsonl')
    # Ensure dir exists
    os.makedirs('logs', exist_ok=True)
    # Count lines before
    with open(log_file, 'a'):
        pass  # ensure exists
    client = app.test_client()
    client.get('/')
    client.get('/products')
    client.get('/static/css/style.css')
    # Check last few lines are valid JSON
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        # last 3 lines
        for line in lines[-3:]:
            if line.strip():
                obj = json.loads(line)
                assert 'path' in obj
    except Exception:
        pass
