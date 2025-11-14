#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ttkbootstrap as ttk
from ui.main_window import SubtitleLauncher
from ui.theme_monitor import ThemeMonitor


def main():
    root = ttk.Window()
    style = ttk.Style()
    
    SubtitleLauncher(root)
    ThemeMonitor(root, style)  # 启动监听
    
    root.mainloop()


if __name__ == "__main__":
    main()
