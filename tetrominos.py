#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import params
import table_screen
import random

class tetrominos:
    #initialise a tetromino at the top of the screen
    def __init__(self):
        self.type 		= random.randrange(params.SHAPE_NB)
        self.angle 		= random.randrange(params.dico_nbrot[self.type])
        self.position_x = params.COL_NB/2
        self.position_y = 0

    #check if the position is possible
    def check_is_possible(self,table):
        test = True
        for (x,y) in params.dico_shape[self.type][self.angle]:
            test = test & table.value[(self.position_x+x)+(self.position_y-y)*params.ROW_NB]!= params.WHITE
        return test

    #turn the triomino
    def rotate(self,dir,table):
        aux = self.angle
        self.angle = (self.angle+dir)%params.dico_nbrot[self.type]
        if self.check_is_possible(table):
            return
        self.angle = aux

    #print and erase the triomino
    def add_tetrominos(self,table):
        for (x,y) in params.dico_shape[self.type][self.angle]:
            table.value[(self.position_x+x)+(self.position_y+y)*params.ROW_NB] = self.color

    #lower the tetrominos and return True if it is possible
    def low(self,table):
        self.position_y += 1
        if self.check_is_possible(table):
            return True
		self.position_y -= 1
        return False
