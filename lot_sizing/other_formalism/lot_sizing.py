# -*- coding:utf-8 -*-

from __future__ import print_function

import os
import sys

import numpy as np
from ortools.linear_solver import pywraplp

from days import Days
from product import Product
from demands import Demands

class LotSizing(object):
    def __init__(self):
        self.solver = pywraplp.Solver.CreateSolver('SCIP')
        self.solver.EnableOutput()

        self.max_each_stock = 70    

    def make_variables(self, days, product):
        all_day_num = days.all_day_num()
        # x
        self.x = {}
        for from_day in days.get_all_days_list():
            self.x[from_day] = {}
            tmp = from_day + product.dead_day
            to_day = tmp if tmp < all_day_num else all_day_num
            for day in range(from_day, to_day):
                self.x[from_day][day] = self.solver.NumVar(0, product.max_product_num, 'x_{}_{}'.format(from_day, day))

        # y
        self.y = {}
        for from_day in days.get_all_days_list():
            self.y[from_day] = self.solver.IntVar(0, 1,
                                                  'y_{}'.format(from_day))
        # I (auxualy)
        self.I = {}
        for day in days.get_target_days_list():
            self.I[day] = self.solver.NumVar(0, self.max_each_stock, 'I_{}'.format(day))
            
    def make_constraint(self, days, product, demands):
        # -- max production --
        for from_day in days.get_all_days_list():
            tmp = [self.x[from_day][_] for _ in self.x[from_day]]
            self.solver.Add(sum(tmp) <= self.y[from_day] * product.change_cost)

        # -- demand --
        for day in days.get_target_days_list():
            if day - product.dead_day <= -1:
                delta_range = range(0, day + 1)
            else:
                delta_range = range(day - product.dead_day + 1, day + 1)
            tmp = [self.x[delta][day] for delta in delta_range]
            self.solver.Add(sum(tmp) == demands[day])
            
        # -- safety stock --
        for day in days.get_target_days_list():
            self.solver.Add(self.I[day] >= product.safety_stock)
            
        # -- relation between I and x --
        # TODO: more sophiscated aggregation
        
        for day in days.get_target_days_list():
            tmp = []
            for from_day in days.get_all_days_list():
                for to_day in days.get_all_days_list():
                    if from_day < day and day < to_day:
                        try:
                            adding = self.x[from_day][to_day]
                        except:
                            continue
                        tmp.append(adding)
            self.solver.Add(self.I[day] == sum(tmp))
            
    def make_objective(self, days, product):
        tmp = []
        for from_day in days.get_all_days_list():
            tmp.extend([product.prod_cost * self.x[from_day][day] for day in self.x[from_day]])

        for day in days.get_target_days_list():
            tmp.append(product.stock_cost * self.I[day])
            tmp.append(product.change_cost * self.y[day])
        self.solver.Minimize(sum(tmp))
        
    def solve(self):
        status = self.solver.Solve()
        return status                

    def result(self, days, demands):
        for day in days.get_target_days_list():
            print(self.I[day].solution_value())
        for from_day in days.get_all_days_list():
            for to_day in self.x[from_day]:
                print('{} -> {}: {}'.format(from_day, to_day, self.x[from_day][to_day].solution_value()))
        for day in days.get_target_days_list():
            print('{}: {}'.format(day, demands[day]))
if __name__  == '__main__':
    days = Days()
    demands = Demands(days)
    product = Product()

    p = LotSizing()
    p.make_variables(days, product)
    p.make_constraint(days, product, demands)
    p.make_objective(days, product)
    p.solve()
    p.result(days, demands)
