#coding:utf-8

import serial
from Smooth import Pressure, SpeedMeter

# ブレーキ装置、速度計、圧力計などのシリアルI/Oを一括管理する
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
        #if self.send_rotate == 0:
        # 速度計への出力
        speed_out = SpeedMeter.getValue(speed)
        self._send(f's{speed_out}EOF\n'.encode('ascii'))
        #self.send_rotate += 1
        #elif self.send_rotate == 1:
            #pressure_out = Pressure.getValue(pressure)
            #self.ser.write(f'p{pressure_out}EOF\n'.encode('ascii'))
            #self.send_rotate = 0
            
    def _send(self, text):
        self.ser.write(text)

if __name__ == '__main__':
    meter = Meter('/dev/de15_meter')
    while True:
        speed_out = int(input('speed: '))
        meter._send(f's{speed_out}EOF\n'.encode('ascii'))
