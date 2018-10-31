#coding:utf-8
import Sounder

s = Sounder.Sounder()
play = False

while True:
    input()
    if not play:
        print("断続音playing... Enterで停止")
        s.irekae.play(0)
        play = True
    else:
        print("断続音stopped... Enterで再生")
        s.irekae.stop(0)
        play = False
