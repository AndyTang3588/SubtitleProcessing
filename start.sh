#!/bin/bash
# 字幕处理工具集启动脚本（自动创建目录 + 自动装依赖）

echo "启动 字幕处理工具集 Launcher..."
echo "检查环境..."

# Python 路径优先使用 /usr/local/bin/python3，不存在则用 python3
PYTHON_BIN="/usr/local/bin/python3"
if ! command -v $PYTHON_BIN &> /dev/null; then
    PYTHON_BIN="python3"
fi

if ! command -v $PYTHON_BIN &> /dev/null; then
    echo "错误：未找到 Python3，请先安装 Python3"
    exit 1
fi

# 检查 pip
echo "- 检查 pip..."
$PYTHON_BIN -m pip --version &> /dev/null
if [ $? -ne 0 ]; then
    echo "错误：pip 未安装，请先安装 pip"
    exit 1
fi

# 检查 tkinter
echo "- 检查 tkinter..."
$PYTHON_BIN -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "错误：tkinter 未安装，请先安装 tkinter 模块"
    exit 1
fi

# 检查 ttkbootstrap
echo "- 检查 ttkbootstrap..."
$PYTHON_BIN -c "import ttkbootstrap" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "未找到 ttkbootstrap，正在自动安装..."
    $PYTHON_BIN -m pip install ttkbootstrap
    if [ $? -ne 0 ]; then
        echo "错误：ttkbootstrap 安装失败，请检查网络或权限"
        exit 1
    fi
fi
echo "依赖检查完毕 ✔"

# 自动创建必要目录
echo "- 检查并创建项目目录..."
mkdir -p cache
mkdir -p output
echo "项目目录检查完毕 ✔"

# 运行 launcher.py
echo "启动 GUI 程序..."
$PYTHON_BIN launcher.py
