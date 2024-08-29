import pandas as pd
import os

CUR_DIR = os.getcwd()
os_env = 'windows'      # 环境：windows / linux
dir_name = "mydata_2"
split_str = "\\" if os_env == "windows" else "/"

csv_names = ["test", "test", "test"]
# 使用示例
csv_files = [os.path.join(CUR_DIR, dir_name, f'{csv_names[i]}_all.csv') for i in range(len(csv_names))]                 # 输入的CSV文件
local_dirs = [os.path.join(CUR_DIR, dir_name, csv_names[i], "wav", csv_names[i]) for i in range(len(csv_names))]    # 音频文件保存的本地目录
url_column = 'Audio:FILE'  # 存储下载网址的列名
output_files = [os.path.join(CUR_DIR, dir_name, f'{csv_names[i]}_local.csv') for i in range(len(csv_names))]        # 输出的CSV文件名

def update_csv_with_local_paths(csv_file, local_directory, url_column, output_csv):
    # 读取CSV文件
    df = pd.read_csv(csv_file)

    # 检查local_directory是否存在
    if not os.path.exists(local_directory):
        raise FileNotFoundError(f"The directory {local_directory} does not exist")

        # 替换URL为本地路径
    for index, row in df.iterrows():
        url = row[url_column]

        # 获取文件名
        file_name = os.path.basename(url)

        first_dir = url.split("/")[0]

        # 生成本地文件路径
        local_file_path = os.path.join(local_directory, file_name)

        # 检查本地文件是否存在
        if os.path.exists(local_file_path):
            # 替换URL为本地路径
            df.at[index, url_column] = local_file_path
        else:
            print(f"Warning: File {file_name} does not exist in the directory {local_directory}")

            # 保存更新后的CSV文件
    df.to_csv(output_csv, index=False)

    print(f"CSV file has been updated and saved as {output_csv}")

for i in range(len(csv_names)):
    if not os.path.exists(local_dirs[i]):
        os.makedirs(local_dirs[i], exist_ok=True)
    update_csv_with_local_paths(csv_files[i], local_dirs[i], url_column, output_files[i])
