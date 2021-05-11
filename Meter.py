#coding:utf-8

import serial
from Smooth import SpeedMeter

# 速度計を管理する
class Meter:
    def __init__(self, device):
        self.send_rotate = 0
        # timeoutを設定することで通信エラーを防止する
        try:
            self.ser = serial.Serial(device, timeout=0.1, inter_byte_timeout=0.1, baudrate=19200)
        except serial.serialutil.SerialException:
            print('正常にシリアルポートを開けませんでした。')
            raise
        
    def send(self, speed, pressure):
        speed_out = SpeedMeter.getValue(speed)
        self._send(f's{speed_out}EOF\n'.encode('ascii'))
            
    def _send(self, text):
        self.ser.write(text)

if __name__ == '__main__':
    meter = Meter('/dev/de15_meter')
    while True:
        speed_out = int(input('speed: '))
        meter._send(f's{speed_out}EOF\n'.encode('ascii'))
