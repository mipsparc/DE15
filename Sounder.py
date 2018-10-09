#coding:utf-8
import pygame

class Sounder:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()
        self.idle = pygame.mixer.Sound('sound/idle.wav')
        self.idle.set_volume(1)
        self.switch = pygame.mixer.Sound('sound/switch.wav')
        self.brake = pygame.mixer.Sound('sound/brake.wav')
        self.hone = pygame.mixer.Sound('sound/hone.wav')
        self.run = pygame.mixer.Sound('sound/run.wav')
        self.run.set_volume(0.3)
        self.power1 = pygame.mixer.Sound('sound/power1.wav')
        self.power2 = pygame.mixer.Sound('sound/power2.wav')
        self.power3 = pygame.mixer.Sound('sound/power3.wav')

        
    def Hone(self):
        self.hone.play()
    
    def Switch(self):
        self.switch.play()
        
    def Idle(self, stop=False):
        if not stop:
            self.idle.play(loops=-1)
        else:
            self.idle.stop()
        
    def Run(self, stop=False):
        if not stop:
            self.run.play(loops=-1)
        else:
            self.run.stop()
            
    def Brake(self, stop=False):
        if not stop:
            self.brake.play(loops=-1)
        else:
            self.brake.stop()
        
    def Power1(self, stop=False):
        if not stop:
            self.power1.play(loops=-1)    
        else:
            self.power1.stop()
        
    def Power2(self, stop=False):
        if not stop:
            self.power2.play(loops=-1)
        else:
            self.power2.stop()
        
    def Power3(self, stop=False):
        if not stop:
            self.power3.play(loops=-1)
        else:
            self.power3.stop()
        
