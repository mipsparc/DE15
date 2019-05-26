#coding:utf-8
import pygame
import time

class Sounder:
    def __init__(self):
        pygame.mixer.init(44100, -16, 1, 256)
        self.idle = Sounds(['sound/idle.wav'])
        self.idle.volume(0.7)
        self.switch = Sounds(['sound/switch.wav'], False)
        self.brake = Sounds(['sound/brake.wav'])
        self.run = Sounds([
            'sound/run0.wav',
            'sound/run1.wav',
            'sound/run2.wav',
            'sound/run3.wav',
            'sound/run4.wav',
            'sound/run5.wav',
        ])
        self.run.volume(0.8)
        self.power = Sounds([
            'sound/power1.wav',
            'sound/power2.wav',
            'sound/power3.wav',
        ])
        self.power.volume(0.7)

class Sounds:
    def __init__(self, paths, loop=True):
        self.sound = []
        self.loop = loop
        for path in paths:
            self.sound.append(pygame.mixer.Sound(path))
            
    def play(self, num):
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
