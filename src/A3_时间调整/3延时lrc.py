import re
import sys

# 获取命令行参数，如果没有提供则默认为0
try:
    time_offset = int(sys.argv[1]) if len(sys.argv) > 1 else 0
except ValueError:
    print("输入无效，默认为0毫秒。")
    time_offset = 0

# 读取cache/output2.lrc文件
try:
    with open('cache/output2.lrc', 'r', encoding='utf-8') as file:
        lines = file.readlines()
except FileNotFoundError:
    print("错误：未找到文件 'cache/output2.lrc'。请确保文件存在于cache目录。")
    exit(1)
except Exception as e:
    print(f"读取文件时出错: {e}")
    exit(1)

# 正则表达式匹配时间格式 [mm:ss.xx] 或 [hh:mm:ss.xx]
# 其中 xx 为两位百分之一秒
time_pattern = re.compile(r'\[(?:(\d+):)?(\d{1,2}):(\d{2})\.(\d{2})\]')

def adjust_time(line, offset):
    def shift_time(match):
        try:
            # 提取时间
            hours = int(match.group(1)) if match.group(1) else 0  # 有时没有小时部分
            minutes = int(match.group(2))
            seconds = int(match.group(3))
            centiseconds = int(match.group(4))

            # 将时间转换为总百分之一秒数
            total_cs = (hours * 3600 * 100) + (minutes * 60 * 100) + (seconds * 100) + centiseconds + offset

            if total_cs < 0:
                total_cs = 0  # 将负时间设置为零

            # 计算新的小时、分钟、秒和百分之一秒
            new_hours = total_cs // 360000
            new_minutes = (total_cs % 360000) // 6000
            new_seconds = (total_cs % 6000) // 100
            new_centiseconds = total_cs % 100

            # 判断是否需要小时部分，只有在超过1小时才显示
            if new_hours > 0:
                return f'[{new_hours:02}:{new_minutes:02}:{new_seconds:02}.{new_centiseconds:02}]'
            else:
                return f'[{new_minutes:02}:{new_seconds:02}.{new_centiseconds:02}]'
        except Exception as e:
            print(f"处理时间时出错: {e}")
            return match.group(0)  # 返回原始匹配，避免替换

    return re.sub(time_pattern, shift_time, line)

# 写入cache/output3.lrc文件
try:
    with open('cache/output3.lrc', 'w', encoding='utf-8') as file:
        for line in lines:
            adjusted_line = adjust_time(line, time_offset)
            file.write(adjusted_line)
    print("时间轴调整完成，输出文件为 'cache/output3.lrc'。")
except Exception as e:
    print(f"写入文件时出错: {e}")
    exit(1)
