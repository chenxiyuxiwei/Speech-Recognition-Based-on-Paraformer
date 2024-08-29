import pandas as pd
import string

cleaned_data_path = 'mydata_2/cleaned_data.xlsx'
out_path = 'mydata_2/output_all.csv'

# 读取Excel文件的数据
raw_df = pd.read_excel(cleaned_data_path)
selected_column = ['音频', '校对内容（标注内容、噪声文本）']
updated_column = ['Audio:FILE', 'Text:LABEL']
df = raw_df[selected_column]

# 假设我们要处理的列名为 'text_column'
df = df.rename(columns={
    selected_column[0]: updated_column[0],  # 将 'OldColumn1' 修改为 'NewColumn1'
    selected_column[1]: updated_column[1]   # 将 'OldColumn2' 修改为 'NewColumn2'
})

# 删除内容为空或内容为“无有效内容”的行
df = df[df[updated_column[1]].notna()]  # 删除空值行
df = df[df[updated_column[1]] != "无有效内容"]  # 删除内容为“无有效内容”的行

# 定义要去除的标点符号：中文标点符号和英文标点符号
chinese_punctuation = "，。！？；：“”‘’（）"
english_punctuation = string.punctuation  # 英文标点符号列表

# 创建一个翻译表，用于将标点符号映射为空字符
trans_table = str.maketrans("", "", chinese_punctuation + english_punctuation)


# 定义一个去除标点符号并添加间隔的函数
def process_text(text):
    text = str(text)
    # 使用翻译表去除标点符号
    text = text.translate(trans_table)

    # 在每个汉字之间添加空格
    text = ' '.join(text)

    return text

# 对指定列应用处理函数
df[updated_column[1]] = df[updated_column[1]].apply(process_text)

# 将处理后的数据保存为CSV文件
df.to_csv(out_path, index=False)