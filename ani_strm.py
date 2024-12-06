#!/usr/bin/env python3
import os
import re
from urllib.parse import unquote, urlparse, urlunparse, parse_qs, urlencode
import logging
import time

# 配置日志记录，使用相对路径记录日志文件，确保在不同系统中可正常创建和写入
logging.basicConfig(filename=os.path.join(os.getcwd(),'script.log'), level=logging.INFO,
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
    need_decode = False
    for line in lines:
        if '%' in line:
            need_decode = True
            break
    if need_decode:
        for line in lines:
            try:
                decoded_line = unquote(line)
                decoded_lines.append(decodedLine)
            except Exception as e:
                print(f"对以下内容解码失败: {line.strip()}，错误信息: {e}")
                logging.error(f"解码错误: {e} - 行内容: {line.strip()}")
    else:
        decoded_lines = lines
    return decoded_lines

def replace_view_query_param(url):
    """
    将 URL 中的?a=view 替换为?d=true
    :param url: 输入的 URL
    :return: 处理后的 URL
    """
    if '?a=view' in url:
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        query_params.pop('a', None)
        query_params['d'] = ['true']
        new_query = urlencode(query_params, doseq=True)
        url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, new_query, parsed_url.fragment))
    return url

def process_lines(lines):
    """
    处理行内容，确保?a=view 的处理方式为替换为?d=true
    :param lines: 解码后的行列表
    :return: 处理后的行列表
    """
    processed_lines = []
    for line in lines:
        processed_line = replace_view_query_param(line)
        processed_lines.append(processed_line)
    return processed_lines

def create_strm_files(lines):
    """
    根据处理后的行内容创建.strm 文件，并按番名分类保存
    :param lines: 处理后的行列表
    """
    # 获取当前执行目录，使用绝对路径确保在不同系统中准确找到工作目录
    current_dir = os.path.abspath(os.getcwd())
    print("当前脚本执行目录为:", current_dir)
    # 处理解码并处理后的内容，创建.strm 文件
    print(f"共读取到 {len(lines)} 行内容，开始创建.strm 文件...")
    for line in lines:
        # 查找[ANi]和.mp4的位置
        start_index = line.find("[ANi] ") + 6
        end_index = line.find(".mp4")
        # 提取文件名部分，过滤非法字符
        file_name = re.sub(r'[\\/:"*?<>|]', '', line[start_index:end_index])
        # 提取番名
        anime_name = line[start_index:line.find(" - ")].strip()
        # 创建番名对应的目录，使用绝对路径拼接目录名
        anime_dir = os.path.join(current_dir, anime_name)
        if not os.path.exists(anime_dir):
            os.makedirs(anime_dir)
        # 创建 strm 文件并写入内容
        try:
            start_time = time.time()
            with open(os.path.join(anime_dir, file_name + '.strm'), 'w') as strm_file:
                strm_file.write(line.strip())
            end_time = time.time()
            print(f"成功创建 {file_name}.strm 文件并写入内容，耗时: {end_time - start_time:.4f} 秒。")
            logging.info(f"成功创建 {file_name}.strm 文件，耗时: {end_time - start_time:.4f} 秒")
        except Exception as e:
            print(f"创建 {file_name}.strm 文件时出错: {e}")
            logging.error(f"创建 {file_name}.strm 文件出错: {e}")

def generate_addresses(address, num_lines, output_file):
    """
    生成地址行并写入文件
    :param address: 地址示例
    :param num_lines: 生成的行数
    :param output_file: 输出文件名
    """
    with open(output_file, 'w') as file:
        for i in range(num_lines):
            parts = address.split(' - ')
            episode_number = int(parts[1].split(' ')[0]) + i
            new_episode_number = f"{episode_number:02}"
            new_address = f"{parts[0]} - {new_episode_number} {' '.join(parts[1].split(' ')[1:])}"
            file.write(new_address + '\n')
            logging.info(f"写入地址到文件: {new_address}")

def analyze_addresses(input_file):
    """
    分析地址文件中的内容（这里主要是为了与原脚本结构保持一致，可根据实际需求调整功能）
    """
    try:
        with open(input_file, 'r') as file:
            for line in file:
                parts = line.split(' - ')
                episode_number = parts[1].split(' ')[0]
                print(f"地址: {line.strip()}")
                print(f"集数: {episode_number}")
    except FileNotFoundError:
        print("文件不存在，请先生成地址文件。")

def get_positive_integer_input(prompt):
    """
    获取正整数输入
    :param prompt: 提示信息
    :return: 正整数输入值
    """
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                print("请输入正整数，您输入的是负数或零，请重新输入。")
            else:
                return value
        except ValueError:
            print("请输入有效的正整数，您输入的不是数字，请重新输入。")

def process_url(url):
    """
    处理 URL，包括解码和替换查询参数（如果需要）
    :param url: 输入的 URL
    :return: 处理后的 URL
    """
    if '%' in url:
        url = unquote(url)
    url = replace_view_query_param(url)
    return url

def main():
    # 生成地址部分
    address_format_prompt = "请按照以下格式输入地址示例：[团队名] <番名(中文)> - <集数> [<解像度>][<来源>][<获取方法>][<音頻格式> <影像格式>][<字幕语言>].[副檔名]\n"
    address_format_prompt += "例如：https://地址/路径/[ANi] 火影忍者 - 01 [1080P][Baha][WEB-DL][AAC AVC][CHT].mp4\n"
    address = input(address_format_prompt)
    address = process_url(address)
    num_lines_prompt = "请输入需要生成的行数，默认为总行数，将以示例中的集数往上递增："
    num_lines = get_positive_integer_input(num_lines_prompt)
    output_file = "output.txt"
    generate_addresses(address, num_lines, output_file)
    analyze_addresses(output_file)
    # 处理生成的 output.txt（即作为 input_video_urls.txt）
    input_file_path = os.path.join(os.getcwd(), output_file)
    if not os.path.exists(input_file_path):
        print("未找到 output.txt 文件，生成地址部分可能出现问题，请检查后重新运行脚本。")
        logging.error("output.txt 文件不存在，生成地址部分出错")
        return
    with open(input_file_path, 'r', encoding='utf-8') as f:
        original_lines = f.readlines()
    decoded_lines = decode_lines(original_lines)
    if not decoded_lines:
        print("由于所有行解码均失败，无法继续创建.strm 文件，请检查 output.txt 内容。")
        logging.error("所有行解码失败，无法继续创建.strm 文件")
        return
    processed_lines = process_lines(decoded_lines)
    with open(input_file_path, 'w', encoding='utf-8') as f:
        f.writelines(processed_lines)
    print("已完成对 output.txt 内容中'?a=view'的处理并保存。")
    choice_prompt = "是否生成.strm 文件？(y/n)：生成.strm 文件可以便于MoviePilot的重命名、刮削和整理\n"
    choice = validate_user_input(choice_prompt, ['y', 'n'])
    if choice == 'y':
        create_strm_files(processed_lines)
    elif choice == 'n':
        print("已取消创建.strm 文件，脚本退出。")
        logging.info("用户取消创建.strm 文件")

if __name__ == "__main__":
    main()
