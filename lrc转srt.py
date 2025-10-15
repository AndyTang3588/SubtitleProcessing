import re

# 可配置的默认持续时间
DEFAULT_DURATION = 8

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

# 辅助函数：将时间从 '[hh:mm:ss.xx]' 或 '[mm:ss.xx]' 转为 'hh:mm:ss,ms' 格式
def convert_to_srt_time(time_str):
    time_str = time_str.strip('[]')
    parts = time_str.split(':')
    if len(parts) == 3:  # hh:mm:ss
        h, m, s = parts
    elif len(parts) == 2:  # mm:ss
        h = 0
        m, s = parts
    else:
        return None
    total_seconds = int(h) * 3600 + int(m) * 60 + float(s)
    ms = int((total_seconds - int(total_seconds)) * 1000)
    return f"{int(total_seconds // 3600):02}:{int(total_seconds % 3600 // 60):02}:{int(total_seconds % 60):02},{ms:03}"

# 从 output3.lrc 文件中读取字幕
input_data = read_input_file('output3.lrc')

# 用正则表达式匹配时间和字幕
pattern = re.compile(r'(\[\d{1,2}:\d{2}\.\d{2}\]|\[\d{1,2}:\d{2}:\d{2}\.\d{2}\])\s*(.+?)(?=\[\d{1,2}:\d{2}\.\d{2}\]|\[\d{1,2}:\d{2}:\d{2}\.\d{2}\]|$)', re.DOTALL)
matches = pattern.findall(input_data)

# 检查 matches 是否为空
if not matches:
    print("没有匹配到任何字幕")
    exit(1)

# 生成 SRT 格式
srt_lines = []
for i, (time_str, subtitle) in enumerate(matches, 1):
    start_time = time_str.strip()  # LRC 格式时间

    # 判断时间格式是否包含小时
    if re.match(r'\[\d{1,2}:\d{2}:\d{2}\.\d{2}\]', start_time):
        # hh:mm:ss.xx 格式
        minutes, seconds = start_time.strip('[]').split(':')[1:3]  # 只提取分钟和秒
        h = start_time.strip('[]').split(':')[0]  # 小时
    else:
        # mm:ss.xx 格式
        minutes, seconds = start_time.strip('[]').split(':')  # 提取分钟和秒
        h = 0  # 没有小时

    if len(seconds.split('.')) == 2:  # 有毫秒
        seconds = seconds.split('.')
        start_seconds = int(h) * 3600 + int(minutes) * 60 + float(seconds[0]) + (int(seconds[1]) / 100)
    else:
        start_seconds = int(h) * 3600 + int(minutes) * 60 + float(seconds)

    # 计算下一条字幕的开始时间，或者设置一个固定的结束时间
    if i < len(matches):
        next_time_str = matches[i][0]
        next_parts = next_time_str.strip('[]').split(':')

        if len(next_parts) == 3:  # hh:mm:ss
            hours = next_parts[0]
            minutes = next_parts[1]
            seconds = next_parts[2]
        elif len(next_parts) == 2:  # mm:ss
            hours = 0
            minutes = next_parts[0]
            seconds = next_parts[1]
        else:
            print(f"无效的时间戳格式: {next_time_str}")
            continue

        end_seconds = int(hours) * 3600 + int(minutes) * 60 + float(seconds)
    else:
        end_seconds = start_seconds + DEFAULT_DURATION  # 默认最后一条字幕的持续时间

    # 如果持续时间大于 DEFAULT_DURATION，取最后 DEFAULT_DURATION 秒
    duration = end_seconds - start_seconds
    if duration > DEFAULT_DURATION:
        end_seconds = start_seconds + DEFAULT_DURATION

    # 转换时间
    start_time_srt = convert_to_srt_time(start_time)
    end_time_srt = convert_to_srt_time(f"[{int(end_seconds // 60):02}:{end_seconds % 60:.2f}]")

    srt_lines.append(f"{i}")
    srt_lines.append(f"{start_time_srt} --> {end_time_srt}")
    srt_lines.append(subtitle.strip())  # 去掉字幕前后的空格
    srt_lines.append("")  # 空行

# 保存修改后的 SRT 文件
with open('output3.srt', 'w', encoding='utf-8') as f:
    f.write("\n".join(srt_lines))

print("处理完成，生成了 output3.srt 文件。")
