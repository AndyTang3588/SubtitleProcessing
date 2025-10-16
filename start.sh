#!/bin/bash
# 字幕处理工具集启动脚本

echo "启动字幕处理工具集 Launcher..."
echo "请确保已安装Python3和tkinter"

# 检查Python3是否安装
if ! command -v /usr/local/bin/python3 &> /dev/null; then
    echo "错误：未找到Python3，请先安装Python3"
    exit 1
fi

# 检查tkinter是否可用
/usr/local/bin/python3 -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "错误：tkinter未安装，请安装tkinter模块"
    exit 1
fi

# 启动launcher
/usr/local/bin/python3 launcher.py