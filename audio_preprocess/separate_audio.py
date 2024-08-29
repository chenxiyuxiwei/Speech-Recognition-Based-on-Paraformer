import torch
from df.enhance import enhance, init_df
from df.utils import download_file
from df.io import load_audio, save_audio
import torchaudio

model_path = r"E:\kechuang\yugu\paraformer\paraformer_finetune\deepfilternet\models\DeepFilterNet3\DeepFilterNet3"
# 初始化模型
model, df_state, _ = init_df(default_model=model_path)  # Load default model

# 加载音频数据并进行预处理
print('Loading audio file...')
input_file = r"E:\kechuang\yugu\paraformer\paraformer_finetune\mydata\train\wav\train\chunk6268.wav"
out_dir = r"E:\kechuang\yugu\paraformer\paraformer_finetune\mydata\tmp\out1.wav"

audio, _ = load_audio(input_file, sr=df_state.sr())
# 使用模型进行语音增强
print('Processing...')
enhanced_audio = enhance(model, df_state, audio)

resampler = torchaudio.transforms.Resample(48000, 16000)
enhanced_audio = resampler(enhanced_audio)


# Save for listening
save_audio(out_dir, enhanced_audio, df_state.sr())
print(f'Enhanced audio has been saved to {out_dir}')

