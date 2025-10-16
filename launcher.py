#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import os
import shutil
import threading
from pathlib import Path

class SubtitleLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("字幕处理工具集 Launcher")
        self.root.geometry("1200x700")
        
        # 设置变量
        self.selected_file = tk.StringVar()
        self.delay_value = tk.StringVar(value="0")
        
        # 步骤版本选择变量
        self.step01_version = tk.StringVar(value="1json2midform.py (最新)")
        self.step02_version = tk.StringVar(value="2去重midform.py (最新)")
        self.step04_version = tk.StringVar(value="midform2srt.py (最新)")
        
        # 状态变量
        self.step01_status = tk.StringVar(value="等待")
        self.step02_status = tk.StringVar(value="等待")
        self.step03_status = tk.StringVar(value="等待")
        self.step04_status = tk.StringVar(value="等待")
        
        # 输出选项变量
        self.output_to_original = tk.BooleanVar(value=False)
        
        self.setup_ui()
        
    def setup_ui(self):
        # 上部区域 - 文件选择
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(top_frame, text="选择输入文件:").pack(side="left")
        ttk.Button(top_frame, text="浏览", command=self.select_file).pack(side="left", padx=(10, 0))
        ttk.Label(top_frame, textvariable=self.selected_file, foreground="blue").pack(side="left", padx=(10, 0))
        
        # 中部区域 - 步骤视图（可横向滚动）
        middle_frame = ttk.Frame(self.root)
        middle_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 创建Canvas和Scrollbar
        canvas = tk.Canvas(middle_frame, height=400)
        scrollbar = ttk.Scrollbar(middle_frame, orient="horizontal", command=canvas.xview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(xscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="bottom", fill="x")
        
        # 创建4个步骤格
        self.create_step_frames(scrollable_frame)
        
        # 下部区域 - 生成转换结果
        bottom_frame = ttk.Frame(self.root)
        bottom_frame.pack(fill="x", padx=10, pady=10)
        
        # 输出选项
        output_frame = ttk.Frame(bottom_frame)
        output_frame.pack(fill="x", pady=5)
        
        ttk.Checkbutton(output_frame, text="输出至原目录", variable=self.output_to_original).pack(side="left")
        ttk.Button(output_frame, text="生成转换结果", command=self.generate_results).pack(side="left", padx=(20, 0))
        
        # 状态显示
        self.result_status = tk.StringVar(value="等待生成结果")
        ttk.Label(bottom_frame, textvariable=self.result_status, foreground="blue").pack(pady=5)
        
    def create_step_frames(self, parent):
        # 步骤01 - 文本转字幕
        step01_frame = ttk.LabelFrame(parent, text="步骤01 - 文本转字幕", width=220, height=350)
        step01_frame.pack(side="left", padx=10, pady=5, fill="y")
        step01_frame.pack_propagate(False)
        
        ttk.Label(step01_frame, text="选择版本:").pack(pady=5)
        step01_combo = ttk.Combobox(step01_frame, textvariable=self.step01_version, 
                                  values=["1json2midform.py (最新)", "1json2lrc&srt.py", "1txt2lrc&srt.py"],
                                  state="readonly", width=15)
        step01_combo.pack(pady=5)
        
        ttk.Button(step01_frame, text="运行", command=lambda: self.run_step("01")).pack(pady=10)
        ttk.Label(step01_frame, textvariable=self.step01_status, foreground="blue").pack()
        
        # 步骤02 - 去重处理
        step02_frame = ttk.LabelFrame(parent, text="步骤02 - 去重处理", width=220, height=350)
        step02_frame.pack(side="left", padx=10, pady=5, fill="y")
        step02_frame.pack_propagate(False)
        
        ttk.Label(step02_frame, text="选择版本:").pack(pady=5)
        step02_combo = ttk.Combobox(step02_frame, textvariable=self.step02_version,
                                  values=["2去重midform.py (最新)", "2去重srt.py"],
                                  state="readonly", width=15)
        step02_combo.pack(pady=5)
        
        ttk.Button(step02_frame, text="运行", command=lambda: self.run_step("02")).pack(pady=10)
        ttk.Label(step02_frame, textvariable=self.step02_status, foreground="blue").pack()
        
        # 步骤03 - 时间调整
        step03_frame = ttk.LabelFrame(parent, text="步骤03 - 时间调整", width=220, height=350)
        step03_frame.pack(side="left", padx=10, pady=5, fill="y")
        step03_frame.pack_propagate(False)
        
        ttk.Label(step03_frame, text="延时(毫秒):").pack(pady=5)
        delay_entry = ttk.Entry(step03_frame, textvariable=self.delay_value, width=10)
        delay_entry.pack(pady=5)
        
        ttk.Button(step03_frame, text="运行", command=lambda: self.run_step("03")).pack(pady=10)
        ttk.Label(step03_frame, textvariable=self.step03_status, foreground="blue").pack()
        
        # 步骤04 - 格式转换
        step04_frame = ttk.LabelFrame(parent, text="步骤04 - 格式转换", width=220, height=350)
        step04_frame.pack(side="left", padx=10, pady=5, fill="y")
        step04_frame.pack_propagate(False)
        
        ttk.Label(step04_frame, text="选择版本:").pack(pady=5)
        step04_combo = ttk.Combobox(step04_frame, textvariable=self.step04_version,
                                  values=["midform2srt.py (最新)", "midform2lrc.py", "lrc转srt_v2.py"],
                                  state="readonly", width=15)
        step04_combo.pack(pady=5)
        
        ttk.Button(step04_frame, text="运行", command=lambda: self.run_step("04")).pack(pady=10)
        ttk.Label(step04_frame, textvariable=self.step04_status, foreground="blue").pack()
        
    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="选择字幕文件",
            filetypes=[("文本文件", "*.txt"), ("JSON文件", "*.json"), ("所有文件", "*.*")]
        )
        if file_path:
            self.selected_file.set(file_path)
            # 清理cache目录，准备新的处理
            self.clean_cache()
            # 重置所有步骤状态
            self.reset_step_status()
    
    def clean_cache(self):
        """清理cache目录中的所有文件"""
        try:
            cache_dir = Path("cache")
            if cache_dir.exists():
                # 删除cache目录中的所有文件
                for file_path in cache_dir.iterdir():
                    if file_path.is_file():
                        file_path.unlink()
                print("Cache目录已清理")
        except Exception as e:
            print(f"清理cache目录时出错: {e}")
    
    def reset_step_status(self):
        """重置所有步骤的状态"""
        self.step01_status.set("等待")
        self.step02_status.set("等待")
        self.step03_status.set("等待")
        self.step04_status.set("等待")
        self.result_status.set("等待生成结果")
    
    def _create_temp_srt_dedup_script(self):
        """创建临时的SRT去重脚本"""
        temp_script_content = '''import re

def remove_duplicates_from_srt(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 分割SRT内容为单独的块
    srt_blocks = []
    blocks = content.strip().split('\\n\\n')
    
    for block in blocks:
        lines = block.strip().split('\\n')
        if len(lines) >= 3:  # 序号、时间、文本
            srt_blocks.append(lines)

    processed_blocks = []
    last_content = ""

    # 定义要删除的内容的正则表达式集合
    patterns_to_remove = {
        r'晚安.*',
        r'あ、あ、.*',
        r'あああ.*',
    }

    # 用于移除比较时的符号
    def clean_content(content):
        return re.sub(r'[{}，。~?!ー？！]', '', content)

    for i, block in enumerate(srt_blocks, 1):
        if len(block) < 3:
            continue
            
        sequence = block[0]
        time_line = block[1]
        text_content = ' '.join(block[2:])
        
        # 规则1：完全相同字符重复超过3次
        text_content = re.sub(r'(.)\\1{3,}', r'\\1\\1\\1', text_content)

        # 规则2：相同的2个字、3个字和4个字重复超过3次
        text_content = re.sub(r'(..)\\1{3,}', r'\\1\\1\\1', text_content)
        text_content = re.sub(r'(...)\\1{3,}', r'\\1\\1\\1', text_content)
        text_content = re.sub(r'(....)\\1{3,}', r'\\1\\1\\1', text_content)

        # 检查内容是否匹配集合中的任何正则表达式
        if any(re.search(pattern, text_content) for pattern in patterns_to_remove):
            continue

        # 规则3：删除内容完全重复的上一行，忽略特定符号
        cleaned_content = clean_content(text_content)
        if clean_content(last_content) == cleaned_content:
            continue

        # 规则4：如果最后一个字符是中文逗号句号，删除句号
        if text_content.endswith('。'):
            text_content = text_content[:-1]
        if text_content.endswith('，'):
            text_content = text_content[:-1]

        last_content = text_content
        
        # 重新构建SRT块
        new_block = [str(len(processed_blocks) + 1), time_line, text_content]
        processed_blocks.append(new_block)

    # 写入到 output2.srt 文件
    with open(output_file, 'w', encoding='utf-8') as f:
        for block in processed_blocks:
            f.write('\\n'.join(block))
            f.write('\\n\\n')

# 使用函数处理文件
remove_duplicates_from_srt('cache/output1.srt', 'cache/output2.srt')
print("处理完成，生成了 cache/output2.srt 文件。")
'''
        with open('temp_srt_dedup.py', 'w', encoding='utf-8') as f:
            f.write(temp_script_content)
            
    def run_step(self, step_num):
        if not self.selected_file.get():
            messagebox.showwarning("警告", "请先选择输入文件")
            return
            
        # 在后台线程中运行步骤
        thread = threading.Thread(target=self._execute_step, args=(step_num,))
        thread.daemon = True
        thread.start()
        
    def _execute_step(self, step_num):
        try:
            # 创建cache目录
            cache_dir = Path("cache")
            cache_dir.mkdir(exist_ok=True)
            
            # 根据文件类型复制到cache目录
            input_file = Path(self.selected_file.get())
            if input_file.suffix.lower() == '.json':
                shutil.copy2(input_file, cache_dir / "input.json")
            else:
                shutil.copy2(input_file, cache_dir / "input.txt")
            
            # 更新状态为运行中
            getattr(self, f"step{step_num.zfill(2)}_status").set("运行中...")
            
            # 构建脚本路径和参数
            if step_num == "01":
                # 检查用户选择的脚本是否与文件类型匹配
                input_file = Path(self.selected_file.get())
                selected_script = self.step01_version.get()
                
                # 移除后缀 "(最新)" 等
                script_name = selected_script.split(" (")[0]
                
                # 如果是JSON文件但选择了txt脚本，或相反，则提示用户
                if input_file.suffix.lower() == '.json' and not script_name.startswith('1json'):
                    messagebox.showwarning("警告", "您选择了JSON文件但脚本是为TXT设计的，请选择JSON脚本")
                    getattr(self, f"step{step_num.zfill(2)}_status").set("等待")
                    return
                elif input_file.suffix.lower() != '.json' and script_name.startswith('1json'):
                    messagebox.showwarning("警告", "您选择了TXT文件但脚本是为JSON设计的，请选择TXT脚本")
                    getattr(self, f"step{step_num.zfill(2)}_status").set("等待")
                    return
                
                script_path = f"01_文本转字幕/{script_name}"
                args = []
            elif step_num == "02":
                selected_script = self.step02_version.get()
                # 移除后缀 "(最新)" 等
                script_name = selected_script.split(" (")[0]
                script_path = f"02_去重处理/{script_name}"
                
                # 根据脚本类型设置输入输出文件
                if script_name == "2去重srt.py":
                    # SRT去重脚本需要修改输入输出文件路径
                    # 这里我们创建一个临时脚本来处理
                    self._create_temp_srt_dedup_script()
                    script_path = "temp_srt_dedup.py"
                args = []
            elif step_num == "03":
                # 检查输出文件类型，选择对应的延时脚本
                cache_dir = Path("cache")
                if (cache_dir / "output2.midform").exists():
                    script_path = "03_时间调整/3延迟midform.py"
                elif (cache_dir / "output2.srt").exists():
                    script_path = "03_时间调整/3延时srt.py"
                else:
                    script_path = "03_时间调整/3延时.py"
                args = [self.delay_value.get()]
            elif step_num == "04":
                selected_script = self.step04_version.get()
                # 移除后缀 "(最新)" 等
                script_name = selected_script.split(" (")[0]
                script_path = f"04_格式转换/{script_name}"
                args = []
            else:
                return
                
            # 执行脚本
            result = subprocess.run(
                ["/usr/local/bin/python3", script_path] + args,
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            
            # 更新状态
            if result.returncode == 0:
                getattr(self, f"step{step_num.zfill(2)}_status").set("Success")
                # 设置绿色
                status_label = None
                for widget in self.root.winfo_children():
                    if isinstance(widget, ttk.Frame):
                        for child in widget.winfo_children():
                            if isinstance(child, tk.Canvas):
                                for grandchild in child.winfo_children():
                                    if isinstance(grandchild, ttk.Frame):
                                        for greatgrandchild in grandchild.winfo_children():
                                            if isinstance(greatgrandchild, ttk.Label) and greatgrandchild.cget("textvariable") == getattr(self, f"step{step_num.zfill(2)}_status"):
                                                greatgrandchild.configure(foreground="green")
                                                break
            else:
                getattr(self, f"step{step_num.zfill(2)}_status").set("Warning")
                # 设置黄色
                for widget in self.root.winfo_children():
                    if isinstance(widget, ttk.Frame):
                        for child in widget.winfo_children():
                            if isinstance(child, tk.Canvas):
                                for grandchild in child.winfo_children():
                                    if isinstance(grandchild, ttk.Frame):
                                        for greatgrandchild in grandchild.winfo_children():
                                            if isinstance(greatgrandchild, ttk.Label) and greatgrandchild.cget("textvariable") == getattr(self, f"step{step_num.zfill(2)}_status"):
                                                greatgrandchild.configure(foreground="orange")
                                                break
                                                
        except Exception as e:
            getattr(self, f"step{step_num.zfill(2)}_status").set(f"Error: {str(e)}")
            messagebox.showerror("错误", f"执行步骤{step_num}时出错: {str(e)}")
    
    def generate_results(self):
        """生成转换结果并复制到指定目录"""
        try:
            self.result_status.set("正在生成结果...")
            
            # 获取输入文件的基础名称（不含扩展名）
            input_file_path = self.selected_file.get()
            if not input_file_path:
                messagebox.showwarning("警告", "请先选择输入文件")
                self.result_status.set("等待生成结果")
                return
                
            input_basename = Path(input_file_path).stem
            
            # 确定输出目录
            if self.output_to_original.get():
                output_dir = Path(input_file_path).parent
            else:
                output_dir = Path("output")
                output_dir.mkdir(exist_ok=True)
            
            # 按优先级查找最新的输出文件
            cache_dir = Path("cache")
            copied_files = []
            
            # 优先级：output3 > output2 > output1
            for priority in ["output3", "output2", "output1"]:
                lrc_file = cache_dir / f"{priority}.lrc"
                srt_file = cache_dir / f"{priority}.srt"
                
                # 复制LRC文件
                if lrc_file.exists():
                    dest_lrc = output_dir / f"{input_basename}.lrc"
                    shutil.copy2(lrc_file, dest_lrc)
                    copied_files.append(str(dest_lrc))
                    break
            
            # 查找SRT文件（可能来自不同步骤）
            for priority in ["output3", "output2", "output1"]:
                srt_file = cache_dir / f"{priority}.srt"
                if srt_file.exists():
                    dest_srt = output_dir / f"{input_basename}.srt"
                    shutil.copy2(srt_file, dest_srt)
                    copied_files.append(str(dest_srt))
                    break
            
            if copied_files:
                self.result_status.set(f"成功生成 {len(copied_files)} 个文件")
                
                # 打开输出目录
                if os.name == 'nt':  # Windows
                    os.startfile(output_dir)
                elif os.name == 'posix':  # macOS and Linux
                    subprocess.run(['open', str(output_dir)])
            else:
                self.result_status.set("未找到可复制的文件")
                messagebox.showwarning("警告", "在cache目录中未找到任何输出文件")
                
        except Exception as e:
            self.result_status.set(f"生成失败: {str(e)}")
            messagebox.showerror("错误", f"生成结果时出错: {str(e)}")

def main():
    root = tk.Tk()
    app = SubtitleLauncher(root)
    root.mainloop()

if __name__ == "__main__":
    main()
