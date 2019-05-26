#coding:utf-8

import serial
import time
import random

# シリアルからlong,int\r\nを受け取って
# -1 ~ 0 ~ 1までの浮動小数点数と0 ~ 65535までの整数を返す
class ReadBrake:
    def __init__(self, device):
        self.ser = serial.Serial(device, timeout=0.3, baudrate=9600, write_timeout=0.3)
        
        # 起動時は運転位置なので2倍
        self.max_raw_brake = self.getRawBrake() * 2
        
        # 10km/h ごとの出力値テーブル
        self.speed_table = [0, 25, 54, 82, 112, 146, 178, 211, 244, 255]

    def getRawBrake(self):
        raw_brake, buttons, x = self.getResult()
        return raw_brake

    def getResult(self):
        self.ser.reset_input_buffer()
        line = self.ser.readline()
        return line.split(b',')

    def waitAndGetData(self):
        result = self.getResult()
        if len(result) != 3:
            return [false, 0]

        raw_brake, buttons, x = result
        
        raw_brake = int(raw_brake)
        buttons = int(buttons)
        
        if raw_brake > self.max_raw_brake:
            raw_brake = self.max_raw_brake
        brake = ((raw_brake * 2) / self.max_raw_brake) - 1.0
        brake = -brake
        if random.randrange(30) == 0:
            print(self.max_raw_brake)
    
        # 遊びを設ける
        if -0.4 < brake < 0.4:
            brake = 0.0

        # ブレーキのレスポンスを悪くする
        brake *= 0.5

        return brake, buttons

    # 速度計の針を動かす
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
        self.sendSpeed(output)
        
    # 速度情報送信をする
    def sendSpeed(self, output):
        self.ser.write(bytes([output]))
        
def Worker(brake_shared, buttons_shared, speed_shared, device):
    brake = ReadBrake(device)
    brake.showRawBrake()
    while True:
        try:
            brake_level, buttons = brake.waitAndGetData()
            if brake_level is False:
                continue
            brake_shared.value = brake_level
            buttons_shared.value = buttons
            brake.setSpeed(speed_shared.value)
        except:
            pass
        finally:
            brake_shared.value = 1.0

if __name__ == '__main__':
    brake = ReadBrake('/dev/brake')
    while True:
        #print(brake.waitAndGetData())
        brake.showRawBrake()
        
