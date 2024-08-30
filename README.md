# Paraformer语音识别模型 & 业务场景应用

## 一、数据准备

### 1.1 语音数据类别标注

在理解和熟悉各预定义类别所描述范围的基础上，对语音数据进行人工打标签。

### 1.2 标注文本噪声清洗

利用[Python脚本](https://github.com/chenxiyuxiwei/Speech-Recognition-Based-on-Paraformer/blob/main/data_denoise.py)初步去除文本中的连续重复字词和与业务场景语义无关的内容，并结合人工检查完善校对与噪声清洗工作。脚本中：

- 预定义了语音中常出现的与业务问题语义无关的字词，在标注文本中过滤掉这一些无效字词。
- 删除说话者口吃或思考造成的连续重复字词。
- 确保标点符号不会出现在句首。

### 1.3 微调用数据集准备

#### 1.3.1 提取特定列生成csv文件

从经过校对和清洗后的语音数据标注文件`cleaned_data.xlsx`中提取出**音频文件路径**和**校对文本内容**两列，将无有效内容的音频所在行滤除，将文本内容一列中所有标点符号去除，且使得每个字符(汉字、数字、英文字母)之间间隔一个空格符，将excel文件转化为csv文件`output_all.csv`。脚本为[excel2csv.py](https://github.com/chenxiyuxiwei/Speech-Recognition-Based-on-Paraformer/blob/main/excel2csv.py)。
| Audio:FILE                                             | Text:LABEL                                                   |
| ------------------------------------------------------ | ------------------------------------------------------------ |
| https://audio.yugu.net.cn/customer_audio/chunk2332.wav | 就 是 这 个 充 电 的 它 老 是 自 己 断  了 然 后 这 个 费 用 是 不 是 没 有 退 还 呀 |
| https://audio.yugu.net.cn/customer_audio/chunk2333.wav | 我 这 边 换 电 然 后 的 话 刚 才 我 是 换 了 一 个 四 十 八 伏 的 然 后 现 在  我 就 到 了 那 充 电 柜 这 边 我 那 个 六 十 伏 的 它 充 满 了 麻 烦 你 帮 我 开 一 下 可 以 吗 |
| https://audio.yugu.net.cn/customer_audio/chunk2334.wav | 我 就 你 这 个 李 宁 新 天 地 这 里 的  换 电 站 转 了 一 圈 没 看 到 在 哪 里 在 地 下 室 吗 |
| https://audio.yugu.net.cn/customer_audio/chunk2336.wav | 我 在 你 这 我 是 否 有 个 电 池 在 你 们 那 逾 期 了 逾 期 了 |

#### 1.3.2 数据集划分

将数据集划分为训练集、验证集和测试集，分别为`train_all.csv`、`val_all.csv`和`test_all.csv`，保存目录为`data`，后续需要自行转移到`FunASR-main/data`路径下。脚本为[data_split.py](https://github.com/chenxiyuxiwei/Speech-Recognition-Based-on-Paraformer/blob/main/data_split.py)。

#### 1.3.3 生成scp和txt文件

通过`train_all.csv`文件和`val_all.csv`文件分别生成`train_text.txt`、`train_wav.scp`和`val_text.txt`、`val_wav.scp`文件。脚本为[data_process.py](https://github.com/chenxiyuxiwei/Speech-Recognition-Based-on-Paraformer/blob/main/data_process.py)。

- `train_text.txt`文件展示：
```text
chunk6536 我这个退电他怎么是寄存啊
chunk3795 我就电池卡在里面了
chunk2460 我刚才换个电池它里面百分之五十个电我都再换怎么换不起来这什么情况
chunk5035 我在这里换电然后取电池显示一个换电失败未知换电站无法取电
chunk3285 哦免押里面要选择退押金是吧
chunk5182 我为啥这锂换电使使怎么就突然间没电了系统显示上摇一摇完它就来电呢
......
```
- `train_wav.scp`文件展示：
```text
chunk6536 https://audio.yugu.net.cn/customer_audio/chunk6536.wav
chunk3795 https://audio.yugu.net.cn/customer_audio/chunk3795.wav
chunk2460 https://audio.yugu.net.cn/customer_audio/chunk2460.wav
chunk5035 https://audio.yugu.net.cn/customer_audio/chunk5035.wav
chunk3285 https://audio.yugu.net.cn/customer_audio/chunk3285.wav
chunk5182 https://audio.yugu.net.cn/customer_audio/chunk5182.wav
chunk2523 https://audio.yugu.net.cn/customer_audio/chunk2523.wav
......
```

#### 1.3.4 生成jsonl文件

通过`scp2jsonl`命令行工具，将`train_text.txt`、`train_wav.scp`和`val_text.txt`、`val_wav.scp`文件分别处理得到`train.jsonl`和`val_jsonl`文件。无需手动执行该命令，因为在执行命令`bash finetune.sh`时会自动执行。

- jsonl文件展示

```json
{"key": "chunk4684", "source": "https://audio.yugu.net.cn/customer_audio/chunk4684.wav", "source_len": 54, "target": "我现在把电池放进去了然后他没有给我弄出来新的", "target_len": 22}
{"key": "chunk5381", "source": "https://audio.yugu.net.cn/customer_audio/chunk5381.wav", "source_len": 54, "target": "就是刚刚这个这锂换电啊就是刚刚我不是要退电池嘛然后嗯退错了就是我把电池安进去了然后那个新的出来了但是我又把它合上了现在打不开了怎么办", "target_len": 66}
{"key": "chunk5328", "source": "https://audio.yugu.net.cn/customer_audio/chunk5328.wav", "source_len": 54, "target": "客服在东莞的话是在哪个城市的", "target_len": 14}
{"key": "chunk6298", "source": "https://audio.yugu.net.cn/customer_audio/chunk6298.wav", "source_len": 54, "target": "我现在在这换电然后那个租车的说是什么线坏了说一会儿掉个线让我又怎么弄的没弄明白怎么回事儿", "target_len": 44}
{"key": "chunk4820", "source": "https://audio.yugu.net.cn/customer_audio/chunk4820.wav", "source_len": 54, "target": "我刚才找的一个取那个线材听见响了一下怎么不知道在哪取了", "target_len": 27}
```

1.3 模型微调
1.3.1 模型部署
- 部署环境：
  - RTX 4090 (须保证Pytorch版本为2.0.0及以上)
  - Linux Ubantu20.04，Python 3.8，Cuda 11.8，Pytorch 2.0.0
- 使用git clone https://github.com/alibaba-damo-academy/FunASR.git将Paraformer模型项目下载到本地。
  - FunASR-main/examples/industrial_data_pretraining路径下的 paraformer 和 paraformer_streaming 目录分别对应离线和流式模型，通过运行目录下的finetune.sh脚本启动对应模型的微调。
  - FunASR-main/data目录用于存放微调数据集，包括训练集和验证集所对应的scp文件和txt文件。
1.3.2 预训练权重部署
将模型预训练权重文件下载到本地。相比于执行微调后将模型自动下载在固定路径，事先下载到本地能够更方便地查看和修改超参数配置文件config.yaml中的内容。
- 下载方式：
  离线模型：git clone https://www.modelscope.cn/iic/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch.git
  流式模型：git clone https://www.modelscope.cn/iic/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-online.git
- 在finetune.sh文件中设置模型文件路径：(以离线模型为例)
  自动下载：model_name_or_model_dir="iic/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch"
  手动下载：model_name_or_model_dir="path/to/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch"
1.3.3 超参数设置
微调过程涉及超参数可在finetune.sh或权重目录下的config.yaml中进行设置。
默认采用超参数配置如下：
暂时无法在飞书文档外展示此内容
1.3.4 音频预处理
- 利用实时语音增强和降噪的深度学习框架 DeepFilterNet 对音频数据进行预处理，通过去除语音中咨询者以外人声等噪声数据和锐化咨询者的人声，提升后续语音识别模型对音频内容的识别效果。
  DeepFilterNet安装方式：pip install deepfilternet 
- 将音频预处理操作整合到Paraformer模型微调框架中。在datasets.py脚本中加载数据集中单个音频文件时，利用预训练的deepfilternet模型对音频数据进行去噪、增强处理，并根据音频采样率执行重采样操作。
- 注：这里的datasets.py脚本来自于通过pip下载得到的funasr项目，而非通过git手动下载到本地的funasr。
  路径为/.../FunASR-main/funasr/datasets/audio_datasets/datasets.py。
1.3.5 微调执行
- 终端执行指令：bash finetune.sh。
- 执行finetune.sh后，首先执行scp2jsonl文件，将训练集与验证集scp、txt文件转化为jsonl文件。
  jsonl文件展示：
{"key": "chunk6400", "source": "https://audio.yugu.net.cn/customer_audio/chunk6400.wav", "source_len": 54, "target": "我昨天我的电池被别人给盗了然后我就联系你们客服了现在拿我电池人他联系我他一直让我给他提供验证码我就没提供给他我想知道我账号现在有什么风险", "target_len": 68}
{"key": "chunk7292", "source": "https://audio.yugu.net.cn/customer_audio/chunk7292.wav", "source_len": 54, "target": "麻烦你这边帮我看一下我那块电瓶的活动轨迹", "target_len": 20}
- 在finetune.sh一系列超参数的设置条件下，执行train_ds.py脚本。
