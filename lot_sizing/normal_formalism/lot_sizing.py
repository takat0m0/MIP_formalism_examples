# -*- coding:utf-8 -*-

from __future__ import print_function

import os
import sys
import math

import numpy as np
from ortools.linear_solver import pywraplp
import matplotlib.pyplot as plt

from products import Products

class LotSizing(object):
    def __init__(self):
        self.solver = pywraplp.Solver.CreateSolver('SCIP')
        self.solver.EnableOutput()

        self.max_each_stock = 70
        self.max_each_prod  = 40

    def make_variables(self, products, num_days):
        # product_num
        self.x = {}
        for product in products:
            self.x[product] = [self.solver.NumVar(0, self.max_each_prod * len(products), 'x_{}_{}'.format(product, _)) for _ in range(num_days)]

        # dandorigae
        self.y = {}
        for product in products:
            self.y[product] = [self.solver.IntVar(0, 1, 'y_{}_{}'.format(product, _)) for _ in range(num_days)]
            
        # stock
        self.I = {}
        for product in products:
            self.I[product] = [self.solver.NumVar(0, self.max_each_stock * len(products), 'I_{}_{}'.format(product, _)) for _ in range(num_days)]        
        
    def make_constraints(self, products, num_days):
        # continuous
        for product in products:
            self.solver.Add(self.I[product][0] == products[product].initial + self.x[product][0] - products[product].demand[0])
            
        for d in range(num_days - 1):
            for product in products:
                self.solver.Add(self.I[product][d + 1] == self.I[product][d] + self.x[product][d + 1] - products[product].demand[d + 1])

        # safety stock
        for d in range(num_days):
            for product in products:
                self.solver.Add(self.I[product][d] >= products[product].safe_stock)
        # return
        for product in products:
            self.solver.Add(self.I[product][num_days - 1] >= products[product].initial)
            
        for d in range(num_days):
            tmp = [self.x[product][d] for product in products]
            self.solver.Add(sum(tmp) <= self.max_each_prod * len(products))
            
        for d in range(num_days):
            tmp = [self.y[product][d] for product in products]
            self.solver.Add(sum(tmp) >= 10)
            
        # stock upper
        for d in range(num_days):
            tmp = [self.I[product][d] for product in products]
            self.solver.Add(sum(tmp) <= len(products) * self.max_each_stock)
        
        # product
        for d in range(num_days):
            for product in products:
                self.solver.Add(self.x[product][d] <= len(products) * self.max_each_prod * self.y[product][d])

    def make_objective(self, products, num_days):
        tmp = []
        for d in range(num_days):
            tmp.extend([products[p].change_fee * self.y[p][d] +
                        products[p].product_fee * self.x[p][d] +
                        products[p].preserve_fee * self.I[p][d] for p in products])
        self.solver.Minimize(sum(tmp))
        
    def solve(self):
        status = self.solver.Solve()
        return status        

    def result(self, products, num_days):
        ps.cost_with_jst()        
        def rounding(target):
            f = math.floor(target)
            c = math.ceil(target)
            if target - f > c - target:
                return c
            else:
                return f
            
        for product in products:
            fig = plt.figure()
            ax1 = fig.add_subplot(211)
            ax1.set_ylim([0, 500])
            
            ax2 = fig.add_subplot(212)            
            ax2.set_ylim([0, 500])
            
            x = [_ for _ in range(num_days)]

            prod = [rounding(self.x[product][d].solution_value()) for d in range(num_days)]
            pre = [rounding(self.I[product][d].solution_value()) for d in range(num_days)]            
            ax1.bar(x, prod, color = 'blue')
            ax2.bar(x, pre,  color = 'green')            
            plt.savefig('result/result_{}.png'.format(product))
            
                
if __name__ == '__main__':
    num_prods = 50
    num_days  = 30
    ps = Products(num_prods, num_days)

    
    ls = LotSizing()
    ls.make_variables(ps, num_days)
    ls.make_constraints(ps, num_days)
    ls.make_objective(ps, num_days)        
    ls.solve()

    ls.result(ps, num_days)
