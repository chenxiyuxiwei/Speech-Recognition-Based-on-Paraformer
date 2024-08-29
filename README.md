# Paraformer语音识别模型 & 业务场景应用

## 一、数据处理

### 1.1 数据清洗



### 1.2 数据准备

完成清洗后的excel文件为cleaned_data.excel，将其转化为微调模型所需要的csv、scp等格式文件。

- **excel2csv.py**

  将cleaned_data.excel文件中的 **无有效内容** 或 **空** 行进行删除，并将音频文本内容列提取出，删去其中所有标点符号，而仅保留文字部分。处理生成output_all.csv文件。

- **data_split.py**

  将output_all.csv文件划分为训练集、验证集与测试集，默认分别为train_all.csv、val_all.csv和test_all.csv。

- **data_preprocess.py**

  将csv文件转化为scp和txt文件。

  - txt文件展示

    ```text
    chunk3360 我这儿把电池放里面它怎么显示换电失败是怎么回事
    chunk1729 要不要我们就加微信什么之类的我们先检查一下电池
    chunk7188 我刚才有个寄存然后它显示失败了但是我现在人不在那边了
    chunk4930 说我租一个月的电池嘛然后到时候我用租电开到学校去那我一直把电池放到我车里面应该没事吧
    ......
    ```

  - scp文件展示

    ```text
    chunk3360 https://audio.yugu.net.cn/customer_audio/chunk3360.wav
    chunk1729 https://audio.yugu.net.cn/customer_audio/chunk1729.wav
    chunk7188 https://audio.yugu.net.cn/customer_audio/chunk7188.wav
    chunk4930 https://audio.yugu.net.cn/customer_audio/chunk4930.wav
    ......
    ```

- **选择将网页上的音频资源下载到本地的情况**

  - **download_wav.py**

    用于将网页上的音频资源下载到本地。

  - **path_http2local.py**

    将csv中的音频文件路径列，从 **http** 改为 **本地路径**。

    - **改前**

      ```text
      Audio:FILE,Text:LABEL
      https://audio.yugu.net.cn/customer_audio/chunk6155.wav,我 一 次 充 电 呢 我 扫 了 五 块 钱 但 是 他 没 用 完 他 就 充 到 两 块 九 毛 四 他 就 结 束 充 电 了 充 电 充 满 了 剩 下 的 钱 在 哪 里 呢
      https://audio.yugu.net.cn/customer_audio/chunk4684.wav,我 现 在 把 电 池 放 进 去 了 然 后 他 没 有 给 我 弄 出 来 新 的
      https://audio.yugu.net.cn/customer_audio/chunk2491.wav,我 电 池 还 了 之 后 他 不 给 我 电 池 不 开 那 怎 么 弄 啊
      https://audio.yugu.net.cn/customer_audio/chunk5357.wav,十 月 三 号 的 时 候 怎 么 在 支 付 宝 上 扣 了 五 百 块 钱 呢
      ......
      ```

    - **改后**

      ```text
      Audio:FILE,Text:LABEL
      E:\kechuang\yugu\paraformer\paraformer_finetune\mydata_2\test\wav\test\chunk6155.wav,我 一 次 充 电 呢 我 扫 了 五 块 钱 但 是 他 没 用 完 他 就 充 到 两 块 九 毛 四 他 就 结 束 充 电 了 充 电 充 满 了 剩 下 的 钱 在 哪 里 呢
      E:\kechuang\yugu\paraformer\paraformer_finetune\mydata_2\test\wav\test\chunk4684.wav,我 现 在 把 电 池 放 进 去 了 然 后 他 没 有 给 我 弄 出 来 新 的
      E:\kechuang\yugu\paraformer\paraformer_finetune\mydata_2\test\wav\test\chunk2491.wav,我 电 池 还 了 之 后 他 不 给 我 电 池 不 开 那 怎 么 弄 啊
      E:\kechuang\yugu\paraformer\paraformer_finetune\mydata_2\test\wav\test\chunk5357.wav,十 月 三 号 的 时 候 怎 么 在 支 付 宝 上 扣 了 五 百 块 钱 呢
      ......
      ```

      

  

  



