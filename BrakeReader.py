#coding:utf-8

import serial
import time
import random

# ブレーキ装置とシリアル伝送で通信して、long,int\r\nを受け取って
# -1 ~ 0 ~ 1までの浮動小数点数と0 ~ 65535までの整数を返す
class ReadBrake:
    def __init__(self, device):
        # timeoutを設定することで通信エラーを防止する
        self.ser = serial.Serial(device, timeout=0.3, baudrate=9600, write_timeout=0.3)
        
        # 現在のコントローラでは一番右がMAXなので、実際のMAXの値から引いたものが現在のraw_brake
        self.max_value = 53480
        
        # 起動初期設定。起動時は一番奥にする
        self.max_raw_brake = self.getRawBrake()
        
        # 10km/h ごとの出力値テーブル
        self.speed_table = [0, 45, 75, 107, 137, 173, 206, 242, 252, 253]
        
    def getRawBrake(self):
        result = self.getResult()
        # 不正な値が来たときは読み飛ばす
        if len(result) != 3:
            return False
        return self.max_value - int(result[0])

    # シリアル通信のバッファから取得する
    def getResult(self):
        self.ser.reset_input_buffer()
        line = self.ser.readline()
        return line.split(b',')

    def waitAndGetData(self):
        result = self.getResult()
        # 不正な値が来たときは読み飛ばす
        if len(result) != 3:
            return [false, 0]

        raw_brake, buttons, x = result
        raw_brake = abs(self.max_value - int(raw_brake))
        buttons = int(buttons)
        
        if raw_brake > self.max_raw_brake:
            raw_brake = self.max_raw_brake
        brake = ((raw_brake * 2) / self.max_raw_brake) - 1.0
        brake = -brake

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

# シリアル通信プロセスのワーカー
def Worker(brake_shared, buttons_shared, speed_shared, device):
    brake = ReadBrake(device)
    print(brake.getRawBrake())
    while True:
        try:
            brake_level, buttons = brake.waitAndGetData()
            # 不正値の読み飛ばし
            if brake_level is False:
                continue
            if brake_level < -1 or 1 < brake_level:
                continue
            brake_shared.value = brake_level
            buttons_shared.value = buttons
            brake.setSpeed(speed_shared.value)
        # できる限りエラーは無視する
        except:
            pass

if __name__ == '__main__':
    brake = ReadBrake('/dev/brake')
    while True:
        print(brake.waitAndGetData())
        #print(brake.getRawBrake())
        
