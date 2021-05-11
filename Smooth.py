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
        [0, 1530],
        [70, 1490],
        [350, 1460],
        [999, 1461],
        [999.9, None], #dummy
    ]
    
class BCToLeft(Smooth):
    # 左回りのBC, サーボusのプロファイル
    PROFILE = [
        [0, 1580],
        [80, 1560],
        [210, 1540],
        [350, 1460],
        [999, 1461],
        [999.9, None], #dummy
    ]
    
class BP(Smooth):
    # BP, サーボusのプロファイル
    PROFILE = [
        [0, 1750],
        [360, 1750],
        [500, 1680],
        [999, 1680],
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
