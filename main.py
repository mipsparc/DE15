#coding: utf-8

# 本物のDE15運転台部品で鉄道模型をリアルに制御するシミュレータシステム
# はじめにREADME.mdを読むこと

import DE10
from Mascon import Mascon
import Brake
from Brake import BrakeStatues
import HID
import DSair2_v1
import SoundManager
from multiprocessing import Process, Value
import time
import sys
import os

# デバイスファイル(udevファイルを読み込ませていればこのまま)
hid_port = '/dev/de15_hid'
dsair2_port = '/dev/dsair2'

# 標準エラー出力をログファイルにする
os.makedirs('log', exist_ok=True)
sys.stderr = open('log/' + str(int(time.time())) + '.txt', 'w')

# 共有メモリ作成
brake_status_shared = Value('i', int(BrakeStatues.FIX))
brake_level_shared = Value('f', 0.0)
speedmeter_shared = Value('i', 0)
mascon_shared = Value('i', 0)
pressure_shared = Value('i', 0)
way_shared = Value('i', 0)

# 引数として接続されていないものを渡す
# ex) python3 main.py controller hid
CONTROLLER_CONNECTED = True
HID_CONNECTED = True
BRAKE_CONNECTED = True
MASCON_CONNECTED = True
test_params = sys.argv[1:]
if 'controller' in test_params:
    CONTROLLER_CONNECTED = False
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

# HID読み書きプロセス起動
if HID_CONNECTED:
    hid_process = Process(target=HID.Worker, args=(brake_status_shared, brake_level_shared, speedmeter_shared, mascon_shared, pressure_shared, way_shared, hid_port))
    # 親プロセスが死んだら自動的に終了
    hid_process.daemon = True
    hid_process.start()

# DE10のモデルオブジェクト
DE101 = DE10.DE10()

# DSair2(DCCコマンドステーション)
if CONTROLLER_CONNECTED:
    is_dcc = True
    addr = 3
    dsair2 = DSair2_v1.DSair2(dsair2_port, is_dcc, addr)
    dsair2.move(0, 1)

# サウンドシステム
Sound = SoundManager.SoundManager()

# メインループを0.1秒おきに回すためのunix timeカウンタ
last_counter = time.time()

while True:
    try:
        # ハードウェアからの入力を共有メモリから取り出す
        if MASCON_CONNECTED:
            # TODO: 現在はマスコンにレバーサがついているため
            way = way_shared.value
            mascon_level = mascon_shared.value
        if BRAKE_CONNECTED:
            brake_status = brake_status_shared.value
            brake_level = brake_level_shared.value
            
        if HID_CONNECTED and not hid_process.is_alive():
            print('HIDプロセスが停止しています')
            raise SystemError
        
        # DE10モデルオブジェクトに入力を与える
        DE101.setWay(way)
        DE101.setMascon(mascon_level)
        DE101.setBrakeStatus(brake_status)
        DE101.setBrake(brake_level)
        DE101.advanceTime()
        speed = DE101.getSpeed()
                
        kph = speed * 3600 / 1000
        # 速度計に現在車速を与える
        speedmeter_shared.value = int(kph)
        pressure_shared.value = int(DE101.getBc())
        
        print('{}km/h  BC: {}'.format(int(kph), int(490 - DE101.getBp())))

        # 音を出す
        Sound.brake(DE101.bc)
        Sound.switch(DE101.getWay())
        Sound.power(mascon_level)
        Sound.joint(speed)
        Sound.run(speed)
        
        # DSAir2に速度と方向を渡す
        if CONTROLLER_CONNECTED:
            if speed <= 0:
                speed_out = 0
            else:
                speed_out = speed * 30
            dsair2.move(speed_out, DE101.getWay())
            last_move = speed == 0

        #if HID_CONNECTED:
            #meter.send(DE101.bc)

        # 0.1秒経過するまで待つ(sleepしないのは、音に影響するため)
        while (time.time() <= last_counter + 0.1):
            pass
        last_counter = time.time()

    # Ctrl-c押下時
    except KeyboardInterrupt:
        # 終了時に走行が停止して、速度計が0になるようにする
        if CONTROLLER_CONNECTED:
            dsair2.move(0, 0)
            dsair2.move(0, 0)
        if HID_CONNECTED:
            speedmeter_shared.value = 0

        # 速度計0が伝搬するまで待つ
        time.sleep(0.5)

        raise
    
# 出力と変換する(値は適当)
def calcDE15SpeedOut(speed):
    if speed <= 0:
        return 0
    return speed * 20
