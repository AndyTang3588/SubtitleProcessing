# 字幕处理工具集

这是一个用于处理字幕文件的Python工具集，支持多种字幕格式之间的转换和处理。

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

## 工作流程

### 标准处理流程
1. **文本转字幕** (`01_文本转字幕/`)
   - 输入：`input.txt`（包含时间戳和字幕文本）
   - 输出：`output1.lrc` 或 `output1.srt`

2. **去重处理** (`02_去重处理/`)
   - 输入：`output1.lrc`
   - 输出：`output2.lrc`
   - 功能：去除重复内容、字符重复、特定模式

3. **时间调整** (`03_时间调整/`)
   - 输入：`output2.lrc`
   - 输出：`output3.lrc`
   - 功能：调整时间轴偏移

4. **格式转换** (`04_格式转换/`)
   - 输入：`output3.lrc`
   - 输出：`output3.srt`
   - 功能：LRC与SRT格式互转

5. **格式还原** (`05_格式还原/`)
   - 输入：`output3.lrc`
   - 输出：`output3朴素.txt`
   - 功能：还原为原始文本格式

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
- **midform格式**：`[hh:mm:ss.mmm - hh:mm:ss.mmm] 字幕内容`
- **朴素格式**：`hh:mm:sss\n字幕内容`

## 使用方法

### 方法一：使用Launcher界面（推荐）

1. 运行 `python3 launcher.py` 启动图形界面
2. 点击"浏览"按钮选择输入的txt或json文件
3. 在界面中选择各步骤的版本（默认使用最新版本）
4. 对于步骤03，可以设置延时毫秒数（默认0）
5. 按顺序点击各步骤的"运行"按钮
6. 查看状态显示：Success（绿色）、Warning（黄色）、Error（红色）
7. 点击"生成转换结果"按钮获取最终文件

### 方法二：命令行方式

1. 将原始字幕文本保存为 `input.txt`
2. 按顺序运行各步骤的脚本
3. 根据需要选择合适的版本（v2、v3等）

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
- 时间格式：`[hh:mm:ss.mmm - hh:mm:ss.mmm]`
- 包含开始时间和结束时间
- 毫秒级精度（3位毫秒）
- 适合需要精确时间控制的应用场景

## 注意事项

- 所有脚本使用UTF-8编码
- 部分脚本会自动创建备份文件
- 时间格式支持小时、分钟、秒的完整格式
- 去重功能支持多种规则和正则表达式过滤
- midform格式提供更高的时间精度

