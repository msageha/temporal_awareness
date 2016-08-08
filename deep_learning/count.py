# -*- coding: utf-8 -*-
# epoch をカウントしていくもの

class Counter:
        def __init__(self):
                self.count = 0
                self.best = 0
                self.epoch_best_num = 0
                
        def best_count(self, now_accuracy, epoch):
                # 最高値を更新したら、カウンタをゼロにもどし、エポックを記憶
                if now_accuracy > self.best:
                        self.epoch_best_num = epoch
                        self.best = now_accuracy
                        self.count = 0
                # 更新しなかったら、カウンタをインクリメント        
                else:
                        self.count += 1
        
                # 更新しなかった回数を返す
                return self.count
