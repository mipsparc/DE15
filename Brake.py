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
        return self.getNames(status_id)

class DE15Brake:
    @staticmethod
    def valueToStatus(brake_value):
        if brake_value == False:
            return BrakeStatues.ERROR_SENSOR
        # 以下のパラメータを修正したら、formatValueのbrake_level導出箇所も修正する
        elif brake_value < 5500:
            return BrakeStatues.ERROR
        # 階ユルメ
        elif brake_value < 5760:
            return BrakeStatues.EMER
        elif brake_value < 5800:
            return BrakeStatues.FIX
        elif brake_value < 5830:
            return BrakeStatues.MAX_BRAKE
        elif brake_value < 6070:
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
            print(BrakeStatues.statusIdToName(status))
            print(value)
            return False

        brake_level = 0
        if status == BrakeStatues.BRAKE:
            brake_level = self.getBrakeLevel(value, 5830, 6070)
            
        return {'status': status.value, 'level': brake_level}
