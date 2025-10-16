import re

# 可配置的默认持续时间
DEFAULT_DURATION = 3

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

# 辅助函数：将时间从 '00:00:00s' 转为 'hh:mm:ss,ms' 格式
def convert_to_srt_time(time_str):
    return time_str.replace('s', ',000')

# 辅助函数：将时间从 '00:00:00s' 转为 '[mm:ss.xx]' 格式
def convert_to_lrc_time(time_str):
    try:
        time_str = time_str.replace('s', '')
        h, m, s = time_str.split(':')
        total_seconds = int(h) * 3600 + int(m) * 60 + int(s)
        return f"[{total_seconds // 60:02}:{total_seconds % 60:02}.00]"
    except ValueError:
        raise ValueError(f"时间格式错误：{time_str}")

# 辅助函数：将秒数转为 'hh:mm:ss,ms' 格式
def seconds_to_srt_time(seconds):
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02}:{m:02}:{s:02},000"

# 从 cache/input.txt 文件中读取字幕
input_data = read_input_file('cache/input.txt')

# 用正则表达式匹配时间和字幕
pattern = re.compile(r'(\d{2}:\d{2}:\d{2}s)\s*\n([\s\S]+?)(?=\d{2}:\d{2}:\d{2}s|$)', re.DOTALL)
matches = pattern.findall(input_data)

# 生成LRC格式
lrc_lines = []
for time_str, subtitle in matches:
    lrc_time = convert_to_lrc_time(time_str)
    lrc_lines.append(f"{lrc_time} {subtitle.strip()}")  # 添加空格以分隔时间和字幕

with open('cache/output1.lrc', 'w', encoding='utf-8') as f:
    f.write("\n".join(lrc_lines))

# 生成SRT格式，处理每句字幕大于 DEFAULT_DURATION 秒的情况
srt_lines = []
for i, (time_str, subtitle) in enumerate(matches, 1):
    start_time = convert_to_srt_time(time_str)

    # 计算开始时间的秒数
    h, m, s = map(int, time_str.replace('s', '').split(':'))
    start_seconds = h * 3600 + m * 60 + s

    # 计算下一条字幕的开始时间，或者设置一个固定的结束时间
    if i < len(matches):
        next_time_str = matches[i][0].replace('s', '')
        h, m, s = map(int, next_time_str.split(':'))
        end_seconds = h * 3600 + m * 60 + s
    else:
        end_seconds = start_seconds + 10  # 默认最后一条字幕的持续时间为 10 秒

    # 如果持续时间大于 DEFAULT_DURATION，取最后 DEFAULT_DURATION 秒
    duration = end_seconds - start_seconds
    if duration > DEFAULT_DURATION:
        end_seconds = start_seconds + DEFAULT_DURATION  # 结束时间为开始时间加 DEFAULT_DURATION 秒

    end_time = seconds_to_srt_time(end_seconds)
    start_time = seconds_to_srt_time(start_seconds)

    srt_lines.append(f"{i}")
    srt_lines.append(f"{start_time} --> {end_time}")
    srt_lines.append(subtitle.strip())  # 去掉字幕前后的空格
    srt_lines.append("")  # 空行

# 保存修改后的 SRT 文件
with open('cache/output1.srt', 'w', encoding='utf-8') as f:
    f.write("\n".join(srt_lines))

print("处理完成，生成了 cache/output1.lrc 和 cache/output1.srt 文件。")
