# 字幕处理工具集 (Subtitle Processing Toolkit)

一个功能强大的字幕文件处理工具集，支持多种字幕格式之间的转换和处理，提供现代化的图形界面和完整的工作流程。

## ✨ 主要特性

- 🌍 **多语言支持**：支持中文和英文界面（默认英文），可随时切换
- 🎨 **现代化界面**：基于 ttkbootstrap 的美观 GUI，支持主题切换
- 📝 **多格式支持**：支持 JSON、TXT、LRC、SRT、midform 等格式
- 🔄 **完整工作流**：从输入预处理到输出转换的完整流程
- ⚙️ **灵活配置**：支持 API 密钥配置（ChatGPT、Groq 等）
- 🚀 **后台处理**：多线程执行，不阻塞界面操作

## 📋 系统要求

- Python 3.7+
- tkinter（通常随 Python 安装）
- ttkbootstrap（启动脚本会自动安装）

## 🚀 快速开始

### 方法一：使用启动脚本（推荐）

**macOS & Linux：**
```bash
chmod +x start.sh
./start.sh
```

启动脚本会自动：
- 检查 Python 环境
- 检查并安装依赖（ttkbootstrap）
- 创建必要的目录（cache、output）
- 启动 GUI 程序

### 方法二：手动启动

**macOS & Linux：**
```bash
python3 launcher.py
```

**Windows：**
```bash
py -3 launcher.py
```

或者直接双击运行 `launcher.py`（系统已关联 .py 到 Python 的情况下）

### 安装依赖

如果启动脚本无法自动安装依赖，可手动执行：

```bash
pip install ttkbootstrap
```

## 📖 使用指南

### 推荐工作流程

1. **准备音频**
   - 将"生肉"视频/音频转换为体积较小的 mp3
   - 推荐使用 Groq 平台的 Whisper（模型 v3 / v3 turbo）
   - Groq 提供免费试用，足够日常使用

2. **获取 JSON 文件**
   - 在 Groq 的 Whisper 结果页面点击"copy json"
   - 保存为 `xxx.json` 文件
   - ⚠️ 不建议使用 TXT，容易出现格式/换行丢失

3. **输入预处理**（在 Launcher 中依次执行）
   - **A1 - 输入转字幕**：选择 JSON 文件，运行 `1json2midform.py`（自动检测文件格式）
   - **A2 - 去重处理**：运行 `2去重midform.py` 去除重复字幕
   - **A3 - 时间调整**：可选，填入毫秒延迟，自动处理小时标记

4. **AI 翻译**（可选，推荐）
   - 打开 `cache/` 目录，找到生成的 `.midform` 文件（推荐使用 `output2.midform` 或 `output3.midform`）
   - 使用 `ai_prompt_midform.txt` 作为提示词，让 AI 只翻译文本部分，保持时间与结构不变
   - 将 AI 的回复覆盖粘贴回对应 `.midform` 文件并保存

5. **输出处理**
   - **C1 - 格式转换**：选择脚本（`midform2lrc.py` 或 `midform2srt.py`），生成对应的 `.lrc` 或 `.srt` 文件
   - **C2 - 多语言字幕**：计划中功能

6. **生成最终文件**
   - 点击窗口底部"生成转换结果"按钮
   - 工具会将 cache 中最新优先级的输出复制到 `output/` 目录
   - 可选择"输出至原目录"选项，将文件保存到输入文件所在目录

### 界面说明

#### 界面布局

- **顶部区域**
  - 左侧：文件选择按钮和已选文件路径显示
  - 右侧：语言切换下拉框（中文/English）和设置按钮

- **中部区域**（支持横向滚动）
  - **输入预处理**（3 个步骤卡片）
    - A1 - 输入转字幕：自动检测文件格式，支持 JSON 等
    - A2 - 去重处理：去除重复字幕行
    - A3 - 时间调整：调整时间轴延迟
  - **文字内容精细处理**（计划中）
    - B1 - AI翻译：自动翻译字幕功能（开发中）
  - **输出处理**（2 个步骤卡片）
    - C1 - 格式转换：转换为 LRC 或 SRT 格式
    - C2 - 多语言字幕：设置指定语言字幕（开发中）

- **底部区域**
  - 输出选项：可选择输出至原目录
  - 生成转换结果按钮
  - 状态显示区域

#### 功能特点

- **智能文件检测**：A1 步骤会自动检测文件格式并提示
- **实时状态显示**：每个步骤显示运行状态（等待/运行中/成功/错误）
- **后台执行**：所有处理在后台线程执行，不阻塞界面
- **自动缓存管理**：所有中间文件保存在 `cache/` 目录
- **版本选择**：每个步骤支持多个脚本版本选择

## 📁 文件格式说明

### 输入格式

#### JSON 格式（推荐）
```json
[
  {
    "id": 0,
    "start": 0,
    "end": 2.24,
    "text": "晚上好呀大家"
  },
  {
    "id": 1,
    "start": 2.24,
    "end": 4.94,
    "text": "这里是FuLu万事屋"
  }
]
```

#### TXT 格式
```
00:00:00s
感谢观看哦~
00:00:30s
结束啦
00:59:51s
あたるあたるはそこはって気持ちいいよ
```

### 输出格式

