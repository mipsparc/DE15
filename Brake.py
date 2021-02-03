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
    @staticmethod
    def valueToStatus(brake_value):
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
    
    @staticmethod
    def getBrakeLevel(value, max_brake, brake):
        return 1 - (float(value) - max_brake) / (brake - max_brake)
        
    @classmethod
    def formatValue(self, value):
        status = self.valueToStatus(value)
        
        # 異常時には状態表示をする
        if status in (BrakeStatues.ERROR, BrakeStatues.ERROR_SENSOR):
            print(BrakeStatusUtil.statusIdToName(status))
            print(value)
            return False

        brake_level = 0
        if status == BrakeStatues.BRAKE:
            brake_level = self.getBrakeLevel(value, 5830, 6100)
            
        return {'status': status.value, 'level': brake_level}
