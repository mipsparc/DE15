#coding: utf-8

# 本物のDE15運転台部品で鉄道模型をリアルに制御するシミュレータシステム
# はじめにREADME.mdを読むこと

import DE10
from Mascon import Mascon
import Brake
from Brake import BrakeStatues
import HID
import SoundManager
from multiprocessing import Process, Value
import time
import sys
import os
from HID2 import HID2
from queue import Queue
import LogRotate

# デバイスファイル(udevファイルを読み込ませていればこのまま)
hid_port = '/dev/de15_hid'
hid2_port = '/dev/de15_meter'

# 標準エラー出力をログファイルにする
os.makedirs('log', exist_ok=True)
sys.stderr = open('log/' + str(int(time.time())) + '.txt', 'w')
LogRotate.rotate()

# 共有メモリ作成
brake_status_shared = Value('i', int(BrakeStatues.FIX))
brake_level_shared = Value('f', 0.0)
mascon_shared = Value('i', 0)
way_shared = Value('i', 0)
gpio_shared = Value('I', 0)
gpio_ready = False

# 引数として接続されていないものを渡す
# ex) python3 main.py controller hid
HID_CONNECTED = True
BRAKE_CONNECTED = True
MASCON_CONNECTED = True
test_params = sys.argv[1:]
if 'hid' in test_params:
    HID_CONNECTED = False
if 'brake' in test_params:
    BRAKE_CONNECTED = False
    brake_status = BrakeStatues.RUN
    brake_level = 0
else:
    input('ブレーキハンドル(自弁)を全ブレーキと固定の中間にして、Enterを押してください')
if 'mascon' in test_params:
    MASCON_CONNECTED = False
    mascon_level = 7
    way = 1

# HID読み書きプロセス起動
if HID_CONNECTED:
    hid_process = Process(target=HID.Worker, args=(brake_status_shared, brake_level_shared, mascon_shared, way_shared, gpio_shared, hid_port))
    # 親プロセスが死んだら自動的に終了
    hid_process.daemon = True
    hid_process.start()

# DE10のモデルオブジェクト
DE101 = DE10.DE10()

hid2 = HID2(hid2_port)

# BCをキューにして、1.5秒(15フレーム)遅延させる
bc_q = Queue(10000)
for i in range(200, 215):
    bc_q.put(i)

# サウンドシステム
Sound = SoundManager.SoundManager()

# メインループを0.1秒おきに回すためのunix timeカウンタ
last_counter = time.time()

# ATSの2進での点灯設定
last_ats_status = 0
# ATSの最初の地上子までの距離(10m)
until_ats_point = 10

# BVEに車速を送る
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dst = ('192.168.3.100', 10492)
sock.sendto(b'setspeedauto 1', dst)
sock.sendto(b'zeroaxis', dst)

Sound.startEngine()
time.sleep(12)

while True:
    try:
        # ハードウェアからの入力を共有メモリから取り出す
        if MASCON_CONNECTED:
            way = way_shared.value
            mascon_level = mascon_shared.value            
        if BRAKE_CONNECTED:
            brake_status = brake_status_shared.value
            brake_level = brake_level_shared.value
            
        if HID_CONNECTED and not hid_process.is_alive():
            print('HIDプロセスが停止しています')
            raise SystemError
        
        if gpio_shared != 9999:
            gpio_ready = True
        
        # DE10モデルオブジェクトに入力を与える
        DE101.setWay(way)
        DE101.setMascon(mascon_level)
        DE101.setBrakeStatus(brake_status)
        DE101.setBrake(brake_level)
        DE101.advanceTime()
        speed = DE101.getSpeed()
                
        kph = speed * 3600 / 1000
        
        # socketでBVEに車速を送る
        if way == 1:
            sock.sendto(('setspeed ' + str(int(kph))).encode('ascii'), dst)
        elif way == 2:
            sock.sendto(('setspeed -' + str(int(kph))).encode('ascii'), dst)
        
        # 速度計に現在車速を与える
        hid2.setMeter(kph)
        
        print('{}km/h  BC: {}'.format(int(kph), int(DE101.getBc())))
        
        if until_ats_point > 0:
            until_ats_point -= speed / 10.0
        
        if gpio_ready:
            # ホーン
            hone = False
            if gpio_shared.value & 0b100000000 == 0:
                hone = True
            
            if until_ats_point > 0:
                gpio_shared.value = (gpio_shared.value & ~0b1111) + 0b0
            if until_ats_point < 0:
                # ATS-P 通常時
                if kph <= 75:
                    gpio_shared.value = (gpio_shared.value & ~0b1111) + 0b1010
                    if last_ats_status != 0b1010:
                        Sound.dingBell()
                    last_ats_status = 0b1010
                # ATS-P ブレーキ動作
                if kph > 80:
                    gpio_shared.value = (gpio_shared.value & ~0b1111) + 0b1011
                    if last_ats_status != 0b1011:
                        Sound.dingBell()
                    last_ats_status = 0b1011
                    DE101.eb = True
                # ATS-P パターン接近
                elif kph > 76:
                    gpio_shared.value = (gpio_shared.value & ~0b1111) + 0b1110
                    if last_ats_status != 0b1110:
                        Sound.dingBell()
                    last_ats_status = 0b1110
                # ブレーキ緩解まで光り続ける
                if DE101.eb == True:
                    gpio_shared.value = (gpio_shared.value & ~0b1111) + 0b1011

        # 音を出す
        Sound.brake(DE101.bc)
        Sound.power(mascon_level)
        Sound.joint(speed)
        Sound.run(speed)
        Sound.hone(hone)

        # 0.1秒経過するまで待つ(sleepしないのは、音に影響するため)
        while (time.time() <= last_counter + 0.1):
            pass
        last_counter = time.time()


    except Exception as e:
        gpio_shared.value = 0
        sock.sendto(('setspeed ' + '0').encode('ascii'), dst)
        time.sleep(0.5)

        raise
