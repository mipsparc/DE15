#encoding: utf-8

import Sounder

class SoundManager:
    def __init__(self):
        self.s = Sounder.Sounder()
        self.last_brake = False
        self.last_bc = 0
        self.last_way = 0
        self.last_kph = 0
        self.last_mascon_level = 0

    def brake(self, bc):
        if (not self.last_brake) and bc != self.last_bc:
            self.last_brake = True
            self.last_bc = bc
            self.s.brake.play(0)
        elif self.last_brake and bc == self.last_bc:
            self.last_brake = False
            self.s.brake.stop()

    def switch(self, way):
        if self.last_way != way:
            self.last_way = way
            self.s.switch.play(0)
        
    def run(self, kph):
        if kph == 0:
            self.s.run.stop()
        if 0 < kph < 15  and not(0 < self.last_kph < 15):
            self.s.run.stop()
            self.s.run.play(0)
        if 15 <= kph < 25  and not (15 <= self.last_kph < 25):
            self.s.run.stop()
            self.s.run.play(1)
        if 25 <= kph < 35  and not (25 <= self.last_kph < 35):
            self.s.run.stop()
            self.s.run.play(2)
        if 35 <= kph < 45  and not (35 <= self.last_kph < 45):
            self.s.run.stop()
            self.s.run.play(3)
        if 45 <= kph < 65  and not (45 <= self.last_kph < 65):
            self.s.run.stop()
            self.s.run.play(4)
        if 65 <= kph  and not(65 <= self.last_kph):
            self.s.run.stop()
            self.s.run.play(5)
        self.last_kph = kph
            
    def power(self, mascon_level):
        if mascon_level == 0:
            self.s.power.stop()
        if 1 <= mascon_level < 5 and (self.last_mascon_level == 0 or 5 <= self.last_mascon_level):
            self.s.power.stop()
            self.s.power.play(0)
        elif 5 <= mascon_level < 10 and (self.last_mascon_level < 5 or 10 <= self.last_mascon_level):
            self.s.power.stop()
            self.s.power.play(1)
        elif 10 <= mascon_level < 14 and (self.last_mascon_level < 10 or 14 <= self.last_mascon_level):
            self.s.power.stop()
            self.s.power.play(2)
        self.last_mascon_level = mascon_level
