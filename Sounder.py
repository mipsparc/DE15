#coding:utf-8
import pygame

class Sounder:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()
        self.idle = LoopSounds(['sound/idle.wav'])
        self.idle.volume(0.4)
        self.switch = pygame.mixer.Sound('sound/switch.wav')
        self.brake = LoopSounds(['sound/brake.wav'])
        self.hone = pygame.mixer.Sound('sound/hone.wav')
        self.run = LoopSounds([
            'sound/run0.wav',
            'sound/run1.wav',
            'sound/run2.wav',
            'sound/run3.wav',
            'sound/run4.wav',
            'sound/run5.wav',
        ])
        self.power = LoopSounds([
            'sound/power1.wav',
            'sound/power2.wav',
            'sound/power3.wav',
        ])
        self.power.volume(0.4)
        self.irekae = LoopSounds(['sound/irekae.wav'])
        self.sekkin = pygame.mixer.Sound('sound/sekkin.wav')
        self.dream = LoopSounds(['sound/dream_park.wav'])
        self.door_announce = pygame.mixer.Sound('sound/door_announce.wav')
        
    def Hone(self):
        self.hone.play()
    
    def Switch(self):
        self.switch.play()
        
    def Sekkin(self):
        self.sekkin.play()
        
    def DoorAnnounce(self):
        self.door_announce.play()

class LoopSounds:
    def __init__(self, paths):
        self.sound = []
        for path in paths:
            self.sound.append(pygame.mixer.Sound(path))
        
    def stopAll(self):
        for stop_num in range(len(self.sound)):
            self.stop(stop_num)
            
    def play(self, num):
        self.sound[num].play(loops=-1)
        
    def stop(self, num):
        self.sound[num].stop()
        
    def volume(self, v):
        for s in self.sound:
            s.set_volume(v)
