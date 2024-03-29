#coding:utf-8

import serial
from Brake import DE15Brake
from Mascon import Mascon
import time

# ブレーキ装置、速度計のシリアルI/Oを一括管理する
class HID:
    def __init__(self, device):
        # timeoutを設定することで通信エラーを防止する
        try:
            self.ser = serial.Serial(device, timeout=0.1, inter_byte_timeout=0.1, baudrate=19200)
        except serial.serialutil.SerialException:
            print('正常にシリアルポートを開けませんでした。')
            raise

    def readSerial(self):
        try:
            raw_value = self.ser.readline()
            raw_text = raw_value.decode('ascii')
        except KeyboardInterrupt:
            raise
        except:
            print('異常データ')
            return False
        
        raw_text = raw_text.replace('\r\n', '')
        try:
            data_type, value = raw_text.split(':')
            return [data_type, value]
        except ValueError:
            return False
        
    def sendATS(self, value):
        self.ser.write(f'a{value}EOF\n'.encode('ascii'))

        
# シリアル通信プロセスのワーカー
def Worker(brake_status_shared, brake_level_shared, mascon_shared, way_shared, gpio_shared, device):
    hid = HID(device)
    
    # 10回読み込んでからブレーキを初期化する
    init_brake_ref_count = 10
    
    # 初期化
    hid.sendATS(0b0)
    
    # GPIOデータがまだ到着していないときのダミー
    gpio_shared.value = 9999
    
    last_sent = time.time();
    while True:
        try:
            serial = hid.readSerial()
            if serial == False:
                continue
        except KeyboardInterrupt:
            raise
        except:
            print('HIDシリアル通信エラー')
            time.sleep(0.05)
            continue
        
        # 受信段
        data_type, value = serial
        if value == '':
            continue
        try:
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
        except ValueError:
            continue
                
        # 送信段
        ats = gpio_shared.value & 0b1111
        
        if last_sent + 0.1 < time.time():
            hid.sendATS(ats)
            last_sent = time.time()
            
        time.sleep(0.01)
        
def syncBrake(brake_value, brake_status_shared, brake_level_shared):
    try:
        brake_result = DE15Brake.formatValue(int(brake_value))
        # 不正値の読み飛ばし
        if brake_result == False:
            print('ブレーキ不正値')
            return
    except (SystemError, ValueError):
        return

    brake_status_shared.value = brake_result['status']
    brake_level_shared.value = brake_result['level']

start_pressing_waysw = False
def syncMascon(mascon_value, mascon_shared, way_shared):
    global start_pressing_waysw
    mascon_level, way = Mascon.formatValue(mascon_value)
        
    # 不正値の読み飛ばし(0-14)
    if not mascon_level in range(15):
        return
    mascon_shared.value = mascon_level
    way_shared.value = way
    
if __name__ == '__main__':
    hid = HID('/dev/de15_hid')
    while True:        
        print(hid.readSerial())
