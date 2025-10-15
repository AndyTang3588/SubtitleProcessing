import re

def remove_duplicates_from_lrc(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    processed_lines = []
    last_content = ""

    for line in lines:
        line = line.strip()
        if not line:  # 跳过空行
            continue

        # 匹配时间戳
        time_pattern = r'^\[(\d{1,2}):(\d{2})\.(\d{2})\]|\[(\d{1,2}):(\d{2}):(\d{2})\.(\d{2})\]'
        match = re.match(time_pattern, line)

        if match:
            # 提取时间戳
            time_stamp = line[:line.index(']') + 1]
            content = line[line.index(']') + 1:].strip()

            # 规则1：完全相同字符重复超过3次
            content = re.sub(r'(.)\1{3,}', r'\1\1\1', content)

            # 规则2：相同的2个字、3个字和4个字重复超过3次
            content = re.sub(r'(..)\1{3,}', r'\1\1\1', content)  # 2个字
            content = re.sub(r'(...)\1{3,}', r'\1\1\1', content)  # 3个字
            content = re.sub(r'(....)\1{3,}', r'\1\1\1', content)  # 4个字

            # 规则3：删除内容完全重复的上一行
            if last_content == content:
                continue  # 如果内容与上一行相同，跳过

            last_content = content
            processed_lines.append(f"{time_stamp} {content}")

    # 写入到 output2.lrc 文件
    with open(output_file, 'w', encoding='utf-8') as f:
        for processed_line in processed_lines:
            f.write(processed_line + "\n")

# 使用函数处理文件
remove_duplicates_from_lrc('output1.lrc', 'output2.lrc')

print("处理完成，生成了 output2.lrc 文件。")
