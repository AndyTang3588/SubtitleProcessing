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

# 辅助函数：将midform时间格式转换为LRC时间格式
def convert_midform_to_lrc_time(time_str):
    """将midform时间格式 [hh:mm:ss.mmm] 转换为LRC时间格式 [mm:ss.xx]"""
    time_str = time_str.strip('[]')
    parts = time_str.split(':')
    if len(parts) == 3:  # hh:mm:ss.mmm
        h, m, s = parts
        seconds_parts = s.split('.')
        if len(seconds_parts) == 2:
            seconds, milliseconds = seconds_parts
            # 将毫秒转换为百分之一秒
            centiseconds = int(milliseconds) // 10
            total_minutes = int(h) * 60 + int(m)
            return f"[{total_minutes:02}:{int(seconds):02}.{centiseconds:02}]"
    return None

# 从 cache/output3.midform 文件中读取字幕
input_data = read_input_file('cache/output3.midform')

lines = input_data.splitlines()
current_hour = 0
lrc_lines = []
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
    text = m.group(9).strip()

    start_hours = int(sh[:-1]) if sh else current_hour

    # 转换到绝对分钟：小时标记×60 + 分钟
    total_minutes = start_hours * 60 + sm
    lrc_lines.append(f"[{total_minutes:02}:{ss:02}.{sms//10:02}]{text}")

# 保存修改后的 LRC 文件
with open('cache/output3.lrc', 'w', encoding='utf-8') as f:
    f.write("\n".join(lrc_lines))

print("处理完成，生成了 cache/output3.lrc 文件。")
