#coding:utf-8

import serial
from Brake import DE15Brake
from Mascon import Mascon
from Smooth import BCToLeft, BCToRight, BP
import time

# ブレーキ装置、速度計、圧力計などのシリアルI/Oを一括管理する
class HID:
    def __init__(self, device):
        # timeoutを設定することで通信エラーを防止する
        try:
            self.ser = serial.Serial(device, timeout=0.1, inter_byte_timeout=0.1, baudrate=19200)
        except serial.serialutil.SerialException:
            print('正常にシリアルポートを開けませんでした。')
            raise
        
        self.last_sent_ats = 0
        # 初期値
        self.last_bc_value = 330
        
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
        
    def sendATS(self, value):
        if self.last_sent_ats != value:
            self.ser.write(f'a{value}EOF\n'.encode('ascii'))
            self.last_sent_ats = value
            
    def setBC(self, bc):
        # 表示計器の関係上
        bc += 30
        
        if self.last_bc_value == bc:
            return
        
        if self.last_bc_value < bc:
            self.sendBC(int(BCToRight.getValue(bc)))
        else:
            self.sendBC(int(BCToLeft.getValue(bc)))

        self.last_bc_value = bc
        
    def setBP(self, bp):
        self.sendBP(int(BP.getValue(bp)))
        
    def setER(self, er):
        self.sendER(int(ER.getValue(er)))

    def sendBC(self, value):
        if 890 <= value <= 1150:
            self.ser.write(f'b{value}EOF\n'.encode('ascii'))
        
    def sendBP(self, value):
        if 1300 <= value <= 1700:
            self.ser.write(f'p{value}EOF\n'.encode('ascii'))
        
# シリアル通信プロセスのワーカー
def Worker(brake_status_shared, brake_level_shared, bc_shared, mascon_shared, way_shared, gpio_shared, device):
    hid = HID(device)
    
    # 10回読み込んでからブレーキを初期化する
    init_brake_ref_count = 10
    
    # 初期化
    hid.sendATS(0)
    
    # GPIOデータがまだ到着していないときのダミー
    gpio_shared.value = 9999
    
    last_sent = time.time();
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
                gpio_shared.value = (int(value) & ~0b1111) + (gpio_shared.value & 0b1111)
                
        # 送信段
        ats = gpio_shared.value & 0b1111
        hid.sendATS(ats)
        
        if last_sent + 0.1 < time.time():
            hid.setBC(bc_shared.value)
            hid.setBP(490 - bc_shared.value)
            last_sent = time.time()
            
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
        value = int(input('bp> '))
        #value = 1600
        hid.sendBP(value)
        
        #value = int(input('bc> '))
        #value = 1400
        #hid.sendBC(value)
        
        #print(hid.readSerial())
