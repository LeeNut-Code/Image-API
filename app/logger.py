import os
import json
from datetime import datetime, timedelta

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
LOG_EXPIRY_DAYS = 3

def _ensure_log_dir():
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

def _get_log_filename():
    return datetime.now().strftime('%Y-%m-%d') + '.log'

def _get_log_filepath():
    return os.path.join(LOG_DIR, _get_log_filename())

def _cleanup_old_logs():
    """删除3天前的日志文件"""
    if not os.path.exists(LOG_DIR):
        return

    cutoff_date = datetime.now() - timedelta(days=LOG_EXPIRY_DAYS)

    for filename in os.listdir(LOG_DIR):
        if filename.endswith('.log'):
            filepath = os.path.join(LOG_DIR, filename)
            try:
                file_date_str = filename.replace('.log', '')
                file_date = datetime.strptime(file_date_str, '%Y-%m-%d')
                if file_date < cutoff_date:
                    os.remove(filepath)
            except (ValueError, OSError):
                pass

def log_request(request_url: str, local_path: str, log_enabled: bool = True):
    """记录请求日志"""
    if not log_enabled:
        return

    _ensure_log_dir()
    _cleanup_old_logs()

    log_entry = {
        'time': datetime.now().isoformat(),
        'request_url': request_url,
        'local_path': local_path
    }

    log_filepath = _get_log_filepath()
    with open(log_filepath, 'a', encoding='utf-8') as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')