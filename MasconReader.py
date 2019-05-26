#coding:utf-8

import serial

class ReadMascon:
    def __init__(self, device):
        self.ser = serial.Serial(device, baudrate=9600)
        #buttons = -1;

    def waitAndGetMascon(self):
        self.ser.reset_input_buffer()
        r = self.ser.read()

        mascon_level = ord(r) & 0b00001111 # 下位4bit
        try:
            return int(mascon_level)
        except ValueError:
            return 0
        
        #buttons_new = ord(r) >> 4
        #if buttons_new != buttons:
            #buttons = buttons_new
            #print('ボタン状態: ' + bytes(buttons))
                
def Worker(mascon_shared, device):    
    mascon = ReadMascon(device)
    while True:
        mascon_level = mascon.waitAndGetMascon()
        mascon_shared.value = mascon_level
        
if __name__ == '__main__':
    mascon = ReadMascon('/dev/mascon')
    while True:
        print(mascon.waitAndGetMascon())
