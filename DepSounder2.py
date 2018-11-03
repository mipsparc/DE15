#coding:utf-8
import Sounder
import time

s = Sounder.Sounder()

play = False

while True:
    input()
    if not play:
        print("See you again playing... Enterで停止")
        s.dep.play(0)
        play = True
    else:
        s.dep.stop(0)
        time.sleep(0.3)
        s.DoorAnnounce()
        time.sleep(5)
        print("See you again stopped... Enterで再生")
        play = False
