import re

def remove_duplicates_from_lrc(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    processed_lines = []
    last_content = ""

    # 定义要删除的内容的正则表达式集合
    patterns_to_remove = {
        r'晚安.*',  # 示例：可以添加更多需要删除的正则表达式
        r'あ、あ、.*',  # 示例
        r'あああ.*',
        # 添加更多正则表达式
    }

    # 用于移除比较时的符号
    def clean_content(content):
        return re.sub(r'[{}，。~?!ー？！]', '', content)  # 移除指定符号

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

            # 检查内容是否匹配集合中的任何正则表达式
            if any(re.search(pattern, content) for pattern in patterns_to_remove):
                continue  # 如果匹配到集合中的正则表达式，跳过该行

            # 规则3：删除内容完全重复的上一行，忽略特定符号
            cleaned_content = clean_content(content)  # 清理后的内容
            if clean_content(last_content) == cleaned_content:
                continue  # 如果清理后的内容与上一行相同，跳过


            # 规则4：如果最后一个字符是中文逗号句号，删除句号
            if content.endswith('。'):
                content = content[:-1]  # 删除最后的句号
            if content.endswith('，'):
                content = content[:-1]  # 删除最后的逗号

            last_content = content  # 更新上一行内容
            processed_lines.append(f"{time_stamp} {content}")  # 添加原始内容

    # 写入到 output2.lrc 文件
    with open(output_file, 'w', encoding='utf-8') as f:
        for processed_line in processed_lines:
            f.write(processed_line + "\n")

# 使用函数处理文件
remove_duplicates_from_lrc('output1.lrc', 'output2.lrc')

print("处理完成，生成了 output2.lrc 文件。")
