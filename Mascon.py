#coding:utf-8

class Mascon:
    @classmethod
    def isTest(self):
        return False
        
    @classmethod
    # 第一返値: マスコンノッチ
    # 第二返値: 方向転換スイッチ状態
    def formatValue(self, mascon_value):
        # 試験用マスコンの場合
        if self.isTest():
            if mascon_value[7] == '1':
                return 1, 0 
            elif mascon_value[6] == '1':
                return 3, 0
            elif mascon_value[5] == '1':
                return 7, 0
            elif mascon_value[4] == '1':
                return 12, 0
            elif mascon_value[3] == '1':
                return 14, 0
            # 方向転換スイッチ押下
            elif mascon_value[2] == '1':
                return 99, 0
            else:
                return 0, 0
        else:            
            # 実際の結線と整合する
            mascon_bits = list('00000')
            if mascon_value[5] == '1':
                mascon_bits[4] = '1'
            if mascon_value[3] == '1':
                mascon_bits[3] = '1'
            if mascon_value[0] == '1':
                mascon_bits[2] = '1'
            if mascon_value[1] == '1':
                mascon_bits[1] = '1'
            if mascon_value[7] == '1':
                mascon_bits[0] = '1'
            
            mascon_bits = ''.join(mascon_bits)            
            mascon_num = int(mascon_bits, 2)
            
            if mascon_value[2] == '1':
                way = 1
            elif mascon_value[4] == '1':
                way = 2
            else:
                way = 0
            
            if mascon_num == 0:
                return 0, way
            if mascon_num < 16:
                return mascon_num - 9, way
            else:
                return mascon_num - 17, way
            
            '''
                ノッチビット対照表
                1ノッチから順に
                1ノッチ  01010 10
                2ノッチ  01011
                3ノッチ  01100
                4ノッチ  01101
                5ノッチ  01110
                6ノッチ  01111 15
                7ノッチ  11000 24
                8ノッチ  11001
                9ノッチ  11010
                10ノッチ 11011
                11ノッチ 11100
                12ノッチ 11101
                13ノッチ 11110
                14ノッチ 11111 31
            '''

