#encoding: utf-8

import DE10
import MasconReader
import BrakeReader
import Controller
from multiprocessing import Process, Value
import time

## マスコン読み込みプロセス起動
#def ReadMasconWorker(mascon_shared, device):    
    #mascon = MasconReader.ReadMascon(device)
    #while True:
        #mascon_level = mascon.waitAndGetMascon()
        #mascon_shared.value = mascon_level

#mascon_shared = Value('i', 0)
#mascon_process = Process(target=ReadMasconWorker, args=(mascon_shared, '/dev/ttyUSB0'))
#mascon_process.start()

# ブレーキ読み込みプロセス起動
def ReadBrakeWorker(brake_shared, device):    
    brake = BrakeReader.ReadBrake(device)
    while True:
        brake_level = brake.waitAndGetBrake()
        brake_shared.value = brake_level

brake_shared = Value('f', 0.0)
brake_process = Process(target=ReadBrakeWorker, args=(brake_shared, '/dev/ttyUSB0'))
#brake_process = Process(target=ReadBrakeWorker, args=(brake_shared, '/dev/ttyUSB2'))
brake_process.start()


DE101 = DE10.DE10()
#controller = Controller.Controller('/dev/ttyUSB1')

# 精密カウンターでメインループを0.1秒おきに回す
last_counter = time.time()

while True:
    #mascon_level = mascon_shared.value
    brake_level = brake_shared.value
    
    #DE101.setMascon(mascon_level)
    DE101.setBrake(brake_level)
    
    # 0.1秒経過するまでwaitする
    while (time.time() < last_counter + 0.1):
        time.sleep(0.001)
    last_counter = time.time()
    
    DE101.advanceTime()
    print(DE101.getBp())
    #speed = DE101.getSpeed()
    
    #controller.move(speed)
