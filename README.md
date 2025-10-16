# 字幕处理工具集

这是一个用于处理字幕文件的Python工具集，支持多种字幕格式之间的转换和处理。

## Launcher 启动方法（macOS & Linux / Windows）
- macOS & Linux：
  - 安装 Python3 后，在项目根目录执行：
    - `python3 launcher.py`
- Windows：
  - 安装 Python3 后，在项目根目录执行：
    - `py -3 launcher.py`
  - 或者直接双击运行 `launcher.py`（系统已关联 .py 到 Python 的情况下）

## 软件使用方法（推荐流程）
1. 准备音频：将“生肉”视频/音频转换为体积较小的 mp3，用于喂给 OpenAI Whisper（推荐 Groq 平台，模型 v3 / v3 turbo；Groq 有免费试用，够日常使用）。
2. 得到 JSON：在 Groq 的 Whisper 结果页面点击“copy json”，复制结果为 `xxx.json` 并保存。
   - 注：不建议使用 txt，txt 需要手动在网页上框选复制，容易出现格式/换行丢失。
3. 导入 JSON 到本工具：在 Launcher 中选择 `xxx.json` 文件，按需依次点击步骤 01、02、03：
   - 步骤 01：文本转字幕（选择 `1json2midform.py（最新）`）。
   - 步骤 02：去重处理（选择 `2去重midform.py（最新）`）。
   - 步骤 03：时间调整（可选，填入毫秒延迟，自动处理小时标记）。
4. 可选AI翻译（推荐）：
   - 打开 `/cache/` 目录，将刚生成的 `.midform` 文件（推荐使用 `output2.midform` 或 `output3.midform`）丢给 AI 翻译。
   - 使用 `ai_prompt_midform.txt` 作为提示词，让模型只翻译文本部分，保持时间与结构不变。
   - 将 AI 的回复覆盖粘贴回对应 `.midform` 文件并保存。
5. 格式转换：在 Launcher 的“格式转换”中选择脚本（`midform2lrc.py` 或 `midform2srt.py`），生成对应的 `.lrc` 或 `.srt`。
6. 生成最终文件：点击窗口底部“生成转换结果”，工具会将 cache 中最新优先级的输出复制到 `output/` 或原目录。

---

## 项目结构

```
SubtitleProcessing/
├── 01_文本转字幕/          # 第1步：将文本格式转换为LRC/SRT/midform格式
│   ├── 1txt2lrc_v2.py     # 文本转LRC格式（v2版本）
│   ├── 1txt2lrc_v3.py     # 文本转LRC格式（v3版本，支持小时进位）
│   ├── 1txt2lrc&srt.py    # 文本同时转换为LRC和SRT格式
│   ├── 1json2lrc.py       # JSON格式转LRC格式
│   ├── 1json2srt.py       # JSON格式转SRT格式
│   ├── 1json2lrc&srt.py   # JSON格式同时转换为LRC和SRT格式
│   └── 1json2midform.py   # JSON格式转midform格式
├── 02_去重处理/            # 第2步：去重处理
│   ├── 2去重.py           # 基础去重功能
│   ├── 2去重v2.py         # 改进的去重算法
│   ├── 2去重v3.py         # 高级去重功能（支持正则表达式过滤）
│   ├── 2去重srt.py        # SRT格式去重功能
│   └── 2去重midform.py    # midform格式去重功能
├── 03_时间调整/            # 第3步：时间轴调整
│   ├── 3延时.py           # LRC格式时间轴延时调整工具
│   ├── 3延时srt.py        # SRT格式时间轴延时调整工具
│   └── 3延迟midform.py    # midform格式时间轴延时调整工具
├── 04_格式转换/            # 格式转换工具
│   ├── lrc转srt.py        # LRC格式转SRT格式
│   ├── lrc转srt_v2.py     # LRC转SRT（v2版本，带备份功能）
│   ├── srt2lrc.py         # SRT格式转LRC格式
│   ├── midform2srt.py     # midform格式转SRT格式
│   └── midform2lrc.py     # midform格式转LRC格式
├── 05_格式还原/            # 格式还原工具
│   └── 重返朴素格式.py     # 将LRC格式还原为朴素文本格式
├── cache/                 # 临时文件目录（自动创建）
├── launcher.py            # 图形界面启动器
└── README.md              # 项目说明文档
```

