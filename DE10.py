#coding:utf-8

class DE10:
    def __init__(self):
        # 車速(m/s)
        self.speed = 0
        self.mascon_level = 0
        # 最大ブレーキシリンダ圧力
        self.BC_MAX = 3.0
        # ブレーキシリンダ圧力(減速度)
        self.bc = self.BC_MAX
        # ブレーキレバー位置(ブレーキシリンダ圧力に作用)
        self.brake_level = 0
        #非常ブレーキ状態
        self.eb = False
        #貨車牽引時の加速度減少(単機: 1)
        self.freight = 0.6
        #統合モジュールのボタン状態(intでビット列)
        # 初期値は前進、本線、鍵ON
        self.buttons = 0b01000000 + 0b00010000 + 0b00001000

    # 0.1秒進める
    def advanceTime(self, honsen):
        # 加速度を求める(m/s2)
        if self.speed < 12:
            accel = self.mascon_level / 14.0 * 0.803
        elif 12 <= self.speed < 25:
            accel = self.mascon_level / 14.0 * 0.5
        elif 25 <= self.speed < 35:
            accel = self.mascon_level / 14.0 * 0.333
        elif 35 <= self.speed < 45:
            accel = self.mascon_level / 14.0 * 0.222
        elif 45 <= self.speed:
            accel = self.mascon_level / 14.0 * 0.194
        
        # 0.1秒あたりのブレーキレバー作用(max ±1.9m/s3) ここは実物に則さない
        if honsen:
            self.bc += self.brake_level * 1.9 * 0.1
        else:
            self.bc += self.brake_level * 2.3 * 0.1
        
        # 減速度(m/s2 max ±5.0m/s2) ここは実物に則さない
        if self.bc < 0:
            self.bc = 0
        elif self.bc > self.BC_MAX:
            self.bc = self.BC_MAX
            
        # 加減速計算
        self.speed = self.speed + (accel - self.bc) * 0.1 * self.freight
        if self.speed < 0:
            self.speed = 0
            
        # OSR 98km/hを超えると非常ブレーキ
        if self.speed > 27.2:
            self.eb = True

        # 非常ブレーキ
        if self.eb:
            self.bc = self.BC_MAX
            self.setMascon(0)
            # 十分に低速になったら自動で復位
            if self.speed < 1:
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
