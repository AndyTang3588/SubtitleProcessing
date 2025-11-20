import re
import sys

# 获取命令行参数，如果没有提供则默认为0
try:
    time_offset = int(sys.argv[1]) if len(sys.argv) > 1 else 0
except ValueError:
    print("输入无效，默认为0毫秒。")
    time_offset = 0

# 读取cache/output2.srt文件
try:
    with open('cache/output2.srt', 'r', encoding='utf-8') as file:
        content = file.read()
except FileNotFoundError:
    print("错误：未找到文件 'cache/output2.srt'。请确保文件存在于cache目录。")
    exit(1)
except Exception as e:
    print(f"读取文件时出错: {e}")
    exit(1)

# 正则表达式匹配SRT时间格式 hh:mm:ss,mmm --> hh:mm:ss,mmm
time_pattern = re.compile(r'(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})')

def adjust_srt_time(time_str, offset):
    """调整SRT时间格式，offset为毫秒"""
    try:
        # 解析时间格式 hh:mm:ss,mmm
        time_part, ms_part = time_str.split(',')
        h, m, s = map(int, time_part.split(':'))
        ms = int(ms_part)
        
        # 转换为总毫秒数
        total_ms = h * 3600000 + m * 60000 + s * 1000 + ms + offset
        
        if total_ms < 0:
            total_ms = 0  # 将负时间设置为零
        
        # 转换回 hh:mm:ss,mmm 格式
        new_h = total_ms // 3600000
        new_m = (total_ms % 3600000) // 60000
        new_s = (total_ms % 60000) // 1000
        new_ms = total_ms % 1000
        
        return f"{new_h:02}:{new_m:02}:{new_s:02},{new_ms:03}"
    except Exception as e:
        print(f"处理时间时出错: {e}")
        return time_str

def adjust_srt_content(content, offset):
    """调整SRT内容中的所有时间"""
    def replace_time(match):
        start_time = match.group(1)
        end_time = match.group(2)
        
        new_start = adjust_srt_time(start_time, offset)
        new_end = adjust_srt_time(end_time, offset)
        
        return f"{new_start} --> {new_end}"
    
    return re.sub(time_pattern, replace_time, content)

# 调整SRT内容
adjusted_content = adjust_srt_content(content, time_offset)

# 写入cache/output3.srt文件
try:
    with open('cache/output3.srt', 'w', encoding='utf-8') as file:
        file.write(adjusted_content)
    print("时间轴调整完成，输出文件为 'cache/output3.srt'。")
except Exception as e:
    print(f"写入文件时出错: {e}")
    exit(1)