## 工作流程（详细说明）
1. 将原视频/音频转为 mp3（更省 token，更稳定）。
2. 在 Groq 平台使用 Whisper（v3 / v3 turbo）转写，点击“copy json”保存为 `xxx.json`。
3. 在 Launcher 选择 `xxx.json`，运行步骤 01 → 02 → 03（03 为可选延时）。
4. （可选）到 `/cache/` 用 `ai_prompt_midform.txt` 引导大模型翻译 `output2.midform` 或 `output3.midform`，将结果粘回保存。
5. 在“格式转换”中选择脚本将 midform 转为 `.lrc` 或 `.srt`。
6. 点击“生成转换结果”，拷贝到输出目录。

## 文件说明

### 输入格式示例

#### TXT格式
```
00:00:00s
感谢观看哦~
00:00:30s
结束啦
00:59:51s
あたるあたるはそこはって気持ちいいよ
```

#### JSON格式
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
    "text": "这里是卫星俱乐部"
  }
]
```

### 输出格式
- **LRC格式**：`[mm:ss.xx] 字幕内容`
- **SRT格式**：标准SRT字幕格式
- **midform格式**：无前中括号、压缩小时：
  - 注释（前两行，必须保留）：
    - `// A middle format for an APP about translation between .lrc & .srt file. It compresses the HH (hour) part of the timestamp.`
    - `// The hour sign [ADD X H] can't be ignored. If a timestamp crosses an hour sign, it will stay before the sign.`
  - 小时标记：`[ADD X H]`
  - 时间行：`mm:ss.mmm-mm:ss.mmm]文本`（必要时也可出现显式小时 `HH:mm:ss.mmm`）
- **朴素格式**：`hh:mm:sss\n字幕内容`

## Launcher界面说明

### 界面布局
- **上部区域**：文件选择按钮和已选文件路径显示
- **中部区域**：4个步骤格，支持横向滚动
  - 步骤01：文本转字幕（7个版本可选，包括midform格式）
  - 步骤02：去重处理（5个版本可选，包括midform格式）
  - 步骤03：时间调整（可设置延时毫秒数，自动检测文件格式）
  - 步骤04：格式转换（5个版本可选，包括midform转换）
- **下部区域**：预留日志区域

### 功能特点
- 自动创建cache目录存储临时文件
- 支持版本选择，默认使用最新版本
- 实时状态显示（等待/运行中/Success/Warning/Error）
- 后台执行，不阻塞界面
- 自动文件复制和管理

## 新增功能

### midform格式支持
- **1json2midform.py**：将JSON格式转换为midform格式
- **2去重midform.py**：对midform格式进行去重处理
- **3延迟midform.py**：调整midform格式的时间轴
- **midform2srt.py**：将midform格式转换为SRT格式
- **midform2lrc.py**：将midform格式转换为LRC格式

### midform格式特点
- 时间行：`mm:ss.mmm-mm:ss.mmm]文本`（无前中括号，小时压缩）
- 小时标记：`[ADD X H]` 指示后续行所属绝对小时
- 注释：前两行以 `//` 开头，工具链保持并忽略
- 毫秒级精度（3位毫秒）

## AI 提示词
- 提示词文件：`ai_prompt_midform.txt`
- 作用：用于引导大语言模型在不改变 midform 结构与时间轴的前提下，进行“二次元可爱风格”的中文字幕翻译，并在 R18 情境下使用更委婉的词汇规避审查。
- 使用方式：将 `ai_prompt_midform.txt` 的内容作为系统/前置提示，与待翻译的 midform 文本一并输入模型。

## 注意事项

- 所有脚本使用UTF-8编码
- 部分脚本会自动创建备份文件
- 时间格式支持小时、分钟、秒的完整格式
- 去重功能支持多种规则和正则表达式过滤
- midform格式提供更高的时间精度

