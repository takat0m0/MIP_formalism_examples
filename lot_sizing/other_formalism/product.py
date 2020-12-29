# -*- coding:utf-8 -*-

import os
import sys

import numpy as np

class Product(object):
    def __init__(self):
        self.dead_day = 6
        self.max_product_num = 100
        self.prod_cost = 10
        self.stock_cost = 5
        self.change_cost = 100
        self.safety_stock = 10
