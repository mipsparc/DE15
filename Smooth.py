#coding:utf-8

class Smooth:  
    @classmethod
    def getValue(self, value):        
        for i, p in enumerate(self.PROFILE):
            if p[0] > value:
                # 1次関数を求める
                tilt = (p[1] - self.PROFILE[i-1][1]) / (p[0] - self.PROFILE[i-1][0])
                b = p[1] - tilt * p[0]
                output = int(tilt * value + b)
                return output

class Speed(Smooth):
    # kph, DSAir指令値のプロファイル
    PROFILE = [
        [0.0, 0],
        [5.0, 30],
        [15.0, 100],
        [20.0, 200],
        [30.0, 300],
        [40.0, 400],
        [50.0, 500],
        [60.0, 600],
        [90.0, 900],
        [180.0, 950],
        [999.9, None], #dummy
    ]

class BCToRight(Smooth):
    # 右回りのBC, サーボusのプロファイル
    PROFILE = [
        [0, 950],
        [160, 1000],
        [280, 1030],
        [350, 1050],
        [999, 1030],
        [999.9, None], #dummy
    ]
    
class BCToLeft(Smooth):
    # 左回りのBC, サーボusのプロファイル
    PROFILE = [
        [0, 910],
        [50, 970],
        [120, 990],
        [335, 1030],
        [999, 1030],
        [999.9, None], #dummy
    ]
    
class BP(Smooth):
    # BP, サーボusのプロファイル
    PROFILE = [
        [0, 1510],
        # 計算の都合上
        [200, 1510],
        [440, 1600],
        [470, 1660],
        [490, 1690],
        [999, 1690],
        [999.9, None], #dummy
    ]
    
class ERToRight(Smooth):
    # 右回りのER, サーボusのプロファイル
    PROFILE = [
        [0, 1700],
        [200, 1700],
        [380, 1600],
        [425, 1550],
        [490, 1485],
        [999, 1485],
        [999.9, None], #dummy
    ]

class ERToLeft(Smooth):
    # 左回りのER, サーボusのプロファイル
    PROFILE = [
        [0, 1750],
        [200, 1750],
        [420, 1700],
        [480, 1639],
        [999, 1640],
        [999.9, None], #dummy
    ]

class SpeedMeter(Smooth):
    # kph, levelのプロファイル
    PROFILE = [
        [0.0, 0.0],
        [10.0, 400.0],
        [40.0, 1600.0],
        [85.0, 3400.0],
        [120.0, 4000.0],
        [999.9, None], #dummy
    ]