- **LRC 格式**：`[mm:ss.xx] 字幕内容`
- **SRT 格式**：标准 SRT 字幕格式
- **midform 格式**：中间格式，用于 AI 翻译
  - 注释（前两行，必须保留）：
    - `// A middle format for an APP about translation between .lrc & .srt file. It compresses the HH (hour) part of the timestamp.`
    - `// The hour sign [ADD X H] can't be ignored. If a timestamp crosses an hour sign, it will stay before the sign.`
  - 小时标记：`[ADD X H]`
  - 时间行：`mm:ss.mmm-mm:ss.mmm]文本`（必要时也可出现显式小时 `HH:mm:ss.mmm`）
  - 毫秒级精度（3 位毫秒）
- **朴素格式**：`hh:mm:sss\n字幕内容`

## 🛠️ 脚本说明

### 输入预处理脚本

#### src/A1_输入转字幕/
- `1json2midform.py`：将 JSON 格式转换为 midform 格式（推荐）
- `1json2lrc&srt.py`：将 JSON 格式转换为 LRC 或 SRT 格式
- `1txt2lrc&srt.py`：将 TXT 格式转换为 LRC 或 SRT 格式

#### src/A2_去重处理/
- `2去重midform.py`：对 midform 格式进行去重处理（推荐）
- `2去重srt.py`：对 SRT 格式进行去重处理

#### src/A3_时间调整/
- `3延迟midform.py`：调整 midform 格式的时间轴
- `3延时lrc.py`：调整 LRC 格式的时间轴
- `3延时srt.py`：调整 SRT 格式的时间轴

### 输出处理脚本

#### src/C1_格式转换/
- `midform2srt.py`：将 midform 格式转换为 SRT 格式（推荐）
- `midform2lrc.py`：将 midform 格式转换为 LRC 格式
- `lrc转srt_v2.py`：将 LRC 格式转换为 SRT 格式

#### src/格式还原/
- `重返朴素格式.py`：将其他格式还原为朴素格式

#### src/工具脚本/
- 其他辅助脚本，提供额外工具功能

## ⚙️ 设置功能

点击右上角"设置"按钮可以配置：

- **ChatGPT API Key**：用于 ChatGPT API 调用（计划中）
- **Groq Platform API Key**：用于 Groq 平台 API 调用（计划中）

设置会自动保存到 `userSetting.json` 文件中。

## 🤖 AI 翻译支持

### 提示词文件

- **文件**：`ai_prompt_midform.txt`
- **作用**：用于引导大语言模型在不改变 midform 结构与时间轴的前提下，进行"二次元可爱风格"的中文字幕翻译，并在 R18 情境下使用更委婉的词汇规避审查
- **使用方式**：将 `ai_prompt_midform.txt` 的内容作为系统/前置提示，与待翻译的 midform 文本一并输入模型

### 推荐流程

1. 完成 A1、A2、A3 步骤后，在 `cache/` 目录找到生成的 `.midform` 文件
2. 打开文件，复制内容
3. 使用 AI 模型（如 ChatGPT、Claude 等）进行翻译
4. 将 `ai_prompt_midform.txt` 的内容作为系统提示
5. 将 midform 内容作为用户输入
6. 复制 AI 的回复，覆盖粘贴回原 `.midform` 文件
7. 继续执行 C1 步骤进行格式转换

## 📂 项目结构

```
SubtitleProcessing/
├── launcher.py              # 主启动文件
├── start.sh                 # 启动脚本（自动检查依赖）
├── README.md                # 本文件
├── userSetting.json         # 用户设置文件（自动生成）
├── ai_prompt_midform.txt    # AI 翻译提示词
│
├── ui/                      # UI 模块
│   ├── main_window.py       # 主窗口
│   ├── settings_window.py   # 设置窗口
│   ├── locales.py           # 多语言支持
│   ├── tb_compat.py         # ttkbootstrap 兼容层
│   └── theme_monitor.py     # 主题监听
│
├── src/
│   ├── A1_输入转字幕/       # 文本转字幕脚本
│   ├── A2_去重处理/         # 去重处理脚本
│   ├── A3_时间调整/         # 时间调整脚本
│   ├── C1_格式转换/         # 格式转换脚本
│   ├── 格式还原/            # 格式还原脚本
│   └── 工具脚本/            # 其他工具脚本
│
├── cache/                   # 缓存目录（自动生成）
├── output/                  # 输出目录（自动生成）
└── FileExemples/            # 示例文件
```

## 🌍 多语言支持

- **默认语言**：英文（English）
- **支持语言**：中文、英文
- **切换方式**：点击右上角语言下拉框
- **实时切换**：切换语言后，界面文本立即更新

## ⚠️ 注意事项

- 所有脚本使用 UTF-8 编码
- 部分脚本会自动创建备份文件
- 时间格式支持小时、分钟、秒的完整格式
- 去重功能支持多种规则和正则表达式过滤
- midform 格式提供更高的时间精度（毫秒级）
- 建议在处理前备份原始文件
- `cache/` 目录中的文件会在选择新文件时自动清理

## 📝 更新日志

### 最新版本
- ✨ 新增多语言支持（中文/英文，默认英文）
- 🎨 优化界面布局，采用卡片式设计
- ⚙️ 新增设置窗口，支持 API 密钥配置
- 🔄 改进文件格式自动检测功能
- 🐛 修复多个已知问题

## 📄 许可证

本项目为个人项目，仅供学习和个人使用。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**享受字幕处理的乐趣！** 🎬
