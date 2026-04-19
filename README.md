# Image API

一个简单的随机图片API服务，用于提供随机图片。

## 功能
- 提供随机图片访问
- 支持不同尺寸的图片
- 轻量级设计

## 快速开始

### 环境要求
- Python 3.7+
- Flask

### 安装
1. 克隆仓库
2. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```

### 运行
- 双击 `start.bat` 启动服务
- 或运行 `python run.pyw`

### 访问
默认访问地址: `http://localhost:5845`

## 配置
修改 `config.json` 文件进行配置。

## 停止服务
- 双击 `stop.bat` 停止服务

## 项目结构
```
image-api/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── image_scanner.py
│   └── routes.py
├── config.json
├── run.pyw
├── start.bat
├── stop.bat
└── README.md
```