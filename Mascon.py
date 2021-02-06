#coding:utf-8

class Mascon:
    @classmethod
    def formatValue(self, mascon_value):
        TEST = True
        if TEST:
            if mascon_value[7:8] == '1':
                return 1
            elif mascon_value[6:7] == '1':
                return 3
            elif mascon_value[4:5] == '1':
                return 7
            elif mascon_value[3:4] == '1':
                return 12
            elif mascon_value[2:3] == '1':
                return 14
        else:
            # 未実装
            pass
