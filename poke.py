# coding:utf-8
import cv2
import sys
import pygame.mixer
from scipy.io import wavfile as sciio
import numpy as np
import wave
from time import sleep

pygame.mixer.init(frequency = 44100)

#画像の読み込みとグレースケール化,画像は引数指定
argvs = sys.argv
filename = argvs[1]

with open('list.txt', 'r') as list:
    pokeList = list.read()
pokeList = pokeList.split('\n')

name = ""
voice = ""
if filename == pokeList[0]:
    name = "フシギダネ"
    voice = "audio/voice/001.wav"
elif filename == pokeList[1]:
    name = "コイキング"
    voice = "audio/voice/129.wav"
elif filename == pokeList[2]:
    name = "リザードン"
    voice = "audio/voice/006.wav"
elif filename == pokeList[3]:
    name = "ニャース"
    voice = "audio/voice/052.wav"
elif filename == pokeList[4]:
    name = "ピカチュウ"
    voice = "audio/voice/025.wav"
elif filename == pokeList[5]:
    name = "トランセル"
    voice = "audio/voice/011.wav"
elif filename == pokeList[6]:
    name = "トレーナー"
elif filename == pokeList[7]:
    name = "ゼニガメ"
    voice = "audio/voice/007.wav"
else:
    name = "けつばん"
    filename = "lost"
    voice = "audio/voice/lost.wav"

img = cv2.imread("img/resource/" + filename + ".png")
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

#正弦波を生成する部分
def create_sine_wave(amp, freqList, fs, sum_length):
    """
    sin波作成
    ---------
    amp:        振幅
    freqList:   基本周波数リスト
    fs:         サンプリング周波数
    sum_length: 合計長（秒）
    ---------
    return:     int16型のnumpy配列
    """

    # 音量パラメータは1（最大）～0（最小）
    if amp >= 1.0:
        amp = 1.0
    elif amp <= 0.0:
        amp = 0

    # 周波数ごとに振幅[-32768～32767]のsin波作成
    #length = sum_length / len(freqList) # 1周波数種当たりの長さ
    #n_all_frames = length * fs     # 総フレーム巣数
    n_all_frames = int(sum_length * fs / len(freqList))
    datas = []
    
    for x in range(0, len(freqList), 2):
        #print("test:{0}".format(f0))
        data1 = [amp * np.sin(2 * np.pi * freqList[x] * i / fs) for i in range(n_all_frames)]
        data2 = [amp * np.sin(2 * np.pi * freqList[x+1] * i / fs) for i in range(n_all_frames)]
        # [-32768, 32767]の整数値に変換(int16値に変換)
        data1 = [x*32767 for x in data1]
        data2 = [x*32767 for x in data2]
        data = []
        [data.append(data1[i]+data2[i]) for i in range(n_all_frames)]
        [datas.append(x) for x in data]

    datas = np.asarray(datas, dtype='int16')

    return datas


#グレースケール化した時に、４階調にするには誤差が出てしまうので、それも込みで処理

#4桁に直す前の配列
freq_before = []

#それぞれの値に対して周波数を設定
for i in range(60):
    for j in range(60):
        if 0 <= gray[i, j] < 63:
            freq_before.append(1)
        elif 63 <= gray[i, j] < 128:
            freq_before.append(2)
        elif 128 <= gray[i, j] < 192:
            freq_before.append(3)
        elif 192 <= gray[i, j] <= 255:
            freq_before.append(4)

#3桁に直す配列
#0.1秒で一つのデータを伝送するとフレーム数は4410に落ちるので、インデックスも実際の周波数から一桁落ちる。
#一桁落ちる部分は初めから許容して、リストを4桁ずつ切り出す作業を、3インデックスごとに繰り返せば、落ちた情報を補完できる

freqList = []

#画像の解像度
resolution = 3600

for i in range(0,resolution-2,3):
    prepare = freq_before[i:i+4]
    prepare = map(str, prepare)
    prepare_four = ''.join(prepare)
    prepare_four = int(prepare_four)
    freqList.append(prepare_four)

#freqqList調整
for x in range(1, len(freqList), 2):
    freqList[x] = freqList[x] + 4440
#出力する正弦波の基本情報
amp = 0.5
fs = 44100
length =  120 #どれだけ音数があってもこの秒数に収めて出力する
filepath = 'sine.wav'
play_sound = True
show_wave = True
start = 0
end = int(fs*length)    # 最大フレーム数
display_info = True

#UI


print("""
    ==============================
    | Poke Sound [Ver 2.0.0]     |
    ==============================
    いまや　おとをつかった　つうしんで　ポケモンを　データにして　おくれるんだと
    かがくの　ちからって　すげー！
    
    ＜{0}＞を おくる　じゅんびを　しています...
    """.format(name))

if name != "けつばん":
    # 作成
    data = create_sine_wave(amp, freqList, fs, length)

    # 書き出し
    sciio.write(filepath, fs, data)

    #再生用関数
    def saisei(name):
        pygame.mixer.init()
        pygame.mixer.music.load(name)
        pygame.mixer.music.set_volume(1.5)
        pygame.mixer.music.play(1)
        if name != "sine.wav":
            sleep(2)
        else: sleep(60)

    #送信
    send = "sine.wav"
    print("""
    -------------------------------------------------
        ＜{0}＞を　あいてに　おくっています...
    -------------------------------------------------
        """.format(name))
    saisei(send)
    sleep(3)
    #鳴き声
    saisei(voice)

    #UI
    print("""＜{0}＞を　おくりました！
    [じゅしんがわの　プログラムを　しゅうりょうしてください]""".format(name))
else:
    
    print("""
    ----------------------------------
    [FATAL ERROR]
    
    ＜けつばん＞は おくれませんでした...
    MissingNo couldn't be transported!
    ----------------------------------
    [じゅしんがわの　プログラムを　しゅうりょうしてください]""")
    
    lost = cv2.imread("img/resource/lost.png")
    pygame.mixer.music.load("audio/voice/lost.wav")
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.play(1)
    cv2.imshow("lost",lost)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
