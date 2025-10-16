import json
import re

# 辅助函数：将秒数转为 'hh:mm:ss.mmm' 格式（midform格式）
def seconds_to_midform_time(seconds):
    """将秒数转换为midform时间格式 hh:mm:ss.mmm"""
    try:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        remaining_seconds = seconds % 60
        # 将小数秒转换为毫秒
        milliseconds = int((remaining_seconds - int(remaining_seconds)) * 1000)
        return f"{hours:02}:{minutes:02}:{int(remaining_seconds):02}.{milliseconds:03}"
    except (ValueError, TypeError):
        return "00:00:00.000"

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

# 生成midform格式
midform_lines = []
for item in json_data:
    if not isinstance(item, dict):
        continue
    
    # 提取时间信息
    start_time = item.get('start', 0)
    end_time = item.get('end', start_time + 1)  # 如果没有end时间，默认1秒后
    text = item.get('text', '')
    
    # 转换时间格式
    start_midform = seconds_to_midform_time(start_time)
    end_midform = seconds_to_midform_time(end_time)
    
    # 清理文本（去除多余的空白字符）
    clean_text = re.sub(r'\s+', ' ', text.strip())
    
    if clean_text:  # 只添加非空文本
        midform_lines.append(f"[{start_midform} - {end_midform}] {clean_text}")

# 保存midform文件
with open('cache/output1.midform', 'w', encoding='utf-8') as f:
    f.write("\n".join(midform_lines))

print("处理完成，生成了 cache/output1.midform 文件。")
