#coding:utf-8

import serial
import sys
from Brake import DE15Brake

# ブレーキ装置、速度計、圧力計などのシリアルI/Oを一括管理する
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
        raw_value = self.ser.readline()
        self.ser.reset_input_buffer()
        raw_text = raw_value.decode('ascii')
        raw_text = raw_text.replace('\r\n', '')
        try:
            data_type, value = raw_text.split(':')
            return [data_type, value]
        except ValueError:
            return False
        
    def send(self, speed):
        # 適当な係数
        speed_out = speed * 2
        # 速度計への出力
        self.ser.write(f'speed:{speed_out}'.encode('ascii'))

# シリアル通信プロセスのワーカー
def Worker(brake_status_shared, brake_level_shared, speedmeter_shared, mascon_shared, device):
    hid = HID(device)
    
    # 10回読み込んでからブレーキを初期化する
    init_brake_ref_count = 10
    while True:
        serial = hid.readSerial()
        if serial == False:
            continue
        data_type, value = serial
        if data_type == 'brake':
            # 最初10回は読み飛ばした上で、初期位置を決定する
            if init_brake_ref_count > 1:
                init_brake_ref_count -= 1
            elif init_brake_ref_count == 1:
                DE15Brake.setRefValue(value)
                init_brake_ref_count = 0
            else:
                syncBrake(value, brake_status_shared, brake_level_shared)
        if data_type == 'mascon':
            syncMascon(value, mascon_shared)
        hid.send(speedmeter_shared.value)
        
def syncBrake(brake_value, brake_status_shared, brake_level_shared):
    brake_result = DE15Brake.formatValue(int(brake_value))
    # 不正値の読み飛ばし
    if brake_result == False:
        return
    brake_status_shared.value = brake_result['status']
    brake_level_shared.value = brake_result['level']
    
def syncMascon(mascon_value, mascon_shared):
    mascon_value = int(mascon_value)
    
    # 不正値の読み飛ばし(0-14)
    if not mascon_value in range(15):
        return
    masconshared.value = mascon_shared
    
if __name__ == '__main__':
    hid = HID('/dev/de15_hid')
    while True:
        print(hid.readSerial())
    
    '''
    #
    # 速度計を動かすようになったら有効化する
    #
    # 速度計の針を動かす
    def setSpeedMeter(speed):
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
