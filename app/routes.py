import os
import random
from flask import send_file, abort, request
from app import app
from app.image_scanner import get_images, clear_cache, get_cache_info
from app.config import config
from app.logger import log_request

@app.route('/')
def index():
    return '欢迎使用本地随机图片API'

@app.route('/scan')
def scan_images():
    """扫描所有配置的目录并返回图片文件列表"""
    results = {}
    
    for dir_config in config.get('directories', []):
        directory = dir_config['directory']
        images = get_images(directory)
        results[dir_config['path']] = {
            'directory': directory,
            'image_count': len(images),
            'images': images
        }
    
    return results

@app.route('/cache/clear')
def clear_image_cache():
    """清除图片缓存"""
    clear_cache()
    return {'message': '缓存已清除'}

@app.route('/cache/info')
def get_cache_status():
    """获取缓存信息"""
    return get_cache_info()

@app.route('/shutdown')
def shutdown():
    """关闭服务"""
    import threading
    threading.Thread(target=lambda: os._exit(0), daemon=True).start()
    return {'message': '服务正在关闭'}

@app.route('/<path:requested_path>')
def get_random_image(requested_path):
    """根据URL路径获取对应目录的随机图片"""
    for dir_config in config.get('directories', []):
        if dir_config['path'] == requested_path:
            directory = dir_config['directory']
            images = get_images(directory)

            if not images:
                abort(404, description='该目录下没有图片文件')

            random_image = random.choice(images)
            log_request(request.url, random_image, config.get('log_enabled', True))
            return send_file(random_image)

    abort(404, description='未找到对应的图片目录')