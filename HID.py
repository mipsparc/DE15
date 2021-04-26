#coding:utf-8

import serial
import sys
from Brake import DE15Brake
from Mascon import Mascon
from Smooth import Pressure, SpeedMeter
import time

# ブレーキ装置、速度計、圧力計などのシリアルI/Oを一括管理する
class HID:
    def __init__(self, device):
        self.send_rotate = 0
        # timeoutを設定することで通信エラーを防止する
        try:
            self.ser = serial.Serial(device, timeout=0.1, inter_byte_timeout=0.1, baudrate=19200)
        except serial.serialutil.SerialException:
            print('正常にシリアルポートを開けませんでした。')
            raise
        
    def readSerial(self):
        raw_value = self.ser.readline()
        try:
            raw_text = raw_value.decode('ascii')
        except UnicodeDecodeError:
            print('異常データ')
            return False
        
        raw_text = raw_text.replace('\r\n', '')
        
        try:
            data_type, value = raw_text.split(':')
            return [data_type, value]
        except ValueError:
            return False
                
    def send(self, speed, pressure):
        if self.send_rotate == 0:
            # 速度計への出力
            speed_out = SpeedMeter.getValue(speed)
            self.ser.write(f's{speed_out}EOF\n'.encode('ascii'))
            self.send_rotate += 1
        elif self.send_rotate == 1:
            pressure_out = Pressure.getValue(pressure)
            self.ser.write(f'p{pressure_out}EOF\n'.encode('ascii'))
            self.send_rotate = 0
        
# シリアル通信プロセスのワーカー
def Worker(brake_status_shared, brake_level_shared, speedmeter_shared, mascon_shared, pressure_shared, way_shared, device):
    hid = HID(device)
    
    # 10回読み込んでからブレーキを初期化する
    init_brake_ref_count = 10
    while True:
        serial = hid.readSerial()
        
        # 受信段
        if serial != False:
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
                syncMascon(value, mascon_shared, way_shared)
            if data_type == 'gpio':
                pass
    
        # 送信段
        hid.send(speedmeter_shared.value, pressure_shared.value)
        
        time.sleep(0.001)
        
def syncBrake(brake_value, brake_status_shared, brake_level_shared):
    brake_result = DE15Brake.formatValue(int(brake_value))
    # 不正値の読み飛ばし
    if brake_result == False:
        return
    brake_status_shared.value = brake_result['status']
    brake_level_shared.value = brake_result['level']

start_pressing_waysw = False
def syncMascon(mascon_value, mascon_shared, way_shared):
    global start_pressing_waysw
    mascon_level, way = Mascon.formatValue(mascon_value)
    
    # テスト用方向転換スイッチ押下
    if mascon_level == 99:
        if start_pressing_waysw == False:
            start_pressing_waysw = time.time()
        else:
            if time.time() > (start_pressing_waysw + 1):
                if way_shared.value == 1:
                    way_shared.value = 2
                else:
                    way_shared.value = 1
                start_pressing_waysw = False
        return
        
    # 不正値の読み飛ばし(0-14)
    if not mascon_level in range(15):
        return
    mascon_shared.value = mascon_level
    way_shared.value = way
    
if __name__ == '__main__':
    hid = HID('/dev/de15_hid')
    while True:
        #hid.readSerial()
        print(hid.readSerial())
        hid.send(0, 180)
