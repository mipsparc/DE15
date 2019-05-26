#! /usr/bin/env python3
#coding: utf-8

import DE10
import MasconReader
import BrakeReader
import Controller
import SoundManager
from multiprocessing import Process, Value
import time
from sys import argv

# 引数として接続されていないものを渡す
# ex) python3 ./NController.py controller mascon brake
CONTROLLER_CONNECTED = True
MASCON_CONNECTED = True
BRAKE_CONNECTED = True
test_params = argv[1:]
if 'controller' in test_params:
    CONTROLLER_CONNECTED = False
if 'mascon' in test_params:
    MASCON_CONNECTED = False
    MASCON_TEST_VALUE = 6
if 'brake' in test_params:
    BRAKE_CONNECTED = False
    BRAKE_TEST_VALUE = 0
    BUTTON_TEST_VALUE = 136

mascon_port = '/dev/mascon'
brake_port = '/dev/brake'
controller_port = '/dev/controller'

## マスコン読み込みプロセス起動
def ReadMasconWorker(mascon_shared, device):    
    mascon = MasconReader.ReadMascon(device)
    while True:
        mascon_level = mascon.waitAndGetMascon()
        mascon_shared.value = mascon_level

mascon_shared = Value('i', 0)
if MASCON_CONNECTED:
    mascon_process = Process(target=ReadMasconWorker, args=(mascon_shared, mascon_port))
    mascon_process.daemon = True # auto kill
    mascon_process.start()

# ブレーキ読み込みプロセス起動
def ReadBrakeWorker(brake_shared, buttons_shared, speed_shared, device):
    brake = BrakeReader.ReadBrake(device)
    brake.showRawBrake()
    while True:
        try:
            brake_level, buttons = brake.waitAndGetData()
            brake_shared.value = brake_level
            buttons_shared.value = buttons
            brake.setSpeed(speed_shared.value)
        except:
            pass

brake_shared = Value('f', 0.0)
buttons_shared = Value('i', 0)
speed_shared = Value('i', 0)
if BRAKE_CONNECTED:
    brake_process = Process(target=ReadBrakeWorker, args=(brake_shared, buttons_shared, speed_shared, brake_port))
    brake_process.daemon = True # auto kill
    brake_process.start()

DE101 = DE10.DE10()

if CONTROLLER_CONNECTED:
    controller = Controller.Controller(controller_port)

Sound = SoundManager.SoundManager()

# メインループを0.1秒おきに回す
last_counter = time.time()

while True:
    try:
        mascon_level = mascon_shared.value
        brake_level = brake_shared.value
        buttons = buttons_shared.value
        if not MASCON_CONNECTED:
            mascon_level = MASCON_TEST_VALUE
        if not BRAKE_CONNECTED:
            brake_level = BRAKE_TEST_VALUE
            buttons = BUTTON_TEST_VALUE
        
        DE101.setMascon(mascon_level)
        DE101.setBrake(brake_level)
        DE101.setButtons(buttons)
        DE101.advanceTime(DE101.isHonsenEnabled())
        speed = DE101.getSpeed()
        kph = speed * 3600 / 1000
        speed_shared.value = int(kph)
        print('BP: {}, BC: {}'.format(int(DE101.getBp()), int(490 - DE101.getBp())))

        Sound.brake(DE101.bc)
        Sound.switch(DE101.getWay())
        Sound.run(kph)
        Sound.power(mascon_level)

        if (not DE101.isKeyEnabled()) or (DE101.getWay() == 0):
            DE101.eb = True
            print('EB')

        if CONTROLLER_CONNECTED:
            controller.move(speed, DE101.getWay(), DE101.isHonsenEnabled())

        # 0.1秒経過するまでwaitする
        while (time.time() < last_counter + 0.1):
            time.sleep(0.001)
        last_counter = time.time()
        
    except KeyboardInterrupt:
        if CONTROLLER_CONNECTED:
            controller.move(0, 0, False)
            controller.move(0, 0, False)
        raise
        

