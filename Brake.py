#coding:utf-8

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
    
    @classmethod
    def getNames(self):
        return {
            self.ERROR_SENSOR: 'センサー通信エラー',
            self.ERROR: 'センサー値異常',
            self.EMER: '非常',
            self.FIX: '固定',
            self.MAX_BRAKE: '全ブレーキ',
            self.BRAKE: 'ブレーキ',
            self.RUN: '運転',
            self.LOWER_BRAKE: 'ユルメ',
        }
    
    @classmethod
    def statusIdToName(self, status_id):
        return self.getNames()[status_id]

class DE15Brake:
    # 起動時に固定位置と全ブレーキの間にして、初期化する
    @classmethod
    def setRefValue(self, ref_value):
        self.ref_value = int(ref_value)
        self.max_brake_diff = 45
        self.brake_diff = 293
    
    @classmethod
    def valueToStatus(self, brake_value):
        if brake_value == False:
            return BrakeStatues.ERROR_SENSOR
        elif brake_value < self.ref_value - 240:
            return BrakeStatues.ERROR
        # 階ユルメ
        elif brake_value < self.ref_value - 70:
            return BrakeStatues.EMER
        elif brake_value < self.ref_value:
            return BrakeStatues.FIX
        elif brake_value < self.ref_value + self.max_brake_diff:
            return BrakeStatues.MAX_BRAKE
        elif brake_value < self.ref_value + self.brake_diff:
            return BrakeStatues.BRAKE
        elif brake_value < self.ref_value + 330:
            return BrakeStatues.RUN
        elif brake_value < self.ref_value + 420:
            return BrakeStatues.LOWER_BRAKE

        return BrakeStatues.ERROR
    
    @staticmethod
    def getBrakeLevel(value, max_brake, brake):
        return 1 - (float(value) - max_brake) / (brake - max_brake)
        
    @classmethod
    def formatValue(self, value):
        status = self.valueToStatus(value)
                
        # 異常時には状態表示をする
        if status in (BrakeStatues.ERROR, BrakeStatues.ERROR_SENSOR):
            return False

        brake_level = 0
        if status == BrakeStatues.BRAKE:
            brake_level = self.getBrakeLevel(value, self.ref_value + self.max_brake_diff, self.ref_value + self.brake_diff)
            
        return {'status': status.value, 'level': brake_level}
