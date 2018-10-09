#encoding: utf-8

import DE10
import MasconReader
import BrakeReader
import Controller
import Sounder
from multiprocessing import Process, Value
import time

## マスコン読み込みプロセス起動
def ReadMasconWorker(mascon_shared, device):    
    mascon = MasconReader.ReadMascon(device)
    while True:
        mascon_level = mascon.waitAndGetMascon()
        mascon_shared.value = mascon_level

mascon_shared = Value('i', 0)
mascon_process = Process(target=ReadMasconWorker, args=(mascon_shared, '/dev/ttyUSB0'))
mascon_process.start()

# ブレーキ読み込みプロセス起動
def ReadBrakeWorker(brake_shared, buttons_shared, device):    
    brake = BrakeReader.ReadBrake(device)
    while True:
        brake_level, buttons = brake.waitAndGetBrake()
        brake_shared.value = brake_level
        buttons_shared.value = buttons

brake_shared = Value('f', 0.0)
buttons_shared = Value('i', 0)
brake_process = Process(target=ReadBrakeWorker, args=(brake_shared, buttons_shared, '/dev/ttyUSB0'))
brake_process.start()

DE101 = DE10.DE10()
controller = Controller.Controller('/dev/ttyUSB2')

Sound = Sounder.Sounder()
Sound.Idle()

# メインループを0.1秒おきに回す
last_counter = time.time()

# ホーンが最後に押されたUNIX time
last_hone = 0

# 最後の方向, 速度
last_way = 0
last_speed = 0
last_mascon_level = 0
last_brake = False

while True:
    try:
        mascon_level = mascon_shared.value
        brake_level = brake_shared.value
        buttons = buttons_shared.value
        
        DE101.setMascon(mascon_level)
        DE101.setBrake(brake_level)
        DE101.setButtons(buttons)
        
        # 0.1秒経過するまでwaitする
        while (time.time() < last_counter + 0.1):
            time.sleep(0.001)
        last_counter = time.time()
        
        DE101.advanceTime()
        speed = DE101.getSpeed()
        
        if (last_hone < time.time() - 3) and DE101.isHoneEnabled():
            last_hone = time.time()
            Sound.Hone()
            
        if brake_level > 0 and not last_brake:
            last_brake = True
            Sound.Brake()
        elif brake_level <= 0:
            last_brake = False
            Sound.Brake(stop=True)
            
        if last_way != DE101.getWay():
            last_way = DE101.getWay()
            Sound.Switch()
            
        if speed > 0 and last_speed <= 0:
            Sound.Run()
        elif speed <= 0 and last_speed > 0:
            Sound.Run(stop=True)
        last_speed = speed
        
        if mascon_level == 0:
            Sound.Power1(stop=True)
            Sound.Power2(stop=True)
            Sound.Power3(stop=True)
        if 1 <= mascon_level < 5 and (last_mascon_level == 0 or 5 <= last_mascon_level):
            Sound.Power2(stop=True)
            Sound.Power3(stop=True)
            Sound.Power1()
        elif 5 <= mascon_level < 10 and (last_mascon_level < 5 or 10 <= last_mascon_level):
            Sound.Power1(stop=True)
            Sound.Power3(stop=True)
            Sound.Power2()
        elif 10 <= mascon_level < 14 and (last_mascon_level < 10 or 14 <= last_mascon_level):
            Sound.Power1(stop=True)
            Sound.Power2(stop=True)
            Sound.Power3()
        last_mascon_level = mascon_level

        
        print(speed * 3600 / 1000)
        controller.move(speed, DE101.getWay())
    except KeyboardInterrupt:
        controller.move(0)
        raise
        

