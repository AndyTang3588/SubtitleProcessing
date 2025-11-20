#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import filedialog, messagebox
import threading, json
import shutil
import subprocess
import sys
import os
from pathlib import Path
from ui.tb_compat import TB_LabelFrame, TB_ScrolledFrame
from ui.settings_window import SettingsWindow
from ui.locales import LANG_DATA


class SubtitleLauncher:
    def __init__(self, root):
        self.root = root
        
        # 初始化语言相关变量
        self.current_lang = 'en'  # 默认语言
        self.lang_vars = {}  # 存放所有的 StringVar
        self._init_lang_vars()  # 初始化变量函数

        # 使用变量设置标题
        self.root.title(self.lang_vars["WINDOW_TITLE"].get())
        self.root.geometry("1200x700")
        self.root.minsize(600, 400)

        # 变量
        self.selected_file = tk.StringVar()
        self.delay_value = tk.StringVar(value="0")
        self.step01_version = tk.StringVar(value="1json2midform.py (最新)")
        self.step02_version = tk.StringVar(value="2去重midform.py (最新)")
        self.step04_version = tk.StringVar(value="midform2srt.py (最新)")
        self.step01_status = tk.StringVar(value=LANG_DATA['en']['STATUS_WAIT'])
        self.step02_status = tk.StringVar(value=LANG_DATA['en']['STATUS_WAIT'])
        self.step03_status = tk.StringVar(value=LANG_DATA['en']['STATUS_WAIT'])
        self.step04_status = tk.StringVar(value=LANG_DATA['en']['STATUS_WAIT'])
        self.output_to_original = tk.BooleanVar(value=False)
        self.stepA1_message = tk.StringVar(value=LANG_DATA['en']['MSG_SELECT_FILE'])
        self.stepA1_run_btn = None

        self.settings_window = None
        self.user_setting_file = Path("userSetting.json")
        self.load_user_setting()

        self.setup_ui()
        
        # 添加语言切换监听（当标题变量变化时，更新窗口标题）
        self.lang_vars["WINDOW_TITLE"].trace_add("write", self._update_window_title)

    # 初始化所有语言变量
    def _init_lang_vars(self):
        # 遍历英文键值对，创建 StringVar
        for key, value in LANG_DATA['en'].items():
            self.lang_vars[key] = tk.StringVar(value=value)

    # 窗口标题更新回调
    def _update_window_title(self, *args):
        self.root.title(self.lang_vars["WINDOW_TITLE"].get())

    # 核心切换逻辑
    def switch_language(self, event=None):
        selected = self.lang_combo.get()
        new_lang = 'zh' if selected == "中文" else 'en'
        
        if new_lang == self.current_lang:
            return
            
        self.current_lang = new_lang
        target_dict = LANG_DATA[self.current_lang]
        
        # 批量更新所有 StringVar
        for key, value in target_dict.items():
            if key in self.lang_vars:
                self.lang_vars[key].set(value)
        
        # 更新 stepA1 的消息文本
        self.update_stepA1_ui()

    # ========== UI ==========
    def setup_ui(self):
        # 上
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill="x", padx=5, pady=5)

        left_frame = ttk.Frame(top_frame)
        left_frame.pack(side="left")
        ttk.Label(left_frame, textvariable=self.lang_vars["SELECT_FILE"]).pack(side="left")
        ttk.Button(left_frame, textvariable=self.lang_vars["BTN_BROWSE"], command=self.select_file).pack(side="left", padx=5)
        ttk.Label(left_frame, textvariable=self.selected_file, bootstyle=INFO).pack(side="left", padx=5)
        
        # 右侧区域：设置 + 语言切换
        # 1. 最右边：设置按钮
        ttk.Button(top_frame, textvariable=self.lang_vars["BTN_SETTINGS"], bootstyle=SECONDARY, command=self.open_settings).pack(side="right")
        
        # 2. 设置按钮左边：语言下拉框
        self.lang_combo = ttk.Combobox(top_frame, values=["中文", "English"], state="readonly", width=8)
        self.lang_combo.current(1)  # 默认英文
        self.lang_combo.pack(side="right", padx=5)
        self.lang_combo.bind("<<ComboboxSelected>>", self.switch_language)

        # 中 - 横向滚动
        middle_frame = ttk.Frame(self.root)
        middle_frame.pack(fill="both", expand=True, padx=5, pady=5)
        middle_frame.columnconfigure(0, weight=1)
        middle_frame.rowconfigure(0, weight=1)

        self.steps_sf = TB_ScrolledFrame(
            middle_frame,
            autohide=True,
            bootstyle=ROUND
        )
        self.steps_sf.grid(row=0, column=0, sticky="nsew")

        # 获取 ScrolledFrame 的内部容器（用于放置内容）
        steps_container = self.steps_sf.container
        steps_container.columnconfigure((0,1,2), weight=1, uniform="steps")
        steps_container.rowconfigure((1,3,5), weight=1)  # 卡片行可扩展

        self.create_step_frames(steps_container)

        # 下
        bottom_frame = ttk.Frame(self.root)
        bottom_frame.pack(fill="x", padx=5, pady=5)

        ttk.Checkbutton(bottom_frame, textvariable=self.lang_vars["CHECK_OUTPUT"], variable=self.output_to_original).pack(side="left")
        ttk.Button(bottom_frame, textvariable=self.lang_vars["BTN_GENERATE"], bootstyle=PRIMARY, command=self.generate_results).pack(side="left", padx=10)

        self.result_status = tk.StringVar(value=LANG_DATA['en']["STATUS_WAIT_RESULT"])
        ttk.Label(bottom_frame, textvariable=self.result_status, bootstyle=INFO).pack(pady=3)

    def _create_card(self, parent, title_key, row, column, columnspan=1):
        # 注意：这里传入的是 title_key (例如 "CARD_A1") 而不是直接的文本
        
        # TB_LabelFrame/LabelFrame 的 text 属性通常不支持 textvariable
        # 解决方法：初始化时设置 text，并添加监听器手动更新
        
        current_text = self.lang_vars[title_key].get()
        card = TB_LabelFrame(parent, text=current_text, padding=5, bootstyle=INFO)
        
        # 定义更新函数
        def update_card_text(*args):
            card.configure(text=self.lang_vars[title_key].get())
        
        # 绑定监听
        self.lang_vars[title_key].trace_add("write", update_card_text)
        
        card.grid(row=row, column=column, columnspan=columnspan, padx=5, pady=5, sticky="nsew")
        return card

    def create_step_frames(self, parent):
        # ===== 第一行：输入预处理 =====
        row1_title = ttk.Label(parent, textvariable=self.lang_vars["GROUP_PREPROCESS"], bootstyle=INFO)
        row1_title.grid(row=0, column=0, columnspan=3, sticky="w", padx=5, pady=(0,3))
        
        self._build_stepA1(self._create_card(parent, "CARD_A1", 1, 0))
        self._build_stepA2(self._create_card(parent, "CARD_A2", 1, 1))
        self._build_stepA3(self._create_card(parent, "CARD_A3", 1, 2))
        
        # ===== 第二行：文字内容精细处理 =====
        row2_title = ttk.Label(parent, textvariable=self.lang_vars["GROUP_REFINE"], bootstyle=INFO)
        row2_title.grid(row=2, column=0, columnspan=3, sticky="w", padx=5, pady=(5,3))
        
        self._build_stepB1(self._create_card(parent, "CARD_B1", 3, 0, 3))
        
        # ===== 第三行：输出处理 =====
        row3_title = ttk.Label(parent, textvariable=self.lang_vars["GROUP_OUTPUT"], bootstyle=INFO)
        row3_title.grid(row=4, column=0, columnspan=3, sticky="w", padx=5, pady=(5,3))
        
        self._build_stepC1(self._create_card(parent, "CARD_C1", 5, 0))
        self._build_stepC2(self._create_card(parent, "CARD_C2", 5, 1, 2))

    # ===== Step Panels =====
    def _build_step01(self, f):
        f.grid_columnconfigure(0, weight=1)  # 内容列可伸缩
        f.grid_rowconfigure(1, weight=1)  # 中间行可扩展，让按钮下沉
        
        ttk.Label(f, textvariable=self.lang_vars["LABEL_VERSION"]).grid(row=0, column=0, sticky="w", pady=(0, 3))
        ttk.Combobox(f, textvariable=self.step01_version,
                     values=["1json2midform.py (最新)", "1json2lrc&srt.py", "1txt2lrc&srt.py"],
                     state="readonly").grid(row=1, column=0, sticky="ew", pady=(0, 5))
        ttk.Button(f, textvariable=self.lang_vars["BTN_RUN"], bootstyle=SUCCESS, command=lambda: self.run_step("01")).grid(row=2, column=0, sticky="sw", padx=5, pady=5)
        ttk.Label(f, textvariable=self.step01_status, bootstyle=INFO).grid(row=2, column=1, sticky="se", padx=5, pady=5)

    def _build_step02(self, f):
        f.grid_columnconfigure(0, weight=1)  # 内容列可伸缩
        f.grid_rowconfigure(1, weight=1)  # 中间行可扩展，让按钮下沉
        
        ttk.Label(f, textvariable=self.lang_vars["LABEL_VERSION"]).grid(row=0, column=0, sticky="w", pady=(0, 3))
        ttk.Combobox(f, textvariable=self.step02_version,
                     values=["2去重midform.py (最新)", "2去重srt.py"],
                     state="readonly").grid(row=1, column=0, sticky="ew", pady=(0, 5))
        ttk.Button(f, textvariable=self.lang_vars["BTN_RUN"], bootstyle=SUCCESS, command=lambda: self.run_step("02")).grid(row=2, column=0, sticky="sw", padx=5, pady=5)
        ttk.Label(f, textvariable=self.step02_status, bootstyle=INFO).grid(row=2, column=1, sticky="se", padx=5, pady=5)

    def _build_step03(self, f):
        f.grid_columnconfigure(0, weight=1)  # 内容列可伸缩
        f.grid_rowconfigure(1, weight=1)  # 中间行可扩展，让按钮下沉
        
        ttk.Label(f, textvariable=self.lang_vars["LABEL_DELAY"]).grid(row=0, column=0, sticky="w", pady=(0, 3))
        ttk.Entry(f, textvariable=self.delay_value).grid(row=1, column=0, sticky="ew", pady=(0, 5))
        ttk.Button(f, textvariable=self.lang_vars["BTN_RUN"], bootstyle=SUCCESS, command=lambda: self.run_step("03")).grid(row=2, column=0, sticky="sw", padx=5, pady=5)
        ttk.Label(f, textvariable=self.step03_status, bootstyle=INFO).grid(row=2, column=1, sticky="se", padx=5, pady=5)

    def _build_step04(self, f):
        f.grid_columnconfigure(0, weight=1)  # 内容列可伸缩
        f.grid_rowconfigure(1, weight=1)  # 中间行可扩展，让按钮下沉
        
        ttk.Label(f, textvariable=self.lang_vars["LABEL_VERSION"]).grid(row=0, column=0, sticky="w", pady=(0, 3))
        ttk.Combobox(f, textvariable=self.step04_version,
                     values=["midform2srt.py (最新)", "midform2lrc.py", "lrc转srt_v2.py"],
                     state="readonly").grid(row=1, column=0, sticky="ew", pady=(0, 5))
        ttk.Button(f, textvariable=self.lang_vars["BTN_RUN"], bootstyle=SUCCESS, command=lambda: self.run_step("04")).grid(row=2, column=0, sticky="sw", padx=5, pady=5)
        ttk.Label(f, textvariable=self.step04_status, bootstyle=INFO).grid(row=2, column=1, sticky="se", padx=5, pady=5)

    # ================= 新结构方法 =================
    def _build_stepA1(self, frame):
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

        ttk.Label(frame, textvariable=self.stepA1_message,
                  bootstyle=INFO).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 5))
        self.stepA1_run_btn = ttk.Button(frame, textvariable=self.lang_vars["BTN_RUN"], bootstyle=SUCCESS,
                                         command=lambda: self.run_step("01"), state=DISABLED)
        self.stepA1_run_btn.grid(row=1, column=0, sticky="sw", padx=5, pady=5)
        ttk.Label(frame, textvariable=self.step01_status,
                  bootstyle=INFO).grid(row=1, column=1, sticky="se", padx=5, pady=5)
        self.update_stepA1_ui()

    def _build_stepA2(self, frame):
        self._build_step02(frame)

    def _build_stepA3(self, frame):
        self._build_step03(frame)

    # 第二行：AI 翻译
    def _build_stepB1(self, frame):
        frame.grid_columnconfigure(0, weight=1)  # 内容列可伸缩
        frame.grid_rowconfigure(0, weight=1)  # 中间行可扩展，让按钮下沉
        
        ttk.Label(frame, textvariable=self.lang_vars["LABEL_AI_TRANSLATE"],
                  bootstyle=WARNING).grid(row=0, column=0, sticky="w", pady=(0, 5))
        ttk.Button(frame, textvariable=self.lang_vars["BTN_START_TRANSLATE"],
                   bootstyle=SECONDARY).grid(row=1, column=0, sticky="sw", padx=5, pady=5)

    # 第三行：输出
    def _build_stepC1(self, frame):
        self._build_step04(frame)

    def _build_stepC2(self, frame):
        frame.grid_columnconfigure(0, weight=1)  # 内容列可伸缩
        frame.grid_rowconfigure(0, weight=1)  # 中间行可扩展，让按钮下沉
        
        ttk.Label(frame, textvariable=self.lang_vars["LABEL_MULTILANG"],
                  bootstyle=WARNING).grid(row=0, column=0, sticky="w", pady=(0, 5))
        ttk.Button(frame, textvariable=self.lang_vars["BTN_START_PROCESS"],
                   bootstyle=SECONDARY).grid(row=1, column=0, sticky="sw", padx=5, pady=5)

    def update_stepA1_ui(self):
        """更新输入转字幕面板，按照文件类型提示是否支持。"""
        if not self.stepA1_run_btn:
            return

        file_path = self.selected_file.get()
        if not file_path:
            self.stepA1_message.set(self.lang_vars["MSG_SELECT_FILE"].get())
            self.stepA1_run_btn.configure(state=DISABLED)
            return

        if Path(file_path).suffix.lower() == ".json":
            self.stepA1_message.set(self.lang_vars["MSG_USE_JSON2MIDFORM"].get())
            self.step01_version.set("1json2midform.py (最新)")
            self.stepA1_run_btn.configure(state=NORMAL)
        else:
            self.stepA1_message.set(self.lang_vars["MSG_FORMAT_NOT_SUPPORTED"].get())
            self.stepA1_run_btn.configure(state=DISABLED)

    # ========== File Select ==========
    def select_file(self):
        f = filedialog.askopenfilename(
            title=self.lang_vars["DIALOG_SELECT_FILE"].get(),
            filetypes=[
                (self.lang_vars["DIALOG_FILE_TYPES_TEXT"].get(), "*.txt"),
                (self.lang_vars["DIALOG_FILE_TYPES_JSON"].get(), "*.json"),
                (self.lang_vars["DIALOG_FILE_TYPES_ALL"].get(), "*.*")
            ])
        if f:
            self.selected_file.set(f)
            self.clean_cache()
            self.reset_step_status()
            self.update_stepA1_ui()

    def clean_cache(self):
        try:
            d = Path("cache")
            if d.exists():
                for p in d.iterdir():
                    if p.is_file(): p.unlink()
        except: pass

    def reset_step_status(self):
        self.step01_status.set(self.lang_vars["STATUS_WAIT"].get())
        self.step02_status.set(self.lang_vars["STATUS_WAIT"].get())
        self.step03_status.set(self.lang_vars["STATUS_WAIT"].get())
        self.step04_status.set(self.lang_vars["STATUS_WAIT"].get())
        self.result_status.set(self.lang_vars["STATUS_WAIT_RESULT"].get())

    # ========== Execution ==========
    def run_step(self, n):
        if not self.selected_file.get():
            messagebox.showwarning(
                self.lang_vars["MSG_WARNING"].get(),
                self.lang_vars["MSG_PLEASE_SELECT_FILE"].get()
            )
            return
        threading.Thread(target=self._execute_step, args=(n,), daemon=True).start()

    def _execute_step(self, n):
        """执行处理步骤"""
        # 更新状态为运行中
        status_var = getattr(self, f"step{n}_status")
        self.root.after(0, lambda: status_var.set(self.lang_vars["STATUS_RUNNING"].get()))
        
        try:
            # 确保 cache 目录存在
            cache_dir = Path("cache")
            cache_dir.mkdir(exist_ok=True)
            
            # 步骤 01: 文本转字幕
            if n == "01":
                # 复制输入文件到 cache/input.json
                input_file = Path(self.selected_file.get())
                if not input_file.exists():
                    raise FileNotFoundError(f"Input file not found: {input_file}")
                
                # 根据文件扩展名决定如何处理
                if input_file.suffix.lower() == '.json':
                    shutil.copy2(input_file, cache_dir / "input.json")
                else:
                    # 对于非 JSON 文件，可能需要其他处理
                    # 这里先只支持 JSON
                    raise ValueError("Only JSON files are supported for step 01")
                
                # 获取选择的版本
                version = self.step01_version.get()
                script_name = version.split()[0]  # 例如 "1json2midform.py"
                
                # 执行脚本
                script_path = Path(f"src/A1_输入转字幕/{script_name}")
                if not script_path.exists():
                    raise FileNotFoundError(f"Script not found: {script_path}")
                
                result = subprocess.run(
                    [sys.executable, str(script_path)],
                    cwd=Path.cwd(),
                    capture_output=True,
                    text=True,
                    encoding='utf-8'
                )
                
                if result.returncode == 0:
                    self.root.after(0, lambda: status_var.set(self.lang_vars["STATUS_SUCCESS"].get()))
                else:
                    error_msg = result.stderr or result.stdout or "Unknown error"
                    self.root.after(0, lambda: status_var.set(f"Error: {error_msg[:50]}"))
            
            # 步骤 02: 去重处理
            elif n == "02":
                version = self.step02_version.get()
                script_name = version.split()[0]  # 例如 "2去重midform.py"
                
                script_path = Path(f"src/A2_去重处理/{script_name}")
                if not script_path.exists():
                    raise FileNotFoundError(f"Script not found: {script_path}")
                
                result = subprocess.run(
                    [sys.executable, str(script_path)],
                    cwd=Path.cwd(),
                    capture_output=True,
                    text=True,
                    encoding='utf-8'
                )
                
                if result.returncode == 0:
                    self.root.after(0, lambda: status_var.set(self.lang_vars["STATUS_SUCCESS"].get()))
                else:
                    error_msg = result.stderr or result.stdout or "Unknown error"
                    self.root.after(0, lambda: status_var.set(f"Error: {error_msg[:50]}"))
            
            # 步骤 03: 时间调整
            elif n == "03":
                delay_ms = int(self.delay_value.get() or "0")
                
                # 检测 cache 目录中的文件类型，按优先级选择
                cache_dir = Path("cache")
                script_name = None
                
                # 按优先级查找文件（output3 > output2 > output1）
                for priority in [2, 1]:  # 注意：脚本通常从 output2 读取
                    if (cache_dir / f"output{priority}.midform").exists():
                        script_name = "3延迟midform.py"
                        break
                    elif (cache_dir / f"output{priority}.lrc").exists():
                        script_name = "3延时lrc.py"
                        break
                    elif (cache_dir / f"output{priority}.srt").exists():
                        script_name = "3延时srt.py"
                        break
                
                if not script_name:
                    raise FileNotFoundError("No input file found in cache for time adjustment")
                
                script_path = Path(f"src/A3_时间调整/{script_name}")
                if not script_path.exists():
                    raise FileNotFoundError(f"Script not found: {script_path}")
                
                # 执行脚本，传递延迟值作为命令行参数
                result = subprocess.run(
                    [sys.executable, str(script_path), str(delay_ms)],
                    cwd=Path.cwd(),
                    capture_output=True,
                    text=True,
                    encoding='utf-8'
                )
                
                if result.returncode == 0:
                    self.root.after(0, lambda: status_var.set(self.lang_vars["STATUS_SUCCESS"].get()))
                else:
                    error_msg = result.stderr or result.stdout or "Unknown error"
                    self.root.after(0, lambda: status_var.set(f"Error: {error_msg[:50]}"))
            
            # 步骤 04: 格式转换
            elif n == "04":
                version = self.step04_version.get()
                script_name = version.split()[0]  # 例如 "midform2srt.py"
                
                script_path = Path(f"src/C1_格式转换/{script_name}")
                if not script_path.exists():
                    raise FileNotFoundError(f"Script not found: {script_path}")
                
                result = subprocess.run(
                    [sys.executable, str(script_path)],
                    cwd=Path.cwd(),
                    capture_output=True,
                    text=True,
                    encoding='utf-8'
                )
                
                if result.returncode == 0:
                    self.root.after(0, lambda: status_var.set(self.lang_vars["STATUS_SUCCESS"].get()))
                else:
                    error_msg = result.stderr or result.stdout or "Unknown error"
                    self.root.after(0, lambda: status_var.set(f"Error: {error_msg[:50]}"))
            
        except Exception as e:
            error_msg = str(e)[:100]
            self.root.after(0, lambda: status_var.set(f"Error: {error_msg}"))

    # ========== Output ==========
    def generate_results(self):
        """生成转换结果：从 cache 目录复制最新优先级的文件到输出目录"""
        cache_dir = Path("cache")
        if not cache_dir.exists():
            self.result_status.set("Error: cache directory not found")
            messagebox.showerror(
                self.lang_vars["MSG_WARNING"].get(),
                self.lang_vars["MSG_CACHE_NOT_FOUND"].get()
            )
            return
        
        # 支持的输出文件扩展名
        supported_extensions = ['.lrc', '.srt', '.midform', '.txt']
        
        # 确定输出目录
        if self.output_to_original.get():
            # 输出到原文件目录
            if self.selected_file.get():
                output_dir = Path(self.selected_file.get()).parent
            else:
                output_dir = Path("output")
                output_dir.mkdir(exist_ok=True)
        else:
            # 输出到 output 目录
            output_dir = Path("output")
            output_dir.mkdir(exist_ok=True)
        
        # 按优先级查找文件（output3 > output2 > output1）
        # 对于每个优先级，复制所有找到的文件
        copied_files = []
        found_priority = None
        
        for priority in [3, 2, 1]:
            priority_files = []
            for ext in supported_extensions:
                cache_file = cache_dir / f"output{priority}{ext}"
                if cache_file.exists() and cache_file.is_file():
                    # 生成输出文件名
                    if self.selected_file.get():
                        original_name = Path(self.selected_file.get()).stem
                        output_file = output_dir / f"{original_name}{ext}"
                    else:
                        output_file = output_dir / f"output{priority}{ext}"
                    
                    try:
                        # 复制文件
                        shutil.copy2(cache_file, output_file)
                        priority_files.append(str(output_file))
                    except Exception as e:
                        print(f"Error copying {cache_file}: {e}")
            
            # 如果找到文件，记录优先级并跳出（只处理最高优先级的文件）
            if priority_files:
                copied_files.extend(priority_files)
                found_priority = priority
                break  # 只处理最高优先级的文件
        
        if copied_files:
            count = len(copied_files)
            self.result_status.set(self.lang_vars["MSG_GENERATED_FILES"].get().format(count=count))
            # 显示成功消息（可选，如果文件太多可能太长）
            if count <= 3:
                messagebox.showinfo(
                    self.lang_vars["MSG_SUCCESS"].get(),
                    f"Successfully generated {count} file(s):\n" + "\n".join(copied_files)
                )
        else:
            self.result_status.set("No output files found in cache")
            messagebox.showwarning(
                self.lang_vars["MSG_WARNING"].get(),
                self.lang_vars["MSG_NO_OUTPUT_FILES"].get()
            )

    # ========== Settings Window ==========
    def load_user_setting(self):
        try:
            if self.user_setting_file.exists():
                u = json.loads(self.user_setting_file.read_text("utf-8"))
                self.chatgpt_api_key = u.get('chatgpt_api_key', '')
                self.groq_api_key = u.get('groq_api_key', '')
        except:
            self.chatgpt_api_key = ''
            self.groq_api_key = ''

    def open_settings(self):
        SettingsWindow(self.root, self)
