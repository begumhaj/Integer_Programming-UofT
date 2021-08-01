import sys
import math
import random
from gurobipy import *

# Data
h = [1.25, 1.25, 0.9, 0.8, 1.9, 1.2, 0.8, 1.5, 1.0, 1.0, 1.2, 0.75]	
f = [450.0, 500.00, 700.00, 550.00,  550.00,  630.00,  680.00,  580.00,  620.00, 470.00,  490.00, 610.00]
SI = [83.0, 31.00, 11.00, 93.00,  82.00,  72.00,  23.00,  91.00,  83.00, 34.00,  61.00,  82.00]
SF = [20.0, 20.00, 20.00, 20.00,  20.00,  20.00,  20.00,  20.00,  20.00, 20.00,  20.00,  20.00]
D = [
[0,   95,  110, 96,  86,  124, 83,  108, 114, 121],  
[98,  96,  96,  98,  103, 104, 122, 101, 89,  108],  
[106, 0,   89,  123, 96,  105, 83,  82,  112, 109], 
[98,  121, 0,   105, 98,  96,  101, 81,  117, 76],   
[0,   124, 113, 123, 123, 79,  111, 98,  97,  80], 
[103, 102, 0,   95,  107, 105, 107, 105, 75,  93],    
[110, 93,  0,   112, 84,  124, 98,  101, 83,  87], 
[85,  92,  101, 110, 93,  96,  120, 109, 121, 87], 
[122, 116, 109, 0,   105, 108, 88,  98,  77,  90], 
[120, 124, 94,  105, 92,  86,  101, 106, 75,  109],
[117, 96,  78,  0,   108, 87,  114, 107, 110, 94], 
[125, 112, 75,  0,   116, 103, 122, 88,  85,  84] 
]
L = [1600, 1800]
alpha = [
    [1.2, 0.8, 1.5, 1.0, 1.0, 1.2, 0.75, 1.25, 1.25, 0.9, 0.8, 1.9], 
    [0.8, 2.5, 0.7, 2.2, 1.4, 0.8, 0.9,  0.8,  1.0,  1.3, 1.5, 2.2] ]

I = 12
T = 10
K = 2

#compute M[i][t]
M = []
for i in range(I):
    row =[]
    for t in range(T):
        value = sum([D[i][k] for k in range(t,T)]) + SF[i]
        row.append(value)
    M.append(row)

# Solution method option: 0 for IP, 1 for cut-and-branch, 2 for branch-and-cut
option = 0

# IMPLEMENT: Cut generator function for a specific "i" and "l"
def get_cut(xvals, yvals, sval, l):
    # Input: x, y values for a specific location (i) and for all "t"" in {0,...,T} ; sval = s[i,l]; l = max index of the cut  (see lecture notes, Chapter 8)
    # Output: set of index that from the cut, S_star (see lecture notes, Chapter 8)
    cut = []

    ## =============================================
    ## Put your code here!




    ## =============================================

    return cut

# IMPLEMENT: Call back function that is call in every node of the search     
def lSCallback(model, where):
    if where == GRB.callback.MIPNODE:
        xvals = [] #  model.cbGetNodeRel(model._x) to get all the x[i,t] variables
        yvals = [] 
        svals = [] 
        ## =============================================
        ## Put your code here!


        # HINT: Use model.cbCut( ) to add your User cuts
        # HINT: print the cut in each iteration (only when debugging) to make sure that you are adding different cuts

        ## =============================================
    

# Create model
m = Model()

#Variables: production
x = {}
for i in range(I):
    for t in range(T):
        x[i,t] = m.addVar(vtype=GRB.CONTINUOUS, lb=0.0, obj=0.0,  name="x_"+str(i)+","+str(t))

# Variables: set-up 
y = {}
for i in range(I):
    for t in range(T):
        y[i,t] = m.addVar(vtype=GRB.BINARY, obj=f[i], name="y_"+str(i)+","+str(t))

# Variables: inventory
s={}
for i in range(I):
    for t in range(T):
        s[i,t] = m.addVar(vtype=GRB.CONTINUOUS, lb=0.0, obj=h[i], name="s_"+str(i)+","+str(t))


m.modelSense = GRB.MINIMIZE
m.update()

# Constraints: Demand
m.addConstrs( (SI[i] + x[i,0] == D[i][0] + s[i,0]  for i in range(I)) )  #initial inventory

for t in range(1,T):
    m.addConstrs( (s[i,t-1] + x[i,t] == D[i][t] + s[i,t]  for i in range(I)) )

# Constraints: final inventory
m.addConstrs( s[i,T-1] == SF[i] for i in range(I))

# Constraints: set-up
for t in range(T):
    m.addConstrs( (x[i,t] <= M[i][t]*y[i,t]  for i in range(I)) )

#Constraints: capacity
for k in range(K):
    m.addConstrs( (quicksum(alpha[k][i] * x[i,t] for i in range(I)) <= L[k] for t in range(T)) ) 

#Print model
#m.write("model.lp")

#Parameters
m.params.threads = 1
m.params.timelimit = 300    # 5 minutes = 300 seconds
m.setParam('Cuts',0)        # turn off all Gurobi cuts

if option != 0:
    m.setParam('Presolve',0)    # turn off presolve features
    m.setParam('PreCrush',1)    # This is the parameter for adding cuts


if option == 0:
    ## Solve the model without cuts
    m.optimize()


if option == 1:
    ## cut-and-branch 

    # Change the variable type to continuous, so we are now solving LP relaxation
    for i in range(I):
    	for t in range(T):
    		y[i,t].Vtype='C'
    
    # Do a loop of cuts outside of the tree (cut-and-branch)
    # You should end the loop when there are no more possible cuts
    ## =============================================
    ## Put your code here!





    ## =============================================

    ## Now we solve the MIP model with the cuts
    # Change type back to binary
    for i in range(I):
    	for t in range(T):
    		y[i,t].Vtype='B'

    # Compute optimal solution
    m.optimize()

if option == 2:
    ## Branch-and-cut
    # Optimize with the callback procedure
    m._x = x
    m._y = y
    m._s = s
    m.update()
    m.optimize(lSCallback)
