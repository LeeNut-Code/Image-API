import os
import sys
import socket
import atexit

from app import app
from app.config import config

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def get_lock_file_path():
    app_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(app_dir, 'service.lock')

def is_already_running():
    lock_file = get_lock_file_path()
    if os.path.exists(lock_file):
        with open(lock_file, 'r') as f:
            pid = int(f.read().strip())
        try:
            os.kill(pid, 0)
            return pid
        except OSError:
            os.remove(lock_file)
            return None
    return None

def write_pid():
    lock_file = get_lock_file_path()
    with open(lock_file, 'w') as f:
        f.write(str(os.getpid()))

def cleanup():
    lock_file = get_lock_file_path()
    if os.path.exists(lock_file):
        os.remove(lock_file)

atexit.register(cleanup)

def stop_service():
    """停止正在运行的服务"""
    port = config.get('port', 5845)
    
    if not is_port_in_use(port):
        print('服务未运行')
        sys.exit(0)
    
    import urllib.request
    try:
        response = urllib.request.urlopen(f'http://127.0.0.1:{port}/shutdown', timeout=5)
        print('服务正在关闭...')
    except Exception as e:
        print(f'关闭服务时出错: {e}')
        sys.exit(1)

if __name__ == '__main__':
    # 检查命令行参数
    if len(sys.argv) > 1:
        if sys.argv[1] == '--stop':
            stop_service()
            sys.exit(0)
    
    port = config.get('port', 5845)
    
    if is_port_in_use(port):
        print(f'Error: Service is already running on port {port}')
        sys.exit(1)
    
    existing_pid = is_already_running()
    if existing_pid:
        print(f'Error: Service is already running (PID: {existing_pid})')
        sys.exit(1)
    
    write_pid()
    
    app.run(debug=False, host='127.0.0.1', port=port, threaded=True, use_reloader=False)