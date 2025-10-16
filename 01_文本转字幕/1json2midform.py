import json
import re

# 辅助函数：将秒数转为 'mm:ss.mmm'（压缩小时，小时由 [ADD X H] 指示）
def seconds_to_minsec_ms(seconds):
    """将秒数转换为 mm:ss.mmm（忽略小时部分，由标记行承载）"""
    try:
        within_hour = seconds % 3600
        minutes = int(within_hour // 60)
        remaining_seconds = within_hour % 60
        milliseconds = int((remaining_seconds - int(remaining_seconds)) * 1000)
        return f"{minutes:02}:{int(remaining_seconds):02}.{milliseconds:03}"
    except (ValueError, TypeError):
        return "00:00.000"

# 辅助函数：读取JSON文件
def read_json_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"输入文件 {filename} 未找到")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"JSON文件格式错误: {e}")
        exit(1)
    except UnicodeDecodeError:
        print("输入文件编码错误")
        exit(1)

# 从 cache/input.json 文件中读取数据
json_data = read_json_file('cache/input.json')

# 检查数据格式
if not isinstance(json_data, list):
    print("错误：JSON文件应该包含一个数组")
    exit(1)

# 生成midform格式（压缩小时、插入小时标记、无前中括号）
midform_lines = []

# 顶部两行保留注释
midform_lines.append("// A middle format for an APP about translation between .lrc & .srt file. It compresses the HH (hour) part of the timestamp.")
midform_lines.append("// The hour sign [ADD X H] can't be ignored. If a timestamp crosses an hour sign, it will stay before the sign.")

current_hour = None
for item in json_data:
    if not isinstance(item, dict):
        continue

    start_time = float(item.get('start', 0))
    end_time = float(item.get('end', start_time + 1))
    text = item.get('text', '')

    # 该段所属小时
    start_hour = int(start_time // 3600)
    # 若小时变化，插入小时标记
    if current_hour is None or start_hour != current_hour:
        current_hour = start_hour
        if current_hour > 0:
            midform_lines.append(f"[ADD {current_hour} H]")

    start_fmt = seconds_to_minsec_ms(start_time)
    end_fmt = seconds_to_minsec_ms(end_time)

    clean_text = re.sub(r'\s+', ' ', str(text).strip())
    if clean_text:
        midform_lines.append(f"{start_fmt}-{end_fmt}]{clean_text}")

# 保存midform文件
with open('cache/output1.midform', 'w', encoding='utf-8') as f:
    f.write("\n".join(midform_lines))

print("处理完成，生成了 cache/output1.midform 文件。")
