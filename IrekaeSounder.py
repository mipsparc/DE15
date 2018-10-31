#coding:utf-8
import Sounder

s = Sounder.Sounder()
play = False

while True:
    input()
    if not play:
        print("断続音playing...")
        s.irekae.play(0)
        play = True
    else:
        print("断続音stopped")
        s.irekae.stop(0)
        play = False
