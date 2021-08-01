#!/usr/bin/env python
# coding: utf-8

# In[46]:


from gurobipy import*


# In[47]:


Numberofnodes=11
matrix =  [[0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1],
                     [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1], 
                     [1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0],
                     [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1], 
                     [1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1],
                     [1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1],
                     [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1], 
                     [1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1], 
                     [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1], 
                     [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0]]


# In[48]:


Edges=tuplelist()
for i in range(len(matrix)):
    for j in range(len(matrix[0])):
        if (matrix[i][j] == 1):
            Edges.append((i,j))
print("Edges=",Edges)
                  


# In[49]:


import networkx as nx
import numpy as np
G = nx.from_numpy_matrix(np.array(matrix)) 
nx.draw(G, with_labels=True)


# In[50]:


A= {}
for idx, row in enumerate(matrix):
        res = []
        for r in range(len(row)):
            if row[r] != 0:
                res.append(r)
                
                A[idx] = res
print ("A=",A)


# In[51]:


Degree=[] 
for i in A:
    v=len(A[i])
    Degree.append(v)
print('Degree=',Degree)


# In[52]:


K=max(Degree)+1
print("K=",K)


# In[53]:


Label=[]
for i in range(1,K):
    Label.append(i)
print("Label=",Label)


# In[54]:


#Modelling the Edge Numbering Problem#
mip= Model('Edge_Numbering')


# In[55]:


#Decision variable for edge takes value K#

x= mip.addVars(Edges,Label, vtype=GRB.BINARY,name='x')


# In[56]:


#Defining  decision variable for minimum number for edges#
m=mip.addVars(Numberofnodes,obj=1,vtype=GRB.INTEGER,name="m")
print(m)


# In[57]:


#defining decision variable for maximumedge number for edges#
M=mip.addVars(Numberofnodes,obj=1,vtype=GRB.INTEGER,name="M")
print(M)


# In[58]:


#constraint for Edge labeling#
for i,j in Edges:
  mip.addConstr(sum(x[i,j,l] for l in Label) == 1,"edgelabel[%d,%d]" % (i, j)) 
  print(i,j,l)


# In[59]:


#constraint for Different labelling#
for i in range(Numberofnodes):
    for l in Label:
        mip.addConstr(sum(x[i,j,l] for j in list(A[i])) <= 1,"differentlabel[%d,%d]"  %(i,l))
        print(i,j,l)
         


# In[62]:


# constraint for minimum edge number#
for  i,j in  Edges:
    mip.addConstr( m[i] <= quicksum(x[i,j,l]*l for l in Label), "minimumedgenum[%d,%d]" %(i,j))
    


# In[63]:


# constraint for maximum edge number#
for  i,j in  Edges:
    mip.addConstr( M[i] >= quicksum(x[i,j,l]*l for l in Label), "maximumedgenum[%d,%d]" %(i,j))
    print(i,j,l)


# In[64]:


#check only upper traingular matrix#
for i,j in Edges:
    if i <= j:
        for l in Label:
            mip.addConstr(x[i,j,l] == x[j,i,l])


# In[65]:


#Constraint in Valid inequality#
for i in range(Numberofnodes):
    mip.addConstr(M[i]-m[i]>=len(A[i])-1, "validinequality[%d]" %i)
    print(m,M)


# In[66]:


#Objective function#
mip.setObjective(quicksum(M[i]-m[i]-len(A[i])-1 for i in range(Numberofnodes)), GRB.MINIMIZE)


# In[ ]:


mip.optimize()


# In[ ]:




