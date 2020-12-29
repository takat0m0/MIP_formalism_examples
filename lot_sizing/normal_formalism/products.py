# -*- coding:utf-8 -*-

import os
import sys

import numpy as np
import matplotlib.pyplot as plt

class Product(object):
    def __init__(self, name, num_day):
        self.name = name
        self.initial = np.random.randint(40, 100)
        self.demand = np.random.randint(0, 70, num_day)
        self.safe_stock = 20

        self.preserve_fee = np.random.randint(5)
        self.product_fee  = np.random.randint(10)
        self.change_fee   = np.random.randint(100)
        
    def dump_demand(self, dir_name):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_ylim([0, 80])        
        x = [_ for _ in range(len(self.demand))]
        ax.bar(x, self.demand, color = 'red')
        plt.savefig('{}/demand_{}.png'.format(dir_name, self.name))

    def cost_with_jst(self):
        days = len(self.demand)
        preserve = days * self.initial
        change = days * self.change_fee
        product = sum(self.product_fee * self.demand)
        return preserve + change + product
        
    def printing(self):
        print('-- {} --'.format(self.name))
        print(self.demand)
        print(self.initial)
        print(self.safe_stock)                
        print(self.preserve_fee)
        print(self.product_fee)
        print(self.change_fee)
        
class Products(object):
    def __init__(self, num_products, num_days):
        self.__data = {}
        for i in range(num_products):
            self.__data['prod_{}'.format(i)] = Product('prod_{}'.format(i), num_days)
        self.dump_demand()

    def __iter__(self):
        return self.__data.__iter__()

    def __getitem__(self, prod_name):
        return self.__data[prod_name]
    
    def __len__(self):
        return self.__data.__len__()
    
    def dump_demand(self):
        dir_name = 'demands'
        for product in self.__data:
            self.__data[product].dump_demand(dir_name)

    def cost_with_jst(self):
        tmp = 0
        for product in self.__data:
            tmp += self.__data[product].cost_with_jst()
        print(tmp)
        
    def printing(self):
        for prod_name in self.__data:
            self.__data[prod_name].printing()
        
if __name__ == '__main__':
    ps = Products(100, 30)
    ps.printing()
