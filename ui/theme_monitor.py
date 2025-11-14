#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess


class ThemeMonitor:
    def __init__(self, root, style):
        self.root = root
        self.style = style
        self.current_mode = None
        self.check_theme()

    def get_system_mode(self):
        try:
            result = subprocess.run(
                ["defaults", "read", "-g", "AppleInterfaceStyle"],
                capture_output=True, text=True
            )
            return "dark" if "Dark" in result.stdout else "light"
        except:
            return "light"

    def apply_theme(self, mode):
        theme = "darkly" if mode == "dark" else "flatly"
        self.style.theme_use(theme)

    def check_theme(self):
        mode = self.get_system_mode()
        if mode != self.current_mode:
            self.current_mode = mode
            self.apply_theme(mode)
        self.root.after(2000, self.check_theme)  # 每 2s 检测一次

