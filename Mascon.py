#coding:utf-8

class Mascon:
    @classmethod
    def formatValue(self, mascon_value):
        # 試験用マスコンの場合
        TEST = True
        if TEST:
            if mascon_value[7:8] == '1':
                return 1
            elif mascon_value[6:7] == '1':
                return 3
            elif mascon_value[5:6] == '1':
                return 7
            elif mascon_value[4:5] == '1':
                return 12
            elif mascon_value[3:4] == '1':
                return 14
            else:
                return 0
        else:
            if (len(mascon_value[3:]) != 5):
                return 0
            mascon_num = int(mascon_value[3:])
            
            if mascon_num < 16:
                return mascon_num - 9
            else:
                return mascon_num - 17
            
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
