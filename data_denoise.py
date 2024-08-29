import pandas as pd
import re
from tqdm import tqdm


def remove_consecutive_chinese_punctuation(text):
    # 中文标点符号的unicode范围
    chinese_punctuation = r'[，。？]'
    text = text.replace(" ", "")
    # 使用正则表达式替换连续的中文标点符号
    result = re.sub(f'({chinese_punctuation})+', r'\1', text)

    # 如果结果字符串的第一个字符是标点符号，则删除它
    if re.match(chinese_punctuation, result):
        result = result[1:]

    return result.replace(" ", "")


# 定义去除连续重复字词的函数
def clean_text_with_removals(text):
    # 定义无效词列表
    filler_words = ["我这边想问一下", "我想请问一下", "我想咨询一下", "我要问一下", "我想问一下", "我请问一下", "我咨询一下", "就我那个啥", "我那个啥", "我问一下",
                    "请问一下", "我想问下", "是这样的", "是这样啊", "对对对", "是这样", "问一下", "请问下", "对，", "对呀", "哎呀", "哎呦", "那个", "这个",
                    "就是", "你好", "您好", "美女", "我那", "对对", "我靠", "咳", "诶", "喂", "啊", "嗯", "呃", "哦", "哎", "唉", "额"]

    # 初始被去掉的词收集器
    removed_words = []

    # 处理去除特殊重复的需要保留的组合
    special_cases = {'了了': 'SPECIAL_DOUBLE_LE', 'PP': 'SPECIAL_PP', '谢谢': 'SPECIAL_DOUBLE_XIE'}
    for special, placeholder in special_cases.items():
        text = text.replace(special, placeholder)

    # 去除连续重复的字
    text = re.sub(r'(\w)\1+', r'\1', text)

    # 去除连续重复的词
    # text = re.sub(r'\b(\w+)\b(?:\s+\1\b)+', r'\1', text)
    # 使用正则表达式匹配连续重复的词
    pattern = r'\b(\w+)(\s+\1)+\b'
    # 使用re.sub替换掉重复的部分，只保留一个
    text = re.sub(pattern, r'\1', text, flags=re.IGNORECASE)

    # 处理无效词
    for filler in filler_words:
        # 找到并记录被去除的词
        matched = re.findall(f'{filler},?', text)
        removed_words.extend(matched)
        # 替换无效词和紧跟的逗号
        text = re.sub(f'{filler},?', '', text)

    # 去除连续重复的字
    text = re.sub(r'(\w)\1+', r'\1', text)

    # 去除连续重复的词
    # 使用正则表达式匹配连续重复的词
    pattern = r'\b(\w+)(\s+\1)+\b'
    # 使用re.sub替换掉重复的部分，只保留一个
    text = re.sub(pattern, r'\1', text, flags=re.IGNORECASE)

    # 恢复特殊情况
    for special, placeholder in special_cases.items():
        text = text.replace(placeholder, special)

    # 删除连续的中文标点符号
    text = remove_consecutive_chinese_punctuation(text)

    return text, removed_words


# 读取Excel文件
input_file = 'data.xlsx'
output_file = 'cleaned_data_3.xlsx'
column_name = '校对内容（标注内容、噪声文本）'

# 读取所需的列并创建新列
df = pd.read_excel(input_file, usecols=[column_name])

# 新建列用于存储去除的词
df['清理后'] = ''
df['去除的词'] = ''

# 对指定列进行清理
for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Processing"):
    original_text = row[column_name]
    original_text = str(original_text)
    if pd.isna(original_text) or original_text == '无有效内容':
        df.at[index, '清理后'] = original_text  # 保留原始内容
        df.at[index, '去除的词'] = ''  # 标记为空，表示没有进行处理
        continue
    cleaned_text, removed_words = clean_text_with_removals(original_text)
    df.at[index, '清理后'] = cleaned_text
    df.at[index, '去除的词'] = ', '.join(removed_words)

# 保存结果到新的Excel文件
df.to_excel(output_file, index_label='行号')

print(f"处理完成，结果已保存到 {output_file}")