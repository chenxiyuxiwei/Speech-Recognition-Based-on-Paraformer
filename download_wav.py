import pandas as pd
import requests
from tqdm import tqdm
import os

csv_path = 'mydata_2/test_all.csv'
local_path = 'mydata_2/test/wav/test'

# 读取CSV文件
df = pd.read_csv(csv_path)
url_column_name = 'Audio:FILE'
os.makedirs(local_path, exist_ok=True)

# 下载音频文件
for index, row in tqdm(df.iterrows(), total=df.shape[0]):
    url = row[url_column_name]

    # 获取文件名
    file_name = os.path.basename(url)

    # 生成本地文件路径
    local_file_path = os.path.join(local_path, file_name)

    # 下载音频文件
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(local_file_path, 'wb') as audio_file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    audio_file.write(chunk)

        print(f"Successfully downloaded {file_name}")

    except requests.exceptions.RequestException as e:
        print(f"Failed to download {file_name}. Error: {e}")

print("All downloads are completed.")