#coding:utf-8

import serial
import sys
from Brake import DE15Brake
from Mascon import Mascon
from Smooth import Pressure, SpeedMeter

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
        speed_out = SpeedMeter.getValue(speed)
        pressure_out = Pressure.getValue(pressure)
        # 速度計への出力
        self.ser.write(f'speed:{speed_out}'.encode('ascii'))
        # 圧力計への出力
        self.ser.write(f'pressure:{pressure_out}'.encode('ascii'))

# シリアル通信プロセスのワーカー
def Worker(brake_status_shared, brake_level_shared, speedmeter_shared, mascon_shared, pressure_shared, device):
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
        hid.send(speedmeter_shared.value, pressure_shared.value)
        
def syncBrake(brake_value, brake_status_shared, brake_level_shared):
    brake_result = DE15Brake.formatValue(int(brake_value))
    # 不正値の読み飛ばし
    if brake_result == False:
        return
    brake_status_shared.value = brake_result['status']
    brake_level_shared.value = brake_result['level']
    
def syncMascon(mascon_value, mascon_shared):
    mascon_level = Mascon.formatValue(mascon_value)
    
    # 不正値の読み飛ばし(0-14)
    if not mascon_level in range(15):
        return
    mascon_shared.value = mascon_level
    
if __name__ == '__main__':
    hid = HID('/dev/de15_hid')
    while True:
        print(hid.readSerial())
