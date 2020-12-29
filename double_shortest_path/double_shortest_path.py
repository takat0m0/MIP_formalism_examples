# -*- coding:utf-8 -*-

from __future__ import print_function

import os
import sys

import numpy as np
from ortools.linear_solver import pywraplp

from my_map import MyMap

class ShortestPath(object):

    def __init__(self, my_map):
        self.solver = pywraplp.Solver.CreateSolver('SCIP')
        self.solver.EnableOutput()        

        self._set_start_vertex(my_map)
        self._make_vertex_variables(my_map)
        self._make_edge_variables(my_map)
        
        for path in self.start_v:
            self._make_constraints(my_map, path, self.start_v[path])
        self._make_goal_constraint(my_map)
        self._make_objective(my_map)

    def _set_start_vertex(self, my_map):
        self.start_v = {}
        path_idx = 0
        for vertex in my_map.get_vertex_names():
            str_type = my_map.get_vertex_type(vertex)
            if str_type == 's':
                self.start_v['p{}'.format(path_idx)] = vertex
                path_idx += 1
                
    def _make_vertex_variables(self, my_map):
        self.vertex_vars = {}
        for path in self.start_v:
            tmp = {name: self.solver.IntVar(0, 1,
                                            '{}_{}'.format(path, name)) for name in my_map.get_vertex_names()}
            self.vertex_vars[path] = tmp
            
        # -- vertex can only one path --
        for vertex in my_map.get_vertex_names():
            tmp = [self.vertex_vars[path][vertex] for path in self.start_v]
            self.solver.Add(sum(tmp) <= 1)
        
    def _make_edge_variables(self, my_map):
        self.edge_vars = {}
        for path in self.start_v:
            tmp = {name: self.solver.IntVar(0, 1,
                                            '{}_{}'.format(path, name)) for name in my_map.get_edge_names()}
            self.edge_vars[path] = tmp
        
    def _make_constraints(self, my_map, path, start_vertex):
            
        # -- start vertex --
        tmp = [self.edge_vars[path][e] for e in my_map.get_edge_names_at_vertex(self.start_v[path])]
        self.solver.Add(sum(tmp) == 1)
        self.solver.Add(self.vertex_vars[path][self.start_v[path]] == 1)
            
        for vertex in my_map.get_vertex_names():
            if vertex == start_vertex:
                continue
            v_type = my_map.get_vertex_type(vertex)
            if v_type == 'x':
                continue
            elif v_type == 'g':
                continue
            else:
                tmp = [self.edge_vars[path][e] for e in my_map.get_edge_names_at_vertex(vertex)]
                self.solver.Add(sum(tmp) == 2 * self.vertex_vars[path][vertex])

    def _make_goal_constraint(self, my_map):
        for vertex in my_map.get_vertex_names():
            v_type = my_map.get_vertex_type(vertex)
            if v_type == 'g':
                tmp = []
                for path in self.start_v:
                    for e in my_map.get_edge_names_at_vertex(vertex):
                        tmp.append((path, e))
                tmp2 = [self.edge_vars[path][e] for path, e in tmp]
                self.solver.Add(sum(tmp2) == 1)
        
    def _make_objective(self, my_map):
        tmp = []
        for path in self.start_v:
            for e in my_map.get_edge_names():
                tmp.append((path, e))
        tmp2 = [self.edge_vars[path][e] for path, e in tmp]        
        self.solver.Minimize(sum(tmp2))
        
    def solve(self):
        status = self.solver.Solve()
                
    def show_result(self, str_map):
        for path in self.start_v:
            for vertex in self.vertex_vars[path]:
                val = self.vertex_vars[path][vertex].solution_value()
                if val == 1.0:
                    tmp = vertex.split('_')
                    if str_map[int(tmp[0])][int(tmp[1])] == 'o':
                        str_map[int(tmp[0])][int(tmp[1])] = path[1:]
        for i in range(len(str_map)):
            print(str_map[i])
            
if __name__ == '__main__':
    my_map = MyMap('map.dat')

    sp = ShortestPath(my_map)
    sp.solve()
    sp.show_result(my_map.get_str_map())
