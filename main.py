#coding: utf-8

# 実際の運転台部品で鉄道模型をリアルに制御するシミュレータシステム
# はじめにREADME.mdを読むこと

import DE10
import MasconReader
import BrakeReader
from BrakeReader import BrakeStatues
import DSair2_v1
import SoundManager
import Meter
from multiprocessing import Process, Value
import time
import sys
import os

# 各装置のデバイスファイル(udevファイルを読み込ませていればこのまま)
mascon_port = '/dev/mascon'
meter_port = '/dev/meter'
brake_port = '/dev/ttyACM0'
# DSair2のシリアルポート。Linuxでほかに機器がなければこのまま
dsair2_port = '/dev/ttyUSB0'

# 標準エラー出力をログファイルにする
os.makedirs('log', exist_ok=True)
sys.stderr = open('log/' + str(int(time.time())) + '.txt', 'w')

# 引数として接続されていないものを渡す
# ex) python3 ./main.py controller mascon brake
CONTROLLER_CONNECTED = True
MASCON_CONNECTED = True
BRAKE_CONNECTED = True
METER_CONNECTED = True
test_params = sys.argv[1:]
if 'controller' in test_params:
    CONTROLLER_CONNECTED = False
if 'mascon' in test_params:
    MASCON_CONNECTED = False
    MASCON_TEST_VALUE = 7
if 'brake' in test_params:
    BRAKE_CONNECTED = False
    BRAKE_STATUS_TEST_VALUE = BrakeStatues.RUN
    BRAKE_LEVEL_TEST_VALUE = 0
if 'meter' in test_params:
    METER_CONNECTED = False

# マスコン読み込みプロセス起動、共有メモリ作成
mascon_shared = Value('i', 0)
if MASCON_CONNECTED:
    mascon_process = Process(target=MasconReader.Worker, args=(mascon_shared, mascon_port))
    # 親プロセスが死んだら自動的に終了
    mascon_process.daemon = True
    mascon_process.start()

# ブレーキ読み書きプロセス起動、共有メモリ作成
brake_status_shared = Value('i', int(BrakeStatues.FIX))
brake_level_shared = Value('f', 0.0)
speed_shared = Value('i', 0)
if BRAKE_CONNECTED:
    brake_process = Process(target=BrakeReader.Worker, args=(brake_status_shared, brake_level_shared, brake_port))
    # 親プロセスが死んだら自動的に終了
    brake_process.daemon = True
    brake_process.start()

# DE10のモデルオブジェクト
DE101 = DE10.DE10()

# DSair2(DCCコマンドステーション)
if CONTROLLER_CONNECTED:
    is_dcc = True
    addr = 3
    dsair2 = DSair2_v1.DSair2(dsair2_port, is_dcc, addr)
    dsair2.move(0, 1)

# ブレーキ圧力計オブジェクト
if METER_CONNECTED:
    meter = Meter.Meter(meter_port)

# サウンドシステム
Sound = SoundManager.SoundManager()

# メインループを0.1秒おきに回すためのunix timeカウンタ
last_counter = time.time()

while True:
    try:
        # ハードウェアからの入力を共有メモリから取り出す
        mascon_level = mascon_shared.value
        brake_status = brake_status_shared.value
        brake_level = brake_level_shared.value

        if not MASCON_CONNECTED:
            mascon_level = MASCON_TEST_VALUE
        if not BRAKE_CONNECTED:
            brake_status = BRAKE_STATUS_TEST_VALUE
            brake_level = BRAKE_LEVEL_TEST_VALUE
        
        # DE10モデルオブジェクトに入力を与える
        DE101.setMascon(mascon_level)
        DE101.setBrakeStatus(brake_status)
        DE101.setBrake(brake_level)
        DE101.advanceTime()
        speed = DE101.getSpeed()
                
        kph = speed * 3600 / 1000
        # 速度計に現在車速を与える
        speed_shared.value = int(kph)
        
        print('{}km/h  BC: {}'.format(int(kph), int(490 - DE101.getBp())))

        # 音を出す
        Sound.brake(DE101.bc)
        Sound.switch(DE101.getWay())
        Sound.power(mascon_level)
        Sound.joint(speed)
        Sound.run(speed)
        
        # DSAir2に速度と方向を渡す
        if CONTROLLER_CONNECTED:
            calcDE15SpeedOut(speed)
            dsair2.move(speed_out, DE101.getWay())
            last_move = speed == 0

        if METER_CONNECTED:
            meter.send(DE101.bc)

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
        if BRAKE_CONNECTED:
            speed_shared.value = 0

        # 速度計0が伝搬するまで待つ
        time.sleep(0.5)

        raise
    
# 出力と変換する(値は適当)
def calcDE15SpeedOut(speed):
    if speed <= 0:
        return 0
    return speed * 20
