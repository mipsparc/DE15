#coding:utf-8

import serial

# マスコン装置とシリアル伝送で通信して、マスコンのノッチを取得する
class ReadMascon:
    def __init__(self, device):
        # timeoutを設定することで通信エラーを防止する
        self.ser = serial.Serial(device, timeout=0.3, baudrate=9600 )
        #buttons = -1;

    def waitAndGetMascon(self):
        self.ser.reset_input_buffer()
        r = self.ser.read()

        mascon_level = ord(r) & 0b00001111 # 下位4bit
        try:
            return int(mascon_level)
        except ValueError:
            return False
        
        #buttons_new = ord(r) >> 4
        #if buttons_new != buttons:
            #buttons = buttons_new
            #print('ボタン状態: ' + bytes(buttons))
                
# シリアル通信プロセスのワーカー
def Worker(mascon_shared, device):    
    mascon = ReadMascon(device)
    while True:
        mascon_level = mascon.waitAndGetMascon()
        if mascon_level is False:
            continue
        if mascon_level < 0 or 14 < mascon_level:
            continue
        mascon_shared.value = mascon_level
        
if __name__ == '__main__':
    mascon = ReadMascon('/dev/mascon')
    while True:
        print(mascon.waitAndGetMascon())
