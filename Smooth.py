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
        # 角度の都合上
        [0, 1300],
        [280, 1300],
        [440, 1600],
        [470, 1660],
        [490, 1690],
        [999, 1690],
        [999.9, None], #dummy
    ]
    
class ER(Smooth):
    # ER, サーボusのプロファイル
    PROFILE = [
        [0, 2000],
        [370, 1000],
        [490, 720],
        [999, 700],
        [999.9, None], #dummy
    ]

class SpeedMeter(Smooth):
    # kph, levelのプロファイル
    PROFILE = [
        [0.0, 0.0],
        [22.0, 1000.0],
        [32.5, 1500.0],
        [43.0, 2000.0]
        [48.0, 2500.0],
        [63.0, 3000.0],
        [73.0, 3500.0],
        [82.0, 4000.0],
        [150.0, 4000.0],
        [999.9, None], #dummy
    ]
