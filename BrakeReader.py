#coding:utf-8

import serial

# シリアルからlong,int\r\nを受け取って
# -1 ~ 0 ~ 1までの浮動小数点数と0 ~ 65535までの整数を返す
class ReadBrake:
    def __init__(self, device):
        self.ser = serial.Serial(device, baudrate=9600)
        
        # 設定する
        self.max_raw_brake = 31000.0

    def waitAndGetBrake(self):
        self.ser.reset_input_buffer()
        
        try:
            line = self.ser.readline()
            raw_brake, buttons, x = line.split(b',')
            
            raw_brake = int(raw_brake)
            
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
       
       
if __name__ == '__main__':
    brake = ReadBrake('/dev/ttyUSB0')
    while True:
        print(brake.waitAndGetBrake())
