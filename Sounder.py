#coding:utf-8
import pygame
import time

class Sounder:
    def __init__(self):
        pygame.mixer.init(44100, -16, 1, 256)
        self.idle = Sounds(['sound/idle.wav'])
        self.switch = Sounds(['sound/switch.wav'], False)
        self.brake = Sounds(['sound/brake.wav'])
        self.brake_fadeout = Sounds(['sound/brake_fadeout.wav'],False)
        self.power = Sounds([
            'sound/power_1_2.wav',
            'sound/power_3_4.wav',
            'sound/power_5_6.wav',
            'sound/power_7_8.wav',
            'sound/power_9_10.wav',
            'sound/power_11_12.wav',
            'sound/power_13_14.wav',
        ])
        self.joint = Sounds(['sound/joint.wav'], False)
        self.run = Sounds(['sound/run.wav'])

class Sounds:
    def __init__(self, paths, loop=True):
        self.sound = []
        self.loop = loop
        for path in paths:
            self.sound.append(pygame.mixer.Sound(path))
            
    def play(self, num=0):
        if self.loop:
            self.sound[num].play(loops=-1)
        else:
            self.sound[num].play()
        
    def stop(self):
        for sound in self.sound:
            sound.stop()
        
    def volume(self, v):
        for s in self.sound:
            s.set_volume(v)
