#coding:utf-8

# DesktopStation DSair2への接続ライブラリ

import serial
import time

class DSair2:
    MAX_SPEED = 800
    
    # 3 はデフォルトアドレス
    LOCO_DEFAULT_ADDR = 49152
    
    # ライトファンクション番号
    LIGHT_FUNC_NUM = 0
    
    def __init__(self, port, is_dcc, addr):
        self.is_dcc = is_dcc
        
        self.ser = serial.Serial(port, baudrate=115200, timeout=0.1, write_timeout=0.1, inter_byte_timeout=0.1)
        # DSair2を再起動
        self.send('reset()')
        time.sleep(1)

        self.ser.reset_input_buffer()
        self.send('setPing()')
        time.sleep(1)
        init_response = self.ser.read(200)
        print(init_response)
        if (not init_response.decode('ascii').endswith('200 Ok\r\n')
            and not init_response.decode('ascii').endswith('100 Ready\r\n')
        ):
            print('DSair2を正常に認識できませんでした。終了します')
            raise ValueError('DSair2認識エラー')
        else:
            print('DSair2を正常に認識しました。')

        if is_dcc:
            self.loco_addr = self.LOCO_DEFAULT_ADDR + addr
            self.last_loco_light = False
            # DCC初期化
            self.send('setPower(1)')
            time.sleep(0.5)
            poweron_response = self.ser.read(50)
            print(poweron_response)
            self.ser.reset_input_buffer()
            
            self.send('setPower(1)')
            time.sleep(0.5)
            poweron_response = self.ser.read(50)
            print(poweron_response)
            self.ser.reset_input_buffer()
        else:
            self.send('setPower(0)')
            time.sleep(0.3)
            self.send('setPower(0)')
            time.sleep(0.3)
            self.send('setPower(0)')
            time.sleep(0.3)
            self.ser.reset_input_buffer()

        print('DSair2 起動完了')
        
        self.last_out_speed = 0
        self.last_way = -1
        
    def move(self, speed_level, way):
        if self.is_dcc:
            self.move_dcc(speed_level, way)
        else:
            self.move_dc(speed_level, way)
        
    def turnOnLight(self):
        if not self.last_loco_light:
            self.last_loco_light = True
            self.send(f'setLocoFunction({self.loco_addr},{self.LIGHT_FUNC_NUM},1)')
        
    def turnOffLight(self):
        if self.last_loco_light:
            self.last_loco_light = False
            self.send(f'setLocoFunction({self.loco_addr},{self.LIGHT_FUNC_NUM},0)')
        
    # 速度や方向などの状態が変わるときのみ命令を出力する
    def move_dcc(self, speed_level, way):
        if self.last_way != way and way == 0:
            self.turnOffLight()
        elif self.last_way != way:
            self.turnOnLight()
        
        if speed_level > 0 and way != 0:
            out_speed = int(speed_level)
        else:
            # 仮想的な方向 0(切)
            out_speed = 0
        
        if out_speed > self.MAX_SPEED:
            out_speed = self.MAX_SPEED
        if out_speed < 0:
            out_speed = 0
        
        if out_speed != self.last_out_speed:
            self.last_out_speed = out_speed
            self.send(f'setLocoSpeed({self.loco_addr},{out_speed},2)')
        
        if way != self.last_way:
            self.last_way = way
            # 仮想的な方向 0(切) は送信しない
            if way != 0:
                self.send(f'setLocoDirection({self.loco_addr},{way})')
    
    # DC駆動用
    def move_dc(self, speed_level, way):
        if speed_level > 0 and way != 0:
            out_speed = int(speed_level)
        else:
            # 仮想的な方向 0(切)
            out_speed = 0
        
        if out_speed > self.MAX_SPEED:
            out_speed = self.MAX_SPEED
        if out_speed < 0:
            out_speed = 0
        
        if way != self.last_way:
            self.last_way = way
            
        if out_speed != self.last_out_speed:
            self.last_out_speed = out_speed
            self.send(f'DC({out_speed},{way})\n')
    
    # 最終的にコマンドを送信する関数
    def send(self, value):
        self.ser.reset_input_buffer()
        self.ser.write(value.encode('ascii') + b'\n')
        self.ser.flush()

if __name__ == '__main__':
    dsair2 = DSair2('/dev/dsair2', True, 3)
    while True:
        level = int(input('level> '))
        dsair2.move(level, 2)
