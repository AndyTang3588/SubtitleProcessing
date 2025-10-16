import re
import sys

# 获取命令行参数，如果没有提供则默认为0
try:
    time_offset = int(sys.argv[1]) if len(sys.argv) > 1 else 0
except ValueError:
    print("输入无效，默认为0毫秒。")
    time_offset = 0

# 读取cache/output2.midform文件
try:
    with open('cache/output2.midform', 'r', encoding='utf-8') as file:
        lines = file.readlines()
except FileNotFoundError:
    print("错误：未找到文件 'cache/output2.midform'。请确保文件存在于cache目录。")
    exit(1)
except Exception as e:
    print(f"读取文件时出错: {e}")
    exit(1)

# 正则表达式匹配midform时间格式 [hh:mm:ss.mmm - hh:mm:ss.mmm]
# 其中 mmm 为三位毫秒
time_pattern = re.compile(r'\[(\d{1,2}):(\d{2}):(\d{2})\.(\d{3})\s*-\s*(\d{1,2}):(\d{2}):(\d{2})\.(\d{3})\]')

def adjust_time(line, offset):
    def shift_time(match):
        try:
            # 提取开始时间
            start_hours = int(match.group(1))
            start_minutes = int(match.group(2))
            start_seconds = int(match.group(3))
            start_milliseconds = int(match.group(4))
            
            # 提取结束时间
            end_hours = int(match.group(5))
            end_minutes = int(match.group(6))
            end_seconds = int(match.group(7))
            end_milliseconds = int(match.group(8))

            # 将时间转换为总毫秒数
            start_total_ms = (start_hours * 3600 * 1000) + (start_minutes * 60 * 1000) + (start_seconds * 1000) + start_milliseconds + offset
            end_total_ms = (end_hours * 3600 * 1000) + (end_minutes * 60 * 1000) + (end_seconds * 1000) + end_milliseconds + offset

            # 确保时间不为负数
            if start_total_ms < 0:
                start_total_ms = 0
            if end_total_ms < 0:
                end_total_ms = 0

            # 计算新的开始时间
            new_start_hours = start_total_ms // 3600000
            new_start_minutes = (start_total_ms % 3600000) // 60000
            new_start_seconds = (start_total_ms % 60000) // 1000
            new_start_milliseconds = start_total_ms % 1000

            # 计算新的结束时间
            new_end_hours = end_total_ms // 3600000
            new_end_minutes = (end_total_ms % 3600000) // 60000
            new_end_seconds = (end_total_ms % 60000) // 1000
            new_end_milliseconds = end_total_ms % 1000

            # 格式化时间字符串
            start_time = f'{new_start_hours:02}:{new_start_minutes:02}:{new_start_seconds:02}.{new_start_milliseconds:03}'
            end_time = f'{new_end_hours:02}:{new_end_minutes:02}:{new_end_seconds:02}.{new_end_milliseconds:03}'
            
            return f'[{start_time} - {end_time}]'
        except Exception as e:
            print(f"处理时间时出错: {e}")
            return match.group(0)  # 返回原始匹配，避免替换

    return re.sub(time_pattern, shift_time, line)

# 写入cache/output3.midform文件
try:
    with open('cache/output3.midform', 'w', encoding='utf-8') as file:
        for line in lines:
            adjusted_line = adjust_time(line, time_offset)
            file.write(adjusted_line)
    print("时间轴调整完成，输出文件为 'cache/output3.midform'。")
except Exception as e:
    print(f"写入文件时出错: {e}")
    exit(1)
