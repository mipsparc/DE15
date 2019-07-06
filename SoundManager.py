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
        self.last_mascon_level = 0
        # 最後にジョイントを先頭の車輪が通過したUNIX TIME
        self.last_joint = time.time()
        # 最後にジョイントを前の車輪が通過したUNIX TIME
        self.last_wheel = 0
        # 特定のジョイントを通過した車輪の数
        self.joint_count = 0
        self.last_run = False
        
        # 頻繁に鳴る音はボリュームを合わせて1.0を超えないようにする
        self.run_max_volume = 0.2
        self.s.power.volume(0.3)
        self.s.joint.volume(0.3)
        self.s.switch.volume(0.2)
        self.s.idle.volume(0.2)
        self.s.idle.play()

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

    def switch(self, way):
        if self.last_way != way:
            self.last_way = way
            self.s.switch.play()
            
    def power(self, mascon_level):
        if mascon_level == 0:
            self.s.power.stop()
        elif mascon_level != self.last_mascon_level:
            self.s.power.stop()
            self.s.power.play(math.floor((mascon_level - 1) / 2.0))
        self.last_mascon_level = mascon_level
