#encoding: utf-8

import serial

class Controller:
    """
    鉄道車両の動く速度(m/s)を受け取って、自作のPWMコントローラへ動く命令をするモジュール
    """
    def __init__(self, device):
        # 2回に一回書き込む
        self.write_count = False
        self.device = serial.Serial(device, baudrate=9600)
        self.way = 1
        
    def move(self, speed, way, honsen):
        """
        PWMコントローラへは走行時は "!" ~ "\xff"までを渡す
        
        Parameters
        ----------
        speed : int
            実際の鉄道車両の速度(m/s)
        way : int
            方向 0切, 1位, 2位
        honsen: bool
            Falseであれば低速性能を強化する
        """
        
        # 切
        if way == 0:
            speed = 0
        
        # 方向転換
        if way != self.way and way != 0:
            self.way = way
            self._write(bytes([ord('\n')]))
            return
        
        # 動き始める速度
        if honsen:
            base_power = 40
        else:
            base_power = 35
        
        #出力値の傾き
        magnify_1 = 1.0
        magnify_2 = 0.7
        
        #傾きが変化する閾値
        criteria = 5.5
        
        #1次関数を2つ繋げる
        if speed < criteria:
            output_power = (speed * magnify_1) + base_power
        else:
            output_power = (speed * magnify_2) + (criteria * magnify_1) + base_power
            
        if (output_power + base_power) > 255:
            output_power = 255 - base_power
        
        if self.write_count == True:
            self.write_count = False
            if speed <= 0:
                self._write(bytes([ord('!')]))
            else:
                self._write(bytes([ord('!') + int(output_power)]))

            print(str(speed * 3600 / 1000) + 'km/h')
        else:
            self.write_count = True
            
    def _write(self,output_power):
        # 2回連続でないと受領しないため、3回連続で送る
        self.device.write(output_power * 3)
