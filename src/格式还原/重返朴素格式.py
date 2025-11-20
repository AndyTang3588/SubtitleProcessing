import os
import shutil
import re

def backup_file(original_file, backup_prefix='备份_反朴_', extension='.lrc'):
    """
    创建一个备份文件，命名为 backup_prefix + 两位数字 + extension，例如 备份01.lrc。
    如果备份文件已存在，则递增数字直到找到一个未被占用的文件名。
    """
    counter = 1
    while True:
        backup_filename = f"{backup_prefix}{counter:02}{extension}"
        if not os.path.exists(backup_filename):
            try:
                shutil.copyfile(original_file, backup_filename)
                print(f"已创建备份文件: {backup_filename}")
                break
            except Exception as e:
                print(f"备份文件失败: {e}")
                exit(1)
        counter += 1

def process_lrc(input_file, output_file):
    """
    处理 .lrc 文件，将其转换为另一种格式，并在处理前创建备份。
    """
    # 创建备份
    if os.path.exists(input_file):
        backup_file(input_file)
    else:
        print(f"输入文件 '{input_file}' 未找到，无法创建备份。")
        return

    # 修改后的正则表达式，支持 [mm:ss.xx] 和 [hh:mm:ss.xx] 格式
    time_pattern = re.compile(r'\[(?:(\d{2}):)?(\d{2}):(\d{2})(?:\.\d+)?\]')
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"输入文件 '{input_file}' 未找到。请确保文件存在并路径正确。")
        return
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return
    
    output_lines = []
    
    for idx, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue  # 跳过空行
        time_matches = time_pattern.findall(line)
        
        if time_matches:
            # 假设每行只有一个时间轴，如果有多个时间轴，可以根据需求调整
            for match in time_matches:
                hours, minutes, seconds = match
                hours = hours if hours else '00'
                formatted_time = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}s"
                
                # 获取字幕内容：去除所有时间轴后剩余的部分
                subtitle = time_pattern.sub('', line).strip()
                
                if subtitle:
                    output_lines.append(f"{formatted_time}\n{subtitle}")
                else:
                    output_lines.append(f"{formatted_time}")
        else:
            # 如果行中没有时间轴，可以选择忽略或处理
            print(f"第 {idx + 1} 行未找到时间轴，内容: {line}")
    
    if output_lines:
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                # 使用换行符连接所有输出内容
                f.write('\n'.join(output_lines))
            print(f"处理完成，输出文件为 '{output_file}'")
        except Exception as e:
            print(f"写入文件时出错: {e}")
    else:
        print("没有匹配到任何时间轴，输出文件未生成。")

if __name__ == "__main__":
    # 调用函数处理文件
    input_file = 'output3.lrc'
    output_file = 'output3朴素.txt'
    process_lrc(input_file, output_file)
