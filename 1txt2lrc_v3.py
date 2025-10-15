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

'''
以下是输入文件的样例：
00:00:00s
感谢观看哦~
00:00:30s
结束啦
00:59:51s
あたるあたるはそこはって気持ちいいよ
01:00:21s
おやすみなさい。
01:00:51s
どう?何か手に吹いてんの?
03:27:57s
谢谢你。

其中会有小时位。
在输出lrc文件的时候，希望lrc文件对小时进位。所以最终期望的输出文件是
[00:00.00] 感谢观看哦~
[00:30.00] 结束啦
[59:51.00] あたるあたるはそこはって気持ちいいよ
[01:00.21] おやすみなさい。
[01:00.51] どう?何か手に吹いてんの?
[03:27.57] 谢谢你。
'''

# 辅助函数：将时间从 '00:00:00s' 转为 '[hh:mm:ss.xx]' 格式
def convert_to_lrc_time(time_str):
    try:
        time_str = time_str.replace('s', '')  # 去掉 's'
        h, m, s = map(int, time_str.split(':'))  # 将时间分解为小时、分钟、秒并转换为整数
        
        # 计算总秒数
        total_seconds = h * 3600 + m * 60 + s  
        
        # 重新计算分钟和秒，处理进位
        minutes = total_seconds // 60
        seconds = total_seconds % 60

        # 生成毫秒部分，取整处理
        milliseconds = 0  # 在此处可以设置为你需要的毫秒值，比如 0
        
        # 添加进位处理逻辑
        '''
        检查分钟部分：
        - 如果时间格式的 [ 和 ] 之间只有一个 :，并且分钟部分大于等于60，
        - 这意味着时间戳未进位，需将分钟部分转为小时。
        - 此时在分钟部分前加个 : 并在前面输出小时。
        - 如果分钟部分小于60，则不需要添加小时和冒号，直接返回。
        '''
        if minutes >= 60:  # 如果分钟部分大于等于60
            hours = minutes // 60  # 计算小时
            minutes = minutes % 60  # 计算剩余分钟
            return f"[{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:02}]"  # 返回格式化的时间字符串
        else:
            return f"[{minutes:02}:{seconds:02}.{milliseconds:02}]"  # 返回格式化的时间字符串
        
    except ValueError:
        raise ValueError(f"时间格式错误：{time_str}")

# 从 input.txt 文件中读取字幕
input_data = read_input_file('input.txt')

# 用正则表达式匹配时间和字幕
pattern = re.compile(r'(\d{2}:\d{2}:\d{2}s)\s*\n([\s\S]+?)(?=\d{2}:\d{2}:\d{2}s|$)', re.DOTALL)
matches = pattern.findall(input_data)

# 生成LRC格式
lrc_lines = []
for time_str, subtitle in matches:
    lrc_time = convert_to_lrc_time(time_str)  # 转换时间格式
    lrc_lines.append(f"{lrc_time} {subtitle.strip()}")  # 添加空格以分隔时间和字幕

# 保存 LRC 文件
with open('output1.lrc', 'w', encoding='utf-8') as f:
    f.write("\n".join(lrc_lines))  # 将所有行写入文件

print("处理完成，生成了 output1.lrc 文件。")  # 提示完成
