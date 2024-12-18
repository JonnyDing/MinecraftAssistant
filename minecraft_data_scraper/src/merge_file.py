import os


def merge_txt_files(input_folder, output_folder, files_per_merge=25):
    # 检查输出文件夹是否存在，不存在则创建
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 获取文件夹中所有txt文件
    txt_files = [f for f in os.listdir(input_folder) if f.endswith('.txt')]
    txt_files.sort()  # 按照文件名排序

    total_files = len(txt_files)
    if total_files == 0:
        print("文件夹中没有TXT文件。")
        return

    # 分批合并
    for i in range(0, total_files, files_per_merge):
        batch_files = txt_files[i:i + files_per_merge]
        output_file = os.path.join(output_folder, f'merged_{i // files_per_merge + 1}.txt')

        with open(output_file, 'w', encoding='utf-8') as outfile:
            for file in batch_files:
                file_path = os.path.join(input_folder, file)
                with open(file_path, 'r', encoding='utf-8') as infile:
                    outfile.write(infile.read())
                    outfile.write('\n')  # 添加分隔符或换行符

        print(f"已生成文件: {output_file}")


# 示例：输入文件夹和输出文件夹路径
input_folder = '../data/resource_data'  # 替换为你的输入文件夹路径
output_folder = '../data/resource_process_data'  # 替换为你的输出文件夹路径

merge_txt_files(input_folder, output_folder)
