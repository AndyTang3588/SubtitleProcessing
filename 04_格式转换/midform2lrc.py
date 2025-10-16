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

# 用正则表达式匹配midform格式的时间和字幕
# 匹配格式: [hh:mm:ss.mmm - hh:mm:ss.mmm] text
pattern = re.compile(r'\[(\d{1,2}:\d{2}:\d{2}\.\d{3})\s*-\s*(\d{1,2}:\d{2}:\d{2}\.\d{3})\]\s*(.+?)(?=\[\d{1,2}:\d{2}:\d{2}\.\d{3}\s*-\s*\d{1,2}:\d{2}:\d{2}\.\d{3}\]|$)', re.DOTALL)
matches = pattern.findall(input_data)

# 检查 matches 是否为空
if not matches:
    print("没有匹配到任何字幕")
    exit(1)

# 生成 LRC 格式
lrc_lines = []
for start_time_str, end_time_str, subtitle in matches:
    # 转换时间格式（LRC只需要开始时间）
    start_time_lrc = convert_midform_to_lrc_time(f"[{start_time_str}]")
    
    if start_time_lrc:
        lrc_lines.append(f"{start_time_lrc}{subtitle.strip()}")

# 保存修改后的 LRC 文件
with open('cache/output4.lrc', 'w', encoding='utf-8') as f:
    f.write("\n".join(lrc_lines))

print("处理完成，生成了 cache/output4.lrc 文件。")
