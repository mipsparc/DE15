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

class SpeedMeter(Smooth):
    # kph, levelのプロファイル
    PROFILE = [
        [0.0, 0.0],
        [3.0, 100.0],
        [7.0, 250.0],
        [14.0, 500.0],
        [20.0, 750.0],
        [23.0, 1000.0],
        [39.0, 1500.0],
        [49.0, 2000.0],
        [60.0, 2500.0],
        [72.0, 3000.0],
        [84.0, 3500.0],
        [89.0, 3750.0],
        [150.0, 4000.0],
        [999.9, None], #dummy
    ]
