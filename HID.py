#coding:utf-8

import serial
import sys
from Brake import DE15Brake

class HID:
    def __init__(self, device):
        # timeoutを設定することで通信エラーを防止する
        try:
            self.ser = serial.Serial(device, timeout=0.3, write_timeout=0.3, inter_byte_timeout=0.3, baudrate=9600)
        except serial.serialutil.SerialException:
            print('正常にシリアルポートを開けませんでした。')
            raise
        
    # intで出力する
    def readSerial(self):
        try:
            raw_value = self.ser.readline()
            self.ser.reset_input_buffer()
            raw_value = raw_value.decode('ascii')
            raw_value = raw_value.replace('\r\n', '')
            return {
                'brake': int(float(raw_value))
            }
        except KeyboardInterrupt:
            exit()
        except:
            return False

# シリアル通信プロセスのワーカー
def Worker(brake_status_shared, brake_level_shared, device):
    hid = HID(device)
    while True:
        try:
            brake_value = hid.readSerial()['brake']
            syncBrake(brake_value, brake_status_shared, brake_level_shared)
        except serial.serialutil.SerialException:
            raise
        
def syncBrake(brake_value, brake_status_shared, brake_level_shared):
    brake_result = DE15Brake.formatValue(brake_value)
    # 不正値の読み飛ばし
    if brake_result == False:
        return
    brake_status_shared.value = brake_result['status']
    brake_level_shared.value = brake_result['level']

    
    '''
    #
    # 速度計を動かすようになったら有効化する
    #
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
    '''
