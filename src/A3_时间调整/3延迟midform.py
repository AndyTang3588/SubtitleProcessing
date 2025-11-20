import re
import sys

# 获取命令行参数，如果没有提供则默认为0
try:
    time_offset = int(sys.argv[1]) if len(sys.argv) > 1 else 0
except ValueError:
    print("输入无效，默认为0毫秒。")
    time_offset = 0

# 读取cache/outputA2.midform文件
try:
    with open('cache/outputA2.midform', 'r', encoding='utf-8') as file:
        lines = file.readlines()
except FileNotFoundError:
    print("错误：未找到文件 'cache/outputA2.midform'。请确保文件存在于cache目录。")
    exit(1)
except Exception as e:
    print(f"读取文件时出错: {e}")
    exit(1)

# 正则表达式匹配midform时间格式 mm:ss.mmm-mm:ss.mmm] 或 HH:MM:SS.mmm-HH:MM:SS.mmm]
# 我们支持两种（允许可选小时），但新的midform压缩为 mm:ss.mmm
time_pattern = re.compile(r'(?:((?:\d{1,2}):)?)(\d{2}):(\d{2})\.(\d{3})-(?:((?:\d{1,2}):)?)(\d{2}):(\d{2})\.(\d{3})\]')

def adjust_time(line, offset):
    def shift_time(match):
        try:
            # 组：1 可选小时+冒号，2 分，3 秒，4 毫秒；5 可选小时+冒号，6 分，7 秒，8 毫秒
            sh_group = match.group(1)
            start_hours = int(sh_group[:-1]) if sh_group else 0
            start_minutes = int(match.group(2))
            start_seconds = int(match.group(3))
            start_milliseconds = int(match.group(4))
            
            eh_group = match.group(5)
            end_hours = int(eh_group[:-1]) if eh_group else 0
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
            
            return f'{start_time}-{end_time}]'
        except Exception as e:
            print(f"处理时间时出错: {e}")
            return match.group(0)  # 返回原始匹配，避免替换

    return re.sub(time_pattern, shift_time, line)

# 写入cache/output3.midform文件（根据偏移重新计算并输出小时标记）
try:
    with open('cache/output3.midform', 'w', encoding='utf-8') as file:
        # 先写入前两行注释（若存在）
        idx = 0
        while idx < len(lines) and lines[idx].lstrip().startswith('//'):
            file.write(lines[idx])
            idx += 1

        # 当前输入小时标记，用于还原绝对时间（缺省为0）
        input_hour = 0
        # 当前输出小时标记（用于避免重复输出）
        output_hour = None

        # 从idx开始处理剩余行
        for j in range(idx, len(lines)):
            raw = lines[j]
            s = raw.strip()
            if not s:
                continue
            # 输入中的小时标记用于计算绝对时间，不直接透传
            m_add = re.match(r'^\[ADD\s+(\d+)\s+H\]$', s)
            if m_add:
                input_hour = int(m_add.group(1))
                continue

            # 匹配时间行，允许可选的显式小时
            m = re.match(r'^(?:((?:\d{1,2}):)?)(\d{2}):(\d{2})\.(\d{3})-(?:((?:\d{1,2}):)?)(\d{2}):(\d{2})\.(\d{3})\](.*)$', s)
            if not m:
                # 不是时间行，原样写出（保底）
                file.write(raw)
                continue

            # 提取开始与结束时间
            sh_opt = m.group(1)
            sm = int(m.group(2)); ss = int(m.group(3)); sms = int(m.group(4))
            eh_opt = m.group(5)
            em = int(m.group(6)); es = int(m.group(7)); ems = int(m.group(8))
            text = m.group(9).strip()

            sh = int(sh_opt[:-1]) if sh_opt else input_hour
            eh = int(eh_opt[:-1]) if eh_opt else input_hour

            # 绝对毫秒并加偏移
            start_abs = ((sh * 3600) + (sm * 60) + ss) * 1000 + sms + time_offset
            end_abs = ((eh * 3600) + (em * 60) + es) * 1000 + ems + time_offset
            if start_abs < 0: start_abs = 0
            if end_abs < 0: end_abs = 0

            # 计算新的小时与小时内时间
            def split_abs(ms):
                h = ms // 3600000
                rem = ms % 3600000
                m_ = rem // 60000
                s_ = (rem % 60000) // 1000
                ms_ = rem % 1000
                return int(h), int(m_), int(s_), int(ms_)

            sh2, sm2, ss2, sms2 = split_abs(start_abs)
            eh2, em2, es2, ems2 = split_abs(end_abs)

            # 如输出小时标记发生变化，则插入标记
            if output_hour is None or sh2 != output_hour:
                output_hour = sh2
                if output_hour > 0:
                    file.write(f"[ADD {output_hour} H]\n")

            # 输出压缩格式（仅分:秒.毫秒），保持 “-” 和 末尾 "]"
            file.write(f"{sm2:02}:{ss2:02}.{sms2:03}-{em2:02}:{es2:02}.{ems2:03}]{text}\n")

    print("时间轴调整完成，输出文件为 'cache/outputA3.midform'。")
except Exception as e:
    print(f"写入文件时出错: {e}")
    exit(1)
