#coding:utf-8
import pygame
import time

class Sounder:
    def __init__(self):
        pygame.mixer.init(44100, -16, 1, 256)
        self.switch = Sounds(['sound/switch.wav'], False)
        self.brake = Sounds(['sound/brake.wav'])
        self.brake_fadeout = Sounds(['sound/brake_fadeout.wav'],False)
        self.power = Sounds([
            'sound/1_or_idle.wav',
            'sound/2.wav',
            'sound/3.wav',
            'sound/4.wav',
            'sound/5.wav',
            'sound/6.wav',
            'sound/7.wav',
            'sound/8.wav',
            'sound/9.wav',
            'sound/10.wav',
            'sound/11.wav',
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
