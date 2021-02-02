#coding:utf-8

import serial
from enum import IntEnum
import sys

class BrakeStatues(IntEnum):
    ERROR_SENSOR = 1
    ERROR = 2
    EMER = 3
    FIX = 4
    MAX_BRAKE = 5
    BRAKE = 6
    RUN = 7
    LOWER_BRAKE = 8
    
class BrakeStatusUtil:
    NAMES = {
        BrakeStatues.ERROR_SENSOR: 'センサー通信エラー',
        BrakeStatues.ERROR: 'センサー値異常',
        BrakeStatues.EMER: '非常',
        BrakeStatues.FIX: '固定',
        BrakeStatues.MAX_BRAKE: '全ブレーキ',
        BrakeStatues.BRAKE: 'ブレーキ',
        BrakeStatues.RUN: '運転',
        BrakeStatues.LOWER_BRAKE: 'ユルメ',
    }
    
    @classmethod
    def statusIdToName(self, status_id):
        return self.NAMES[status_id]

    @classmethod
    def statusIdToEnum(self, status_id):
        for e in self.NAMES.keys():
            if status_id == e.value:
                return e

class DE15Brake:
    def __init__(self, device):
        # timeoutを設定することで通信エラーを防止する
        try:
            self.ser = serial.Serial(device, timeout=0.3, write_timeout=0.3, inter_byte_timeout=0.3, baudrate=9600)
        except serial.serialutil.SerialException:
            print('正常にシリアルポートを開けませんでした。')
            raise
        
        self.fix_value = self.read()
        self.value = self.fix_value # 初期値は固定位置のデータにしておく
        self.status = BrakeStatues.FIX

    # intで出力する
    def read(self):
        try:
            raw_value = self.ser.readline()
            self.ser.reset_input_buffer()
            raw_value = raw_value.decode('ascii')
            raw_value = raw_value.replace('\r\n', '')
            return int(float(raw_value))
        except KeyboardInterrupt:
            exit()
        except:
            return False

    def valueToStatus(self, brake_value):
        if brake_value == False:
            return BrakeStatues.ERROR_SENSOR
        elif brake_value < 5500:
            return BrakeStatues.ERROR
        # 階ユルメ
        elif brake_value < 5760:
            return BrakeStatues.EMER
        elif brake_value < 5800:
            return BrakeStatues.FIX
        elif brake_value < 5830:
            return BrakeStatues.MAX_BRAKE
        elif brake_value < 6100:
            return BrakeStatues.BRAKE
        elif brake_value < 6130:
            return BrakeStatues.RUN
        elif brake_value < 6230:
            return BrakeStatues.LOWER_BRAKE

        return BrakeStatues.ERROR
        
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
        
    def syncSharedMem(self):
        value = self.read()
        self.status = self.valueToStatus(value)
        
        # 異常時には状態表示をする
        if self.status in (BrakeStatues.ERROR, BrakeStatues.ERROR_SENSOR):
            print(BrakeStatusUtil.statusIdToName(self.status))
            print(value)

        self.brake_level = 0
        if self.status == BrakeStatues.BRAKE:
            self.brake_level = self.getBrakeLevel(value, 5830, 6100)
            
        return {'status': self.status.value, 'level': self.brake_level}
    
    def getBrakeLevel(self, value, max_brake, brake):
        return 1 - (float(value) - max_brake) / (brake - max_brake)
    
# シリアル通信プロセスのワーカー
def Worker(brake_status_shared, brake_level_shared, device):
    brake = DE15Brake('/dev/ttyACM0')
    while True:
        try:
            result = brake.syncSharedMem()
            # 不正値の読み飛ばし
            if (result['status'] == BrakeStatues.ERROR_SENSOR or result['status'] == BrakeStatues.ERROR):
                continue;
            brake_status_shared.value = result['status']
            brake_level_shared.value = result['level']
            # brake.setSpeed(speed_shared.value)
        except serial.serialutil.SerialException:
            raise
        # できる限りエラーは無視する
        except Exception as e:
            print(e, file=sys.stderr)
            pass

if __name__ == '__main__':
    brake = DE15Brake('/dev/ttyACM0')
    while True:
        print(brake.syncSharedMem())
