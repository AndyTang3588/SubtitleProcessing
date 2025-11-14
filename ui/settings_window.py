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
        self.w.title("设置")
        self.w.geometry("500x400")

        top = ttk.Frame(self.w)
        top.pack(fill="x", pady=10)
        ttk.Button(top, text="保存", bootstyle=PRIMARY, command=self.save).pack(side="right")

        sf = TB_ScrolledFrame(self.w, autohide=True)
        sf.pack(fill="both", expand=True, padx=10, pady=10)

        self.api_chatgpt = tk.StringVar(value=getattr(launcher, "chatgpt_api_key", ""))
        self.api_groq = tk.StringVar(value=getattr(launcher, "groq_api_key", ""))

        ttk.Label(sf, text="ChatGPT API:").pack(anchor="w", pady=5)
        ttk.Entry(sf, textvariable=self.api_chatgpt).pack(fill="x")

        ttk.Label(sf, text="Groq Platform API:").pack(anchor="w", pady=5)
        ttk.Entry(sf, textvariable=self.api_groq).pack(fill="x")

    def save(self):
        self.launcher.chatgpt_api_key = self.api_chatgpt.get()
        self.launcher.groq_api_key = self.api_groq.get()
        json.dump({"chatgpt_api_key": self.api_chatgpt.get(),
                   "groq_api_key": self.api_groq.get()},
                  open(self.launcher.user_setting_file, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)
        messagebox.showinfo("成功", "设置已保存")

