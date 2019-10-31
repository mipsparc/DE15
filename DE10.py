#coding:utf-8
import math

class DE10:
    def __init__(self):
        # 車速(m/s)
        self.speed = 0
        self.mascon_level = 0
        # 最大ブレーキシリンダ圧力 本物は5.7kg/cm2
        self.BC_MAX = 3.0
        # ブレーキシリンダ圧力(減速度)
        self.bc = self.BC_MAX
        # ブレーキレバー位置(ブレーキシリンダ圧力に作用)
        self.brake_level = 0
        #非常ブレーキ状態
        self.eb = False
        #貨車牽引時の加速度減少(単機: 1)
        self.freight = 0.9
        #統合モジュールのボタン状態(intでビット列)
        # 初期値は前進、本線、鍵ON
        self.buttons = 0b01000000 + 0b00010000 + 0b00001000
        # クラッチがつながっているか
        self.clutch = True
        
    def getSmoothLevel(self):
        # y = log2(x+1) 最大が1
        return (math.log2(self.mascon_level+1))/4.0

    # 0.1秒進める
    def advanceTime(self):
        # 加速度を求める(m/s2)
        if self.speed < 3.33:
            accel = self.getSmoothLevel() * 0.803
        elif self.speed < 6.94:
            accel = self.getSmoothLevel() * 0.5
        elif self.speed < 9.72:
            accel = self.getSmoothLevel() * 0.333
        elif self.speed < 12.5:
            accel = self.getSmoothLevel() * 0.222
        elif self.speed < 23.5:
            accel = self.getSmoothLevel() * 0.194
        # 最高速度では加速は0になる
        else:
            accel = 0

        # 走行中に切にすると停車までクラッチが切れる
        if self.getWay() == 0 and self.speed > 0:
            self.clutch = False
        # 停車でクラッチ接続
        if self.clutch == False and self.speed == 0:
                self.clutch = True

        # 切位置時かクラッチ切れ時は空吹かしになって加速はしない
        if self.getWay() == 0 or not self.clutch:
            print('空吹かし')
            accel = 0

        # 0.1秒あたりのブレーキレバー作用(max ±1.9m/s3) ここは実物に則さない
        if self.isKeyEnabled():
            # bc: 減速度(m/s2) ここは実物に則さない
            self.bc += self.brake_level * 1.9 * 0.1
            if self.bc < 0:
                self.bc = 0
        # キーSWが運転位置にない場合は固定
        else:
            print('固定位置')
        
        # 走行抵抗
        if self.bc < 0.06 and self.mascon_level == 0:
            self.bc = 0.055
        elif self.bc > self.BC_MAX:
            self.bc = self.BC_MAX
            
        # 加減速計算
        self.speed = self.speed + (accel - self.bc) * 0.1 * self.freight
        if self.speed < 0:
            self.speed = 0

        # 非常ブレーキ
        if self.eb:
            self.bc = self.BC_MAX
            self.setMascon(0)
            # 停車で復位
            if self.speed == 0:
                self.eb = False
                self.setBrake(0)

    def getSpeed(self):
        return self.speed
    
    # 0 ~ 14のマスコンノッチを入力 EB時は力行不可
    def setMascon(self, mascon_level):
        if not self.eb:
            self.mascon_level = mascon_level
        else:
            self.mascon_level = 0
    
    # -1(緩め) ~ 0(重なり) ~ +1(常用・非常) のブレーキレベルを入力
    def setBrake(self, brake_level):
        self.brake_level = brake_level
        
    # 実際のブレーキ管圧力を便宜上のブレーキシリンダ圧力値から求める
    # ブレーキ管圧力は通常490kPa 140kPa減圧して350kPaになると最大がかかる
    def getBp(self):
        return 490 - (self.bc / self.BC_MAX) * 140
        
    def setButtons(self, buttons):
        self.buttons = buttons
        
    # 0(切),1,2の3つの方向を返す
    def getWay(self):
        return (self.buttons & 0b11000000) >> 6
    
    # 入換・本線スイッチ状態をboolで返す
    def isHonsenEnabled(self):
        return bool(self.buttons & 0b00010000)
    
    # 鍵スイッチ状態をboolで返す
    def isKeyEnabled(self):
        return bool(self.buttons & 0b00001000)
