#!/usr/bin/env python3
import os
import re
from urllib.parse import unquote
import logging

# 配置日志记录
logging.basicConfig(filename='script.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def validate_user_input(prompt, valid_choices):
    """
    验证用户输入是否在给定的有效选择范围内
    :param prompt: 提示信息
    :param valid_choices: 有效选择列表
    :return: 用户输入的有效选择
    """
    while True:
        choice = input(prompt).lower()
        if choice in valid_choices:
            return choice
        else:
            print(f"无效的输入，请输入 {', '.join(valid_choices)} 中的一个。")
            logging.warning(f"用户输入了无效的选择: {choice}")

def decode_lines(lines):
    """
    对给定的行列表进行解码操作
    :param lines: 原始行列表
    :return: 解码后的行列表
    """
    decoded_lines = []
    for line in lines:
        try:
            decoded_line = unquote(line)
            decoded_lines.append(decoded_line)
        except Exception as e:
            print(f"对以下内容解码失败: {line.strip()}，错误信息: {e}")
            logging.error(f"解码错误: {e} - 行内容: {line.strip()}")
    return decoded_lines

def process_lines(lines):
    """
    处理行内容，删除"?a=view"字符串
    :param lines: 解码后的行列表
    :return: 处理后的行列表
    """
    processed_lines = []
    for line in lines:
        if "?a=view" in line:
            line = line.replace("?a=view", "")
        processed_lines.append(line)
    return processed_lines

def create_strm_files(lines):
    """
    根据处理后的行内容创建.strm文件
    :param lines: 处理后的行列表
    """
    # 获取当前执行目录
    current_dir = os.getcwd()
    print("当前脚本执行目录为:", current_dir)

    # 处理解码并处理后的内容，创建.strm文件
    print(f"共读取到 {len(lines)} 行内容，开始创建.strm文件...")
    for line in lines:
        # 查找[ANi]和.mp4的位置
        start_index = line.find("[ANi] ") + 6
        end_index = line.find(".mp4")
        # 提取文件名部分，过滤非法字符
        file_name = re.sub(r'[\\/:"*?<>|]', '', line[start_index:end_index])
        # 创建strm文件并写入内容
        try:
            with open(os.path.join(current_dir, file_name + '.strm'), 'w') as strm_file:
                strm_file.write(line.strip())
            print(f"成功创建 {file_name}.strm文件并写入内容。")
            logging.info(f"成功创建 {file_name}.strm文件")
        except Exception as e:
            print(f"创建 {file_name}.strm文件时出错: {e}")
            logging.error(f"创建 {file_name}.strm文件出错: {e}")

def main():
    # 检查 input_video_urls.txt 是否存在
    input_file_path = os.path.join(os.getcwd(), 'input_video_urls.txt')
    if not os.path.exists(input_file_path):
        print("未找到 input_video_urls.txt 文件，将创建该文件，请编辑配置后重新运行脚本。")
        logging.info("input_video_urls.txt 文件不存在，已创建")
        # 创建 input_video_urls.txt 文件
        with open(input_file_path, 'w') as f:
            pass
        return

    # 打开 input_video_urls.txt 文件用于读取原始内容
    with open(input_file_path, 'r', encoding='utf-8') as f:
        original_lines = f.readlines()

    # 对 input_video_urls.txt 的内容进行解码处理
    decoded_lines = decode_lines(original_lines)
    if not decoded_lines:
        print("由于所有行解码均失败，无法继续创建.strm文件，请检查 input_video_urls.txt 内容。")
        logging.error("所有行解码失败，无法继续创建.strm文件")
        return

    # 对解码后的每行内容判断是否含有"?a=view"，有的话删掉它
    processed_lines = process_lines(decoded_lines)

    # 打开 input_video_urls.txt 文件用于写入处理后的内容
    with open(input_file_path, 'w', encoding='utf-8') as f:
        f.writelines(processed_lines)

    print("已完成对 input_video_urls.txt 内容中'?a=view'的处理并保存。")

    # 询问是否生成strm文件
    choice = validate_user_input("是否生成strm文件？(y/n)：", ['y', 'n'])
    if choice == 'y':
        create_strm_files(processed_lines)
    elif choice == 'n':
        print("已取消创建strm文件，脚本退出。")
        logging.info("用户取消创建strm文件")

if __name__ == "__main__":
    main()
