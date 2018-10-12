#coding:utf-8

import serial
import time
import random

# シリアルからlong,int\r\nを受け取って
# -1 ~ 0 ~ 1までの浮動小数点数と0 ~ 65535までの整数を返す
class ReadBrake:
    def __init__(self, device):
        self.ser = serial.Serial(device, baudrate=9600)
        
        # 設定する
        self.max_raw_brake = 31000.0
        
        # 10km/h ごとの出力値テーブル
        self.speed_table = [0, 25, 54, 82, 112, 146, 178, 211, 244, 255]

    def waitAndGetData(self):
        self.ser.reset_input_buffer()
        
        try:
            line = self.ser.readline()
            raw_brake, buttons, x = line.split(b',')
            
            raw_brake = int(raw_brake)
            buttons = int(buttons)
            
            if raw_brake > self.max_raw_brake:
                raw_brake = self.max_raw_brake
            brake = ((raw_brake * 2) / self.max_raw_brake) - 1.0
            
            # 遊びを設ける
            if -0.1 < brake < 0.1:
                brake = 0.0
            
        except ValueError:
            brake = 0.0
            buttons = 0

        return brake, buttons

    def setSpeed(self, speed):
        if speed == 0:
            speed = 1
        if speed / 10 >= 9:
            speed = 89
            
        lower_speed = self.speed_table[speed // 10]
        higher_speed = self.speed_table[(speed // 10) + 1]
        output = lower_speed + int((lower_speed + higher_speed) / (speed * 2) * (speed % 10))
        
        output += random.randrange(-5, 5)
        
        if output < 0:
            output = 0
        if output > 255:
            output = 255
            
        self.ser.write(bytes([output]))
       
if __name__ == '__main__':
    brake = ReadBrake('/dev/ttyUSB0')
    while True:
        print(brake.waitAndGetBrake())
        
