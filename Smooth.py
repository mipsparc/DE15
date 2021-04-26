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
        [40.0, 350.0],
        [80.0, 700.0],
        [120.0, 1050.0],
        [999.9, None], #dummy
    ]
