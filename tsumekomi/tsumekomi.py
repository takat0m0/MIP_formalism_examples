# -*- coding:utf-8 -*-

from __future__ import print_function

import os
import sys

import numpy as np
from ortools.linear_solver import pywraplp
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from squares import Squares, COLORS

NUM_COLORS = len(COLORS)

class NormalTsumekomi(object):
    
    def __init__(self, height, width):
        self.height = height
        self.width  = width
        
        self.solver = pywraplp.Solver.CreateSolver('SCIP')
        self.solver.EnableOutput()
        
        
    def make_variable(self, squares):
        # x and y
        self.x = []; self.y = []
        for s_id in range(len(squares)):
            square = squares[s_id]
            self.x.append(self.solver.NumVar(0, self.width - square.width,
                                             'x_{}'.format(s_id)))

            self.y.append(self.solver.NumVar(0, self.height - square.height,
                                             'y_{}'.format(s_id)))
        # z
        self.zL = {}; self.zR = {}; self.zU = {}; self.zD = {}
        for s_id in range(len(squares)):
            self.zL[s_id] = {}
            self.zR[s_id] = {}
            self.zU[s_id] = {}
            self.zD[s_id] = {}
            for s_id_ in range(s_id + 1, len(squares)):
                self.zL[s_id][s_id_] = self.solver.IntVar(0, 1, 'zL_{}_{}'.format(s_id, s_id_))

                self.zR[s_id][s_id_] = self.solver.IntVar(0, 1, 'zR_{}_{}'.format(s_id, s_id_)) 

                self.zU[s_id][s_id_] = self.solver.IntVar(0, 1, 'zU_{}_{}'.format(s_id, s_id_))

                self.zD[s_id][s_id_] = self.solver.IntVar(0, 1, 'zD_{}_{}'.format(s_id, s_id_))

    def make_constraint(self, squares):
        self._z_sum_equals_one()
        self._not_overlap(squares)
        
    def _z_sum_equals_one(self):
        for s_id in range(len(self.x)):
            for s_id_ in range(s_id + 1, len(self.x)):
                tmp = [self.zL[s_id][s_id_], self.zR[s_id][s_id_],
                       self.zU[s_id][s_id_], self.zD[s_id][s_id_]]
                self.solver.Add(sum(tmp) == 1)
                
    def _not_overlap(self, ss):
        for i in range(len(self.x)):
            for j in range(i + 1, len(self.x)):
                s  = ss[i]
                s_ = ss[j]
                w, h = s.width, s.height
                w_, h_ = s_.width, s_.height
                W, H = self.height, self.width
                
                self.solver.Add(self.x[i] + w  <= self.x[j] + W * (1 - self.zL[i][j]))
                self.solver.Add(self.x[j] + w_ <= self.x[i] + W * (1 - self.zR[i][j]))
                self.solver.Add(self.y[i] + h  <= self.y[j] + H * (1 - self.zU[i][j]))
                self.solver.Add(self.y[j] + h_ <= self.y[i] + H * (1 - self.zD[i][j]))
                
    def solve(self):
        status = self.solver.Solve()
        return status
    
    def set_xy_to_squares(self, ss):
        xy = []
        for s_id in range(len(self.x)):
            xy.append((self.x[s_id].solution_value(),
                       self.y[s_id].solution_value()))
        ss.set_xys(xy)

class Tsumekomi(NormalTsumekomi):
    def __init__(self, height, width):
        super().__init__(height, width)

    def make_additional_variable_and_constraint(self, ss):
        self.maxW = [self.solver.NumVar(0, self.width,
                                        'maxW_{}'.format(c_id)) for c_id in range(NUM_COLORS)]
        self.minW = [self.solver.NumVar(0, self.width,
                                        'minW_{}'.format(c_id)) for c_id in range(NUM_COLORS)]
        self.maxH = [self.solver.NumVar(0, self.height,
                                     'maxH_{}'.format(c_id)) for c_id in range(NUM_COLORS)]
        self.minH = [self.solver.NumVar(0, self.height,
                                     'minH_{}'.format(c_id)) for c_id in range(NUM_COLORS)]
        
        for c_id in range(NUM_COLORS):
            squres_c_id = ss.get_s_id_list_with_c_id(c_id)
            for s_id in squres_c_id:
                w, h = ss[s_id].width, ss[s_id].height
                self.solver.Add(self.maxW[c_id] >= w + self.x[s_id])
                self.solver.Add(self.minW[c_id] <= self.x[s_id])
                self.solver.Add(self.maxH[c_id] >= h + self.y[s_id])
                self.solver.Add(self.minH[c_id] <= self.y[s_id])
        tmp = [self.maxW[c_id] - self.minW[c_id] + self.maxH[c_id] - self.minH[c_id] for c_id in range(NUM_COLORS)]
        
        self.solver.Minimize(sum(tmp))
        
        
if __name__ == '__main__':
    height = 15
    width  = 15
    num_squares = 35
    
    ss = Squares()
    for _ in range(num_squares):
        ss.add_square()

    p = Tsumekomi(height = height, width = width)    
    p.make_variable(ss)
    p.make_constraint(ss)
    p.make_additional_variable_and_constraint(ss)

    status = p.solve()
    p.set_xy_to_squares(ss)
    
    fig = plt.figure()    
    ax = fig.add_subplot(1,1,1)
    ax.set_xlim([-1, width + 1])
    ax.set_ylim([-1, height + 1])    
    r = patches.Rectangle(xy = (0, 0),
                          width = width, height = height,
                          edgecolor = 'black',
                          facecolor = 'white'
    )    
    ax.add_patch(r)
    ss.add_rectangles_to_ax(ax)
    plt.savefig('result.png')
