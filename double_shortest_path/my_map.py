# -*- coding:utf-8 -*-

import os
import sys
import copy

class Vertex(object):
    def __init__(self, name, type_str, pos):
        self.name = name
        self.type_str = type_str
        self.pos = pos
        self.edges = []
        
    def add_edge(self, edge):
        self.edges.append(edge)
        
    def get_edges(self):
        return self.edges

    def get_name_and_type_str(self):
        return self.name, self.type_str
    
    def printing(self):
        print(self.pos)
        print(self.edges)
        
class MyMap(object):
    def __init__(self, map_dat_file):
        # -- read map_dat_file --
        self.str_map = []
        with open(map_dat_file, 'r') as f:
            for l in f:
                self.str_map.append([_ for _ in l.strip()])
                
        # -- make vertext --
        self.vertexes = []
        for i in range(len(self.str_map)):
            self.vertexes.append([Vertex('{}_{}'.format(i, j), self.str_map[i][j], [i, j]) for j in range(len(self.str_map[i]))])
                
        # -- aggregate edge --
        self.edge_dict = {}
        for i in range(len(self.str_map)):
            for j in range(len(self.str_map[i])):
                if self.str_map[i][j] == 'x':
                    continue
                
                if self.str_map[i - 1][j] != 'x':
                    self.edge_dict['{}_{}__{}_{}'.format(i - 1, j, i, j)] = [(i - 1, j), (i, j)]
                    
                if self.str_map[i][j - 1] != 'x':
                    self.edge_dict['{}_{}__{}_{}'.format(i, j - 1, i, j)] = [(i, j - 1), (i, j)]
                    
                if self.str_map[i][j + 1] != 'x':
                    self.edge_dict['{}_{}__{}_{}'.format(i, j, i, j + 1)] = [(i, j), (i, j + 1)]
                    
                if self.str_map[i + 1][j] != 'x':
                    self.edge_dict['{}_{}__{}_{}'.format(i, j, i + 1, j)] = [(i, j), (i + 1, j)]
                    
        # -- add vertexes --
        for edge_name in self.edge_dict:
            tmp = self.edge_dict[edge_name]
            start_i = tmp[0][0]
            start_j = tmp[0][1]
            end_i   = tmp[1][0]
            end_j   = tmp[1][1]
            self.vertexes[start_i][start_j].add_edge(edge_name)
            self.vertexes[end_i][end_j].add_edge(edge_name)
            
    def get_str_map(self):
        return copy.deepcopy(self.str_map)
    
    def get_vertex_names(self):
        vertex_names = []
        for i in range(len(self.vertexes)):
            for j in range(len(self.vertexes[i])):
                name, type_str = self.vertexes[i][j].get_name_and_type_str()
                if type_str != 'x':
                    vertex_names.append(name)
        return vertex_names
    
    def get_edge_names(self):
        return [_ for _ in self.edge_dict]

    def get_edge_names_at_vertex(self, vertex_name):
        tmp = vertex_name.split('_')
        return self.vertexes[int(tmp[0])][int(tmp[1])].get_edges()
    
    def get_vertex_type(self, vertex_name):
        tmp = vertex_name.split('_')        
        _, type_str = self.vertexes[int(tmp[0])][int(tmp[1])].get_name_and_type_str()
        return type_str
    
    def printing(self):
        for i in range(len(self.vertexes)):
            for j in range(len(self.vertexes[i])):
                self.vertexes[i][j].printing()
            

if __name__ == '__main__':
    my_map = MyMap('map.dat')
    my_map.printing()
    vs = my_map.get_vertex_names()
    print(vs)
    for v in vs:
        print(my_map.get_edge_names_at_vertex(v))
        print(my_map.get_vertex_type(v))
    print(my_map.get_edge_names())
