# parameters
from PyQt4.QtGui import QColor

# number of cases in a row
ROW_NB		= 25

# number of cases in a column
COL_NB		= 13 

# speed reference for tetrominoes fall
SPEED		= 50

# cases colors
RED 		= QColor(255, 0, 0) 
TURQUOISE	= QColor(0,	255, 255)
BLUE		= QColor(0, 0, 255)
GREEN		= QColor(0, 255, 0)
PURPLE		= QColor(255, 0, 255)
YELLOW		= QColor(255, 255, 0)
WHITE		= QColor(255, 255, 255)
BLACK		= QColor(0, 0, 0)

# tetrominoes
SHAPE_NB	= 7

# SQUARE
square_0	= [(0,0),(0,1),(1,0),(1,1)]

square		= [square_0]

# LINE
line_0		= [(0,0),(0,1),(0,2),(0,3)]
line_1		= [(-1,0),(0,0),(1,0),(2,0)]

line		= [line_0,line_1]

# P-SHAPE
p_1			= [(0,0),(0,1),(0,2),(1,2)]
p_2			= [(-1,0),(-1,1),(0,0),(1,0)]
p_3			= [(-1,0),(0,0),(0,1),(0,2)]
p_4			= [(-1,1),(0,1),(1,1),(0,1)]

p			= [p_1,p_2,p_3,p_4]

# Q-SHAPE
q_1			= [(0,0),(0,1),(0,2),(-1,2)]
q_2			= [(-1,0),(-1,1),(0,1),(1,1)]
q_3			= [(0,0),(1,0),(0,1),(0,2)]
q_4			= [(-1,0),(0,0),(1,0),(1,1)]

q			= [q_1,q_2,q_3,q_4]

# Z-SHAPE
z_1			= [(0,0),(1,2),(1,0),(1,1)]
z_2			= [(-1,1),(0,1),(0,0),(1,0)]

z			= [z_1,z_2]

# S-SHAPE
s_1			= [(0,0),(0,1),(-1,1),(-1,2)]
s_2			= [(-1,0),(0,0),(0,1),(1,1)]

s			= [s_1,s_2]

# T-SHAPE
t_1			= [(0,0),(0,1),(-1,1),(1,1)]
t_2			= [(0,0),(0,1),(0,2),(1,1)]
t_3			= [(0,0),(-1,0),(1,0),(0,1)]
t_4			= [(0,0),(0,1),(0,2),(-1,1)]

t 			= [t_1, t_2, t_3, t_4]

# DICTIONNARIES
dico_shape	= {0:square, 1:line, 2:p, 3:q, 4:z, 5:s, 6:t}
dico_nbrot	= {0:1, 1:2, 2:4, 3:4, 4:2, 5:2, 6:4}
dico_color	= {0:YELLOW, 1:TURQUOISE, 2:BLUE, 3:PURPLE, 4:GREEN, 5:RED, 6:BLACK}
