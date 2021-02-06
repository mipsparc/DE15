#coding:utf-8

class Smooth:  
    @classmethod
    def getValue(self, value):        
        for i, p in enumerate(self.PROFILE):
            if p[0] > value:
                # 1次関数を求める
                tilt = (p[1] - self.PROFILE[i-1][1]) / (p[0] - self.PROFILE[i-1][0])
                b = p[1] - tilt * p[0]
                return int(tilt * value + b)

class Pressure(Smooth):
    # BC, サーボusのプロファイル
    PROFILE = [
        [0.0, 0.0],
        [100.0, 750.0],
        [200.0, 1500.0],
        [999.9, None], #dummy
    ]

class SpeedMeter(Smooth):
    # kph, levelのプロファイル
    PROFILE = [
        [0.0, 0.0],
        [10.0, 30.0],
        [150.0, 1024.0],
        [999.9, None], #dummy
    ]
