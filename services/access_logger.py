import json
import os
import time
from datetime import datetime
from threading import Lock

_log_lock = Lock()


class AccessLogger:
    def __init__(self, log_file=None):
        self.log_file = log_file or os.path.join('logs', 'legitimate_access.jsonl')
        self._ensure_log_dir()

    def _ensure_log_dir(self):
        log_dir = os.path.dirname(self.log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

    def log_request(self, source_ip, method, path, status_code, referer=None,
                    user_agent=None, response_bytes=None, duration_ms=None):
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        record = {
            'timestamp': timestamp,
            'source_ip': source_ip,
            'method': method,
            'path': path,
            'status_code': status_code,
            'referer': referer or '',
            'user_agent': user_agent or '',
            'response_bytes': response_bytes if response_bytes is not None else 0,
            'duration_ms': duration_ms if duration_ms is not None else 0.0
        }
        with _log_lock:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(record) + '\n')


def get_source_ip(request):
    # Do not trust arbitrary client-supplied forwarding headers
    return request.remote_addr or '127.0.0.1'
