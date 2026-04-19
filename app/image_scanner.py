import os
import time
from typing import List, Dict

# 支持的图片文件扩展名
SUPPORTED_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.webp']

# 缓存结构: {directory_path: {'files': [...], 'timestamp': ...}}
_cache = {}
# 缓存过期时间 (秒)
CACHE_EXPIRY = 3600

def is_image_file(filename: str) -> bool:
    """检查文件是否为图片文件"""
    ext = os.path.splitext(filename)[1].lower()
    return ext in SUPPORTED_EXTENSIONS

def scan_directory(directory: str) -> List[str]:
    """扫描目录，返回图片文件列表"""
    image_files = []
    
    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if is_image_file(file):
                    image_files.append(os.path.join(root, file))
    except Exception as e:
        print(f"扫描目录时出错: {e}")
    
    return image_files

def get_images(directory: str) -> List[str]:
    """获取目录中的图片文件，使用缓存提高性能"""
    current_time = time.time()
    
    # 检查缓存是否存在且未过期
    if directory in _cache:
        cache_entry = _cache[directory]
        if current_time - cache_entry['timestamp'] < CACHE_EXPIRY:
            return cache_entry['files']
    
    # 缓存不存在或已过期，重新扫描
    image_files = scan_directory(directory)
    
    # 更新缓存
    _cache[directory] = {
        'files': image_files,
        'timestamp': current_time
    }
    
    return image_files

def clear_cache() -> None:
    """清除缓存"""
    global _cache
    _cache = {}

def get_cache_info() -> Dict:
    """获取缓存信息"""
    current_time = time.time()
    cache_info = {}
    
    for directory, entry in _cache.items():
        cache_info[directory] = {
            'file_count': len(entry['files']),
            'cached_at': entry['timestamp'],
            'age_seconds': current_time - entry['timestamp']
        }
    
    return cache_info