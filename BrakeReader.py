#coding:utf-8

import serial

# シリアルからlong\r\nを受け取って
# -1 ~ 0 ~ 1までの浮動小数点数を返す
class ReadBrake:
    def __init__(self, device):
        self.ser = serial.Serial(device, baudrate=9600)
        
        # 設定する
        self.max_raw_brake = 31000.0

    def waitAndGetBrake(self):
        self.ser.reset_input_buffer()
        
        try:
            raw_brake = int(self.ser.readline())
            if raw_brake > self.max_raw_brake:
                raw_brake = self.max_raw_brake
            brake = ((raw_brake * 2) / self.max_raw_brake) - 1.0
            
            # 遊びを設ける
            if -0.1 < brake < 0.1:
                brake = 0.0
            
        except ValueError:
            brake = 0.0

        return brake
       
       
if __name__ == '__main__':
    brake = ReadBrake('/dev/ttyUSB0')
    while True:
        print(brake.waitAndGetBrake())
