#coding:utf-8
import pygame
import time

class Sounder:
    def __init__(self):
        pygame.mixer.init(44100, -16, 1, 256)
        self.idle = Sounds(['sound/idle.wav'])
        self.idle.volume(0.2)
        self.switch = Sounds(['sound/switch.wav'], False)
        self.switch.volume(0.2)
        self.brake = Sounds(['sound/brake.wav'])
        self.brake_fadeout = Sounds(['sound/brake_fadeout.wav'],False)
        self.power = Sounds([
            'sound/power1.wav',
            'sound/power2.wav',
            'sound/power3.wav',
        ])
        self.power.volume(0.6)
        self.joint = Sounds(['sound/joint.wav'], False)
        self.joint.volume(0.4)

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
