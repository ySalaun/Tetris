#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import params
import table_screen
import random


square_0=[(0,0),(0,1),(1,0),(1,1)]
line_0=[(0,0),(0,1),(0,2),(0,3)]
line_1=[(-1,0),(0,0),(1,0),(2,0)]
p_1=[(0,0),(0,1),(0,2),(1,2)]
p_2=[(-1,0),(-1,1),(0,0),(1,0)]
p_3=[(-1,0),(0,0),(0,1),(0,2)]
p_4=[(-1,1),(0,1),(1,1),(0,1)]
q_1=[(0,0),(0,1),(0,2),(-1,2)]
q_2=[(-1,0),(-1,1),(0,1),(1,1)]
q_3=[(0,0),(1,0),(0,1),(0,2)]
q_4=[(-1,0),(0,0),(1,0),(1,1)]
z_1=[(0,0),(1,2),(1,0),(1,1)]
z_2=[(-1,1),(0,1),(0,0),(1,0)]
s_1=[(0,0),(0,1),(-1,1),(-1,2)]
s_2=[(-1,0),(0,0),(0,1),(1,1)]
t_1=[(0,0),(0,1),(-1,1),(1,1)]
t_2=[(0,0),(0,1),(0,2),(1,1)]
t_3=[(0,0),(-1,0),(1,0),(0,1)]
t_4=[(0,0),(0,1),(0,2),(-1,1)]
square=[square_0]
line=[line_0,line_1]
p=[p_1,p_2,p_3,p_4]
q=[q_1,q_2,q_3,q_4]
z=[z_1,z_2]
s=[s_1,s_2]
dico_shape={0:square,1:line,2:p,3:q,4:z,5:s,6:t}
dico_nbrot={0:1,1:2,2:4,3:4,4:2,5:2,6:4}
dico_color={0:params.YELLOW,1:params.TURQUOISE,2:params.BLUE,3:params.PURPLE,4:params.GREEN,5:params.RED,6:params.BLACK}


class tetrominos:
    #initialise a tetromino at the top of the screen
    def __init__(self):
        self.type=random.randrange(7)
        self.angle=random.randrange(dico_nbrot[self.type])
        self.position_x=COL_NB/2
        self.position_y=random.randrange(ROW_NB-2)+1

    #check if the position is possible
    def check_is_possible(self,table):
        test=True
        for (x,y) in dico_shape[self.type][self.angle]:
            test=test & table.value[(self.position_x+x)+(self.position_y-y)*params.ROW_NB]!= params.WHITE
        return test

    #turn the triomino
    def rotate(self,dir,table):
        aux=self.angle
        self.angle=(self.angle+dir)%dico_nbrot[self.type]
        if self.check_is_possible(table):
            return
        self.angle=aux

    #print and erase the triomino
    def show(self,table,color):
        for (x,y) in dico_shape[self.type][self.angle]:
            table.value[(self.position_x+x)+(self.position_y+y)*params.ROW_NB] = color

    #low the tetrominos and return True if it is possible
    def low(self,table,color):
        self.position_y+=1
        if self.check_is_possible(table):
            self.position_y+=1
            self.show(table,params.WHITE)
            self.position_y-=1
            self.show(table,dico_color[self.type])
            return True
        return False
