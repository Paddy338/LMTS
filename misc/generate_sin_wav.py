'''
本程序可以生成指定频率、指定时长的正弦波音频，保存为 .wav 格式。
'''
import math
import wave
import struct

SAMPLE_RATE = 44100    # 采样率
FREQ = 1000            # 1000Hz
DURATION = 1.0         # 1秒
AMPLITUDE = 30000      # 音量，范围0~32767，别拉满防止破音
CHANNELS = 1           # 单声道，足够提示音

# 计算总采样点数
total_samples = int(SAMPLE_RATE * DURATION)

# 打开wav写入
wf = wave.open("beep_1000hz.wav", 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(2) # 16bit PCM，2字节
wf.setframerate(SAMPLE_RATE)

# 逐点生成正弦波形
frames = b''
for i in range(total_samples):
    t = i / SAMPLE_RATE
    value = AMPLITUDE * math.sin(2 * math.pi * FREQ * t)
    # 转成16位有符号小端short
    packed = struct.pack('<h', int(value))
    frames += packed

wf.writeframes(frames)
wf.close()
print("√ 生成完毕")
