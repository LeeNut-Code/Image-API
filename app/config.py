import json
import os

def load_config():
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        'port': 5000,
        'directories': [
            {
                'path': 'landscape',
                'directory': 'D:\\Administrator\\图片\\横屏壁纸'
            },
            {
                'path': 'portrait',
                'directory': 'D:\\Administrator\\图片\\竖屏壁纸'
            }
        ]
    }

config = load_config()