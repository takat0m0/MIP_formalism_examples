# -*- coding:utf-8 -*-

import os
import sys

import numpy as np

from days import Days

MAX_DEMAND = 30

class Demands(object):
    def __init__(self, days):
        self.__data = [0 for _ in days.get_all_days_list()]
        for day in days.get_target_days_list():
            self.__data[day] = np.random.randint(0, MAX_DEMAND)
            
    def __getitem__(self, day):
        return self.__data[day]

if __name__ == '__main__':
    days = Days()
    d = Demands(days)
    print(d[20])
