# -*- coding:utf-8 -*-

import os
import sys

import numpy as np

class Days(object):
    def __init__(self):
        self.pre_days    = 3
        self.post_days   = 1
        self.target_days = 30
        
    def all_day_num(self):
        all_days = self.pre_days + self.post_days + self.target_days
        return all_days
        
    def get_all_days_list(self):
        all_days = self.all_day_num()
        return [_ for _ in range(all_days)]
    
    def get_pre_days_list(self):
        return [_ for _ in range(self.pre_days)]

    def get_target_days_list(self):
        return [_ for _ in range(self.pre_days, self.pre_days + self.target_days)]

    def get_post_days_list(self):
        from_ = self.pre_days + self.target_days
        to_ = self.pre_days + self.target_days + self.post_days
        return [_ for _ in range(from_, to_)]


if __name__ == '__main__':
    days = Days()
    print(days.get_all_days_list())
    print(days.get_pre_days_list())
    print(days.get_target_days_list())
    print(days.get_post_days_list())            
