# coding:utf-8
import pyaudio
import wave
import numpy as np
from datetime import datetime

#録音の基本情報
chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
iDeviceIndex = 0 #デバイス番号は適宜確認
RECORD_SECONDS = 120

#録音開始の閾値
threshold = 0.3

p = pyaudio.PyAudio()

stream = p.open(format = FORMAT,
    channels = CHANNELS,
    rate = RATE,
    input = True,
    input_device_index = iDeviceIndex,
    frames_per_buffer = chunk
)

cnt = 0

while True:
    data = stream.read(chunk)
    x = np.frombuffer(data, dtype="int16") / 32768.0
    if x.max() > threshold:
        print("---------------------------------")
        print("ポケモンを　うけとって　います...")
        filename = "sine.wav"

        all = []
        all.append(data)
        for i in range(0, int(RATE / chunk * int(RECORD_SECONDS))):
            data = stream.read(chunk)
            all.append(data)
        data = b''.join(all)

        out = wave.open(filename,'w')
        out.setnchannels(CHANNELS)
        out.setsampwidth(2)
        out.setframerate(RATE)
        out.writeframes(data)
        out.close()

        cnt += 1
    if cnt > 0:
        break
    
stream.close()
p.terminate()