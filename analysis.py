# coding:utf-8
import wave
import sys
import struct
import numpy as np
import subprocess
import pygame.mixer
import cv2
import math
import os
from scipy import fromstring, int16

#BGM
pygame.mixer.init(frequency = 44100)
pygame.mixer.music.load("audio/theme.wav")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)
#UI
print("""
    ==============================
    |Poke Sound [Ver 2.0.0]      |
    ==============================
    
    いまや　おとをつかった　つうしんで　ポケモンを　うけとれるんだと
    かがくの　ちからって　すげー！
    
    ...たいきちゅうです""")

subprocess.check_call(['python','record_1.py'])
#はじめに単なる一次元配列として変換値を入れとくところ
decode = []

#1,2,3,4と実際の画素値を対応させる
def trans_gaso(num):
    if num == 1 or num == 1.0:
        return 0
    if num == 2 or num == 2.0:
        return 72
    if num == 3 or num == 3.0:
        return 145
    if num == 4 or num == 4.0:
        return 255
    else: return 255
    
#指定の秒数でwavファイルを切り取る関数
def cut_wav(filename, time):
    
    global decode
    
    wavf = filename + '.wav'
    wr = wave.open(wavf, 'r')
    
    ch = wr.getnchannels()
    width = wr.getsampwidth()
    fr = wr.getframerate()
    fn = wr.getnframes()
    total_time = 1.0 * fn / fr
    integer = math.floor(total_time)
    t = time
    frames = int(ch * fr * t)
    num_cut = int(integer//t)

    # waveの実データを取得し、数値化
    data = wr.readframes(wr.getnframes())
    wr.close()
    X = fromstring(data, dtype=int16)
    
    for i in range(num_cut):
        start_cut = i*frames
        end_cut = i*frames + frames
        Y = X[start_cut:end_cut]
        #フーリエ解析
        F = np.fft.fft(Y)
        
        Amp = np.abs(F)

        Pow = Amp ** 2
        pow_arg = Pow.argsort()[::-1]
        #print("{0}, {1}, {2}, {3}".format(pow_arg[0],pow_arg[1],pow_arg[2],pow_arg[3]))
        pow_use = pow_arg[:4]
        switch = []
        for i in pow_use:
            if i < 1000: switch.append(i)
        
        tmp = 0
        if switch[0] > switch[1]:
            tmp = switch[0] - 444
            switch[0] = switch[1]
            switch[1] = tmp
        else: 
            switch[1] = switch[1] - 444
        for i in switch:
            #得られた数字を切り分けて格納
            hu = int(i - (i % 100))
            i = i - hu
            te = int(i - (i % 10))
            i = i - te
            one = int(i % 10)

            decode.append(trans_gaso(hu/100))
            decode.append(trans_gaso(te/10))
            decode.append(trans_gaso(one))


argvs = sys.argv
#画像解像度3600
resolution = 3600
cut_wav("sine", 0.1)
#値の取り方には誤差があるので、足りない分は白い画素で補完する
for i in range(resolution - len(decode)):
    decode.append(255)

#画像を生成する部分
#まず空の画像を作る
decode_np = np.zeros((60, 60))
cv2.imwrite("brank.jpg", decode_np)

#読み込み直してグレースケール化(画素値を一つに収める)
trans = cv2.imread("brank.jpg")
gray_trans = cv2.cvtColor(trans, cv2.COLOR_RGB2GRAY)

#全ての画素を一つ一つ書き換え
for i in range(60):
    for j in range(60):
        gray_trans[i, j] = decode[60*i+j]

#リサイズして最終出力
result = cv2.resize(gray_trans, (600, 600), interpolation = cv2.INTER_NEAREST)
print("""
    やったー！　ポケモンが　やってきました
    かわいがってやってください""")
pygame.mixer.music.load("audio/finish.wav")
pygame.mixer.music.set_volume(0.8)
pygame.mixer.music.play(1)
cv2.imwrite("result.jpg",result)
cv2.imshow("result", result)
cv2.waitKey(0)
cv2.destroyAllWindows()

#余計なものを消す
os.remove("brank.jpg")
os.remove("sine.wav")