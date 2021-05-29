#coding:utf-8

import serial
from Smooth import SpeedMeter, ERToRight, ERToLeft

# 速度計を管理する
class HID2:
    def __init__(self, device):
        self.send_rotate = 0
        # timeoutを設定することで通信エラーを防止する
        try:
            self.ser = serial.Serial(device, timeout=0.1, inter_byte_timeout=0.1, baudrate=19200)
        except serial.serialutil.SerialException:
            print('正常にシリアルポートを開けませんでした。')
            raise
        
        self.last_er = 0
        
    def setMeter(self, speed):
        speed_out = SpeedMeter.getValue(speed)
        self._sendMeter(speed_out)
    
    def _sendMeter(self, speed_out):
        self._send(f's{speed_out}EOF\n'.encode('ascii'))
    
    # 釣り合い管
    def setER(self, er):
        if self.last_er == er:
            return;
        
        if self.last_er < er:
            self._sendER(int(ERToRight.getValue(er)))
        else:
            self._sendER(int(ERToLeft.getValue(er)))
        self.last_er = er

    def _sendER(self, pressure_out):
        if 1400 <= pressure_out <= 1800:
            self._send(f'e{pressure_out}EOF\n'.encode('ascii'))

    def _send(self, text):
        self.ser.write(text)

if __name__ == '__main__':
    hid2 = HID2('/dev/de15_meter')
    while True:
        #speed_out = int(input('speed: '))
        #hid2._send(f's{speed_out}EOF\n'.encode('ascii'))
        
        value = int(input('er> '))
        #value = 1500
        hid2._sendER(value)
