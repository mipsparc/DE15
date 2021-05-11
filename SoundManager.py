#encoding: utf-8

import Sounder
import time
import math

class SoundManager:
    def __init__(self):
        self.s = Sounder.Sounder()
        self.last_brake = False
        self.last_bc = 0
        self.last_way = 0
        self.power_num = 99 # dummy
        # 最後にジョイントを先頭の車輪が通過したUNIX TIME
        self.last_joint = time.time()
        # 最後にジョイントを前の車輪が通過したUNIX TIME
        self.last_wheel = 0
        # 特定のジョイントを通過した車輪の数
        self.joint_count = 0
        self.last_run = False
        self.hone_state = 0
        self.hone_time = 0
        
        # 頻繁に鳴る音はボリュームを合わせて1.0を超えないようにする
        self.run_max_volume = 0.3
        self.s.power.volume(0.3)
        self.s.joint.volume(0.8)
        self.s.brake.volume(0.5)
        self.s.brake_fadeout.volume(0.5)
        self.s.hone_start.volume(0.7)
        self.s.hone_mid.volume(0.7)
        self.s.hone_end.volume(0.7)
        self.s.start.volume(0.7)

    def brake(self, bc):
        if (not self.last_brake) and bc != self.last_bc:
            self.last_brake = True
            self.s.brake.play()
        elif self.last_brake and bc == self.last_bc:
            self.last_brake = False
            self.s.brake.stop()
            self.s.brake_fadeout.play()
        self.last_bc = bc

    def joint(self, speed):
        if speed < 0.1:
            return
        
        # レール長
        rail_length = 25.0
        interval = rail_length / speed
        # 車輪間の距離
        wheel_distance = 1.2
        interval_wheel = wheel_distance / speed
        
        # DE10なので5軸+ダミー1軸
        wheel_count = 6
        # 最後のジョイントから時間が経っていれば、先頭の車輪が次のジョイントに到達
        now = time.time()
        if self.last_joint + interval < now:
            self.joint_count = 1
            self.last_joint = now
            self.last_wheel = now
            self.s.joint.play()
        
        if self.joint_count > 0:
            if self.last_wheel + interval_wheel < now:
                self.joint_count += 1
                self.last_wheel = now
                # 3軸目にダミーを入れる
                if self.joint_count != 3:
                    self.s.joint.play()
                if self.joint_count >= wheel_count:
                    self.joint_count = 0

    def run(self, speed):
        if not self.last_run and speed > 0.1:
            self.s.run.play()
            self.last_run = True
        elif speed < 0.1:
            self.s.run.stop()
            self.last_run = False
            return

        self.s.run.volume(min(speed / 15 * self.run_max_volume, self.run_max_volume))
            
    def dingBell(self):
        self.s.ding_bell.play()
        
    def startEngine(self):
        self.s.start.play()
            
    def hone(self, hone):
        if self.hone_state == 0:
            if hone:
                self.hone_time = time.time()
                self.s.hone_start.play()
                self.hone_state = 1
        elif self.hone_state == 1:
            if self.hone_time + self.s.hone_start.length() - 0.18 <= time.time():
                self.s.hone_start.stop()
                self.s.hone_mid.play()
                self.hone_state = 2
        elif self.hone_state == 2:
            if not hone:
                self.s.hone_mid.stop()
                self.s.hone_end.play()
                self.hone_time = time.time()
                self.hone_state = 3
        elif self.hone_state == 3:
            if self.hone_time + 0.2 <= time.time():
                self.hone_state = 0
            
    def power(self, mascon_level):        
        if mascon_level in (0, 1):
            num = 0
        elif mascon_level >= 11:
            num = 10
        else:
            num = mascon_level - 1

        if num != self.power_num:
            self.s.power.stop()
            self.power_num = num
            self.s.power.play(num)
        
