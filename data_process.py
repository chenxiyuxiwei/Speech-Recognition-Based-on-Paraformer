import os
import csv
import sys
import shutil

CUR_DIR = os.getcwd()

os_env = 'windows'      # 环境：windows / linux
is_local = False        # 本地 / 网页
dir_name = "mydata_2"
split_str = "\\" if os_env == "windows" else "/"
'''
    type                要处理的数据集类型，可以是train,val,test,分别代表训练、验证、测试集
    max_num             最大数据条数,如果为0则无限制
    csv_file            csv的文件路径名
    output_path         .scp和text及wav文件输出目录
    wav_parent_path     wav文件最终的输出父目录，比如最终微调的时候放到/home/data/目录下
'''
def process_data(type, max_num, csv_file, output_path, wav_parent_path=''):
    if type != "train" and type != "val" and type != "test":
        print("type is invalid,train or val or test is valid data")
        return

    data_path = os.path.basename(csv_file)

    if not os.path.exists(output_path):
        os.mkdir(output_path)

    # 写train_wav.scp
    wav_path = os.path.join(output_path, f"{type}_wav.scp")
    wav_file = open(wav_path, 'w', encoding='utf-8')

    # 写train_text.txt
    text_path = os.path.join(output_path, f"{type}_text.txt")
    text_file = open(text_path, 'w', encoding='utf-8')

    # 以UTF-8编码打开CSV文件
    with open(csv_file, mode='r', encoding='utf-8', newline='') as csvfile:
        # 创建csv.reader对象
        reader = csv.reader(csvfile)
        # 读取标题行
        headers = next(reader)
        print(headers)

        # 读取每一行
        index = 0
        for row in reader:
            print(row)
            index += 1
            audio_file = row[0]
            if is_local:
                if os_env == 'windows':
                    audio_file = audio_file.replace("/", "\\")
                elif os_env == 'linux':
                    audio_file = audio_file.replace("\\", "/")
            text = row[1].replace(" ", "")

            file_name_with_extension = os.path.basename(audio_file)
            file_name_without_extension, _ = os.path.splitext(file_name_with_extension)

            wav_file.write(f"{file_name_without_extension} {audio_file}\n")
            text_file.write(f"{file_name_without_extension} {text}\n")
            if max_num > 0 and index >= max_num:
                break

    wav_file.close()
    text_file.close()


if __name__ == "__main__":
    process_data("train", 20000,
                 os.path.join(CUR_DIR, dir_name, "train_all.csv"),
                 os.path.join(CUR_DIR, dir_name, "list"),
                 os.path.join(CUR_DIR, dir_name))
    process_data("val", 10000,
                 os.path.join(CUR_DIR, dir_name, "val_all.csv"),
                 os.path.join(CUR_DIR, dir_name, "list"),
                 os.path.join(CUR_DIR, dir_name))
    # process_data("val", 10000, "./data/speech_asr_aishell_devsets.csv", "FunASR-main/data/list", '/home/data/asr_finetune')
    # process_data("test", 5000, "./data/speech_asr_aishell_testsets.csv", "./data/list/",'/home/data/')
