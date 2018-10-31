#coding:utf-8
import Sounder
import time

s = Sounder.Sounder()

play = False

while True:
    input()
    if not play:
        print("発車メロディplaying... Enterで停止")
        s.dream.play(0)
        play = True
    else:
        s.dream.stop(0)
        time.sleep(0.3)
        s.DoorAnnounce()
        time.sleep(5)
        print("発車メロディstopped... Enterで再生")
        play = False
