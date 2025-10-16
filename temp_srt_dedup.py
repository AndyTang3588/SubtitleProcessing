import re

def remove_duplicates_from_srt(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 分割SRT内容为单独的块
    srt_blocks = []
    blocks = content.strip().split('\n\n')
    
    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) >= 3:  # 序号、时间、文本
            srt_blocks.append(lines)

    processed_blocks = []
    last_content = ""

    # 定义要删除的内容的正则表达式集合
    patterns_to_remove = {
        r'晚安.*',
        r'あ、あ、.*',
        r'あああ.*',
    }

    # 用于移除比较时的符号
    def clean_content(content):
        return re.sub(r'[{}，。~?!ー？！]', '', content)

    for i, block in enumerate(srt_blocks, 1):
        if len(block) < 3:
            continue
            
        sequence = block[0]
        time_line = block[1]
        text_content = ' '.join(block[2:])
        
        # 规则1：完全相同字符重复超过3次
        text_content = re.sub(r'(.)\1{3,}', r'\1\1\1', text_content)

        # 规则2：相同的2个字、3个字和4个字重复超过3次
        text_content = re.sub(r'(..)\1{3,}', r'\1\1\1', text_content)
        text_content = re.sub(r'(...)\1{3,}', r'\1\1\1', text_content)
        text_content = re.sub(r'(....)\1{3,}', r'\1\1\1', text_content)

        # 检查内容是否匹配集合中的任何正则表达式
        if any(re.search(pattern, text_content) for pattern in patterns_to_remove):
            continue

        # 规则3：删除内容完全重复的上一行，忽略特定符号
        cleaned_content = clean_content(text_content)
        if clean_content(last_content) == cleaned_content:
            continue

        # 规则4：如果最后一个字符是中文逗号句号，删除句号
        if text_content.endswith('。'):
            text_content = text_content[:-1]
        if text_content.endswith('，'):
            text_content = text_content[:-1]

        last_content = text_content
        
        # 重新构建SRT块
        new_block = [str(len(processed_blocks) + 1), time_line, text_content]
        processed_blocks.append(new_block)

    # 写入到 output2.srt 文件
    with open(output_file, 'w', encoding='utf-8') as f:
        for block in processed_blocks:
            f.write('\n'.join(block))
            f.write('\n\n')

# 使用函数处理文件
remove_duplicates_from_srt('cache/output1.srt', 'cache/output2.srt')
print("处理完成，生成了 cache/output2.srt 文件。")
