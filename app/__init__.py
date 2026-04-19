from flask import Flask

app = Flask(__name__)

from app import routes

from app.logger import _cleanup_old_logs
_cleanup_old_logs()