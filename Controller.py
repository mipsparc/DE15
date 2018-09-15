#encoding: utf-8

import serial

class Controller:
    def __init__(self, device):
        #出力値の傾き
        self.magnify_1 = 1.0
        self.magnify_2 = 0.5
        
        # 2回に一回書き込む
        self.write_count = False
        self.device = serial.Serial(device, baudrate=9600)
        
    # speed: m/s
    def move(self, speed):
        # 動き始める速度
        base_power = 42
        
        #1次関数を2つ繋げる
        if speed < 5.5:
            output_power = (speed * magnify_1) + base_power
        else:
            output_power = (speed * magnify_2) + (5.5 * magnify_1) + base_power
            
        if output_power > 255:
            output_power = 255
        
        if self.write_count == True:
            self.write_count = False
            if speed <= 0:
                self._write(bytes([ord('!')]))
            else:
                self._write(bytes([ord('!') + int(output_power)]))

            print(str(speed * 3600 / 1000) + 'km/h')
        else:
            self.write_count = True
            
    def _write(self,output_power):
        self.device.write(output_power)
