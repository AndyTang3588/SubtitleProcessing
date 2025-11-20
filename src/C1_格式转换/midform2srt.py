import re

# 辅助函数：读取输入文件
def read_input_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"输入文件 {filename} 未找到")
        exit(1)
    except UnicodeDecodeError:
        print("输入文件编码错误")
        exit(1)

# 辅助函数：将midform时间格式转换为SRT时间格式
def convert_midform_to_srt_time(time_str):
    """将midform时间格式 [hh:mm:ss.mmm] 转换为SRT时间格式 hh:mm:ss,mmm"""
    time_str = time_str.strip('[]')
    parts = time_str.split(':')
    if len(parts) == 3:  # hh:mm:ss.mmm
        h, m, s = parts
        seconds_parts = s.split('.')
        if len(seconds_parts) == 2:
            seconds, milliseconds = seconds_parts
            return f"{int(h):02}:{int(m):02}:{int(seconds):02},{int(milliseconds):03}"
    return None

# 从 cache/output3.midform 文件中读取字幕
input_data = read_input_file('cache/output3.midform')

# 逐行解析，支持注释与小时标记
lines = input_data.splitlines()
blocks = []
current_hour = 0
time_line_regex = re.compile(r'^(?:((?:\d{1,2}):)?)(\d{2}):(\d{2})\.(\d{3})-((?:\d{1,2}):)?(\d{2}):(\d{2})\.(\d{3})\](.*)$')

for raw in lines:
    s = raw.strip()
    if not s:
        continue
    if s.startswith('//'):
        continue
    add = re.match(r'^\[ADD\s+(\d+)\s+H\]$', s)
    if add:
        current_hour = int(add.group(1))
        continue
    m = time_line_regex.match(s)
    if not m:
        continue
    # 组：1 可选小时含冒号；2分；3秒；4毫秒；5可选小时含冒号；6分；7秒；8毫秒；9文本
    sh = m.group(1)
    sm = int(m.group(2))
    ss = int(m.group(3))
    sms = int(m.group(4))
    eh = m.group(5)
    em = int(m.group(6))
    es = int(m.group(7))
    ems = int(m.group(8))
    text = m.group(9).strip()

    start_hours = int(sh[:-1]) if sh else 0
    end_hours = int(eh[:-1]) if eh else 0
    # 若未给出小时，用当前小时标记
    if sh is None:
        start_hours = current_hour
    if eh is None:
        end_hours = current_hour

    def to_srt(h, m_, s_, ms_):
        return f"{h:02}:{m_:02}:{s_:02},{ms_:03}"

    srt_start = to_srt(start_hours, sm, ss, sms)
    srt_end = to_srt(end_hours, em, es, ems)
    blocks.append((srt_start, srt_end, text))

if not blocks:
    print("没有匹配到任何字幕")
    exit(1)

srt_lines = []
for i, (start_time_srt, end_time_srt, subtitle) in enumerate(blocks, 1):
    srt_lines.append(f"{i}")
    srt_lines.append(f"{start_time_srt} --> {end_time_srt}")
    srt_lines.append(subtitle)
    srt_lines.append("")

# 保存修改后的 SRT 文件
with open('cache/output3.srt', 'w', encoding='utf-8') as f:
    f.write("\n".join(srt_lines))

print("处理完成，生成了 cache/output3.srt 文件。")
