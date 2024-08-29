import librosa
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write


def reduce_noise(y, sr):
    # 使用Short-time Fourier Transform (STFT)将音频转换为频谱图
    stft = librosa.stft(y)
    stft_db = librosa.amplitude_to_db(abs(stft))

    # 计算频谱图中的噪声样本平均值
    noise_samples = stft_db[:, :int(sr * 0.1)]
    noise_profile = np.mean(noise_samples, axis=1)

    # 将噪声样本从整个谱图中减去
    reduced_noise_stft_db = stft_db - noise_profile[:, None]

    # 将处理完的频谱图转换回波形
    reduced_noise_stft = librosa.db_to_amplitude(reduced_noise_stft_db)
    y_reduced = librosa.istft(reduced_noise_stft)

    return y_reduced


# 读取音频文件
filename = r"E:\kechuang\yugu\paraformer\paraformer_finetune\mydata\train\wav\train\chunk6268.wav"  # 替换为你的音频文件路径
y, sr = librosa.load(filename, sr=None)

# 进行降噪处理
y_reduced = reduce_noise(y, sr)

# 保存处理后的音频文件
output_filename = r"E:\kechuang\yugu\paraformer\paraformer_finetune\mydata\tmp\out.wav"
write(output_filename, sr, y_reduced.astype(np.float32))

print(f'处理后的音频文件已保存为 {output_filename}')

