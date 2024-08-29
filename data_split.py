import pandas as pd
from sklearn.model_selection import train_test_split

input_path = 'mydata_2/output_all.csv'  # 带划分数据
out_dir = 'mydata_2'                    # 划分后数据保存目录
train_ratio = 0.7                       # 训练集占比

out_names = ["train", "val", "test"]
out_path = [out_dir + "/" + out_names[i] + "_all.csv" for i in range(len(out_names))]

# 读取已处理的CSV文件
df = pd.read_csv(input_path)

column_name = 'Text:LABEL'

# 删除内容为空或内容为“无有效内容”的行
df = df[df[column_name].notna()]  # 删除空值行
df = df[df[column_name] != "无有效内容"]  # 删除内容为“无有效内容”的行

# 划分数据集
train_df, temp_df = train_test_split(df, test_size=1-train_ratio, random_state=42)  # 70% 训练，30% 临时集
val_df, test_df = train_test_split(temp_df, test_size=0.5, random_state=42)  # 50% 验证，50% 测试

# 将不同数据集保存为CSV文件
train_df.to_csv(out_path[0], index=False)
val_df.to_csv(out_path[1], index=False)
test_df.to_csv(out_path[2], index=False)

print("数据集已成功划分并保存为 'train.csv', 'val.csv', 'test.csv'.")