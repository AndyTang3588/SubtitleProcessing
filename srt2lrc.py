import re
import os

def srt_to_lrc(input_file='input.srt', output_file='output_srt.lrc'):
    # 检查输入文件是否存在
    if not os.path.isfile(input_file):
        print(f"Error: {input_file} does not exist.")
        return

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.readlines()
    except Exception as e:
        print(f"Error reading {input_file}: {e}")
        return

    lrc_lines = []
    pattern_time = re.compile(r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})')
    idx = 0

    while idx < len(content):
        line = content[idx].strip()

        if line.isdigit():  # 跳过序号
            idx += 1
            continue
        
        # 匹配时间戳
        time_match = pattern_time.match(line)
        if time_match:
            start_time = time_match.group(1)
            start_time_lrc = convert_time_to_lrc(start_time)
            idx += 1
            # 获取字幕文本
            subtitle_text = ''
            while idx < len(content) and content[idx].strip() != '':
                subtitle_text += content[idx].strip() + ' '
                idx += 1
            lrc_line = f'{start_time_lrc}{subtitle_text.strip()}'
            lrc_lines.append(lrc_line)
        else:
            idx += 1

    # 输出到 LRC 文件
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lrc_lines))
        print(f"Successfully converted to {output_file}")
    except Exception as e:
        print(f"Error writing to {output_file}: {e}")

def convert_time_to_lrc(srt_time):
    """将 SRT 时间格式转换为 LRC 时间格式"""
    hours, minutes, seconds_milliseconds = srt_time.split(':')
    seconds, milliseconds = seconds_milliseconds.split(',')
    # 转换为 LRC 格式 [mm:ss.xx]
    return f'[{int(minutes):02}:{int(seconds):02}.{int(milliseconds) // 10:02}]'

if __name__ == '__main__':
    srt_to_lrc()
