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
        
    def move(self, speed):
        """
        PWMコントローラへは "!" ~ "\xff"までを渡す
        
        Parameters
        ----------
        speed : int
            実際の鉄道車両の速度(m/s)
        """
        # 動き始める速度
        base_power = 42
        
        #出力値の傾き
        magnify_1 = 1.0
        magnify_2 = 0.5
        
        #傾きが変化する閾値
        criteria = 5.5
        
        #1次関数を2つ繋げる
        if speed < 5.5:
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
        self.device.write(output_power)
