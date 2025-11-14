#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ttkbootstrap as ttk

# Labelframe 兼容
if hasattr(ttk, "Labelframe"):
    TB_LabelFrame = ttk.Labelframe
elif hasattr(ttk, "LabelFrame"):  # 老版本
    TB_LabelFrame = ttk.LabelFrame
else:
    raise ImportError("未找到适配的 LabelFrame/Labelframe 类")

# ScrolledFrame 兼容
try:
    from ttkbootstrap.widgets.scrolled import ScrolledFrame as TB_ScrolledFrame
except ImportError:
    try:
        from ttkbootstrap.scrolled import ScrolledFrame as TB_ScrolledFrame
    except ImportError:
        # 最旧版本没有 ScrolledFrame → 直接提示
        raise ImportError("您的 ttkbootstrap 版本不支持 ScrolledFrame，请升级：pip install -U ttkbootstrap")

