# -*- coding:utf-8 -*-

import os
import sys

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

MAX_LENGTH = 3
#COLORS = ['magenta', 'red', 'blue', 'yellow', 'cyan', 'green']
#COLORS = ['red', 'blue', 'cyan', 'green']
COLORS = ['red', 'blue', 'green']

class Square(object):
    def __init__(self):
        self.width  = np.random.randint(1, MAX_LENGTH + 1)
        self.height = np.random.randint(1, MAX_LENGTH + 1)
        self.color_id = np.random.choice([_ for _ in range(len(COLORS))]) 
        
        self.x = None
        self.y = None

    def set_xy(self, x, y):
        self.x = x; self.y = y

    def add_rectangle_to_ax(self, ax):
        r = patches.Rectangle(xy = (self.x, self.y),
                              width = self.width, height = self.height,
                              edgecolor = 'black',
                              facecolor = COLORS[self.color_id]
                              )
        ax.add_patch(r)

class Squares(object):
    def __init__(self):
        self.__data = []
        
    def add_square(self):
        self.__data.append(Square())

    def set_xys(self, xys):
        # xys = [(x, y), ....]
        assert(len(xys) == len(self.__data))
        for xy, square in zip(xys, self.__data):
            square.set_xy(xy[0], xy[1])
            
    def add_rectangles_to_ax(self, ax):
        for square in self.__data:
            square.add_rectangle_to_ax(ax)
            
    def get_s_id_list_with_c_id(self, c_id):
        ret = []
        for s_id, square in enumerate(self.__data):
            if square.color_id == c_id:
                ret.append(s_id)
        return ret
    
    def __iter__(self):
        return self.__data.__iter__()

    def __getitem__(self, idx):
        return self.__data[idx]
    
    def __len__(self):
        return len(self.__data)
    
if __name__ == '__main__':
    
    ss = Squares()
    for _ in range(2):
        ss.add_square()
    ss.set_xys([(10, 10), (20, 20)])
    
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.set_xlim([-1, 51])
    ax.set_ylim([-1, 51])    
    r = patches.Rectangle(xy = (0, 0),
                          width = 50, height = 50,
                          edgecolor = 'black',
                          facecolor = 'white'
    )    
    ax.add_patch(r)
    ss.add_rectangles_to_ax(ax)
    plt.savefig('test.png')

    
