import serial

class Meter:
    def __init__(self, device):
        self.device = serial.Serial(device, baudrate=9600)
        self.last_angle = 0
        self.send_count = 0
    def send(self, bc):
        # 出力70のときにBC_MAX 3
        angle = int(bc * 23)
        
        if angle == self.last_angle:
            return;        
        last_angle = angle
        
        if self.send_count == 1:
            self.send_count = 0
            # 0ぴったりだと振動してしまうので加算する
            self._write(bytes([ord('!') + 5 + int(angle)]))
        else:
            self.send_count += 1
        
    def _write(self,output_power):
        # 2回連続でないと受領しないため、3回連続で送る
        self.device.write(output_power * 3)
        
if __name__ == '__main__':
    meter = Meter('/dev/meter')
    while True:
        bc = int(input('bc>'))
        meter.send(bc)
