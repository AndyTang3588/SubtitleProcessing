#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
import json
from ui.tb_compat import TB_ScrolledFrame


class SettingsWindow:
    def __init__(self, parent, launcher):
        self.launcher = launcher
        self.w = ttk.Toplevel(parent)
        self.w.title(self.launcher.lang_vars["SETTINGS_TITLE"].get())
        self.w.geometry("500x400")
        
        # 监听语言变化，更新窗口标题
        self.launcher.lang_vars["SETTINGS_TITLE"].trace_add("write", self._update_title)

        top = ttk.Frame(self.w)
        top.pack(fill="x", pady=5)
        self.save_btn = ttk.Button(top, textvariable=self.launcher.lang_vars["SETTINGS_SAVE"], bootstyle=PRIMARY, command=self.save)
        self.save_btn.pack(side="right", padx=5, pady=5)

        sf = TB_ScrolledFrame(self.w, autohide=True)
        sf.pack(fill="both", expand=True, padx=5, pady=5)

        self.api_chatgpt = tk.StringVar(value=getattr(launcher, "chatgpt_api_key", ""))
        self.api_groq = tk.StringVar(value=getattr(launcher, "groq_api_key", ""))

        self.label_chatgpt = ttk.Label(sf, textvariable=self.launcher.lang_vars["SETTINGS_CHATGPT_API"])
        self.label_chatgpt.pack(anchor="w", pady=3)
        ttk.Entry(sf, textvariable=self.api_chatgpt).pack(fill="x")

        self.label_groq = ttk.Label(sf, textvariable=self.launcher.lang_vars["SETTINGS_GROQ_API"])
        self.label_groq.pack(anchor="w", pady=3)
        ttk.Entry(sf, textvariable=self.api_groq).pack(fill="x")

    def _update_title(self, *args):
        self.w.title(self.launcher.lang_vars["SETTINGS_TITLE"].get())

    def save(self):
        self.launcher.chatgpt_api_key = self.api_chatgpt.get()
        self.launcher.groq_api_key = self.api_groq.get()
        json.dump({"chatgpt_api_key": self.api_chatgpt.get(),
                   "groq_api_key": self.api_groq.get()},
                  open(self.launcher.user_setting_file, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)
        messagebox.showinfo(
            self.launcher.lang_vars["MSG_SUCCESS"].get(),
            self.launcher.lang_vars["MSG_SETTINGS_SAVED"].get()
        )

