from __future__ import print_function
import sys
from ortools.constraint_solver import pywrapcp
from termcolor import colored
from data import *

nbcouleurs=0
couleurs=[]

for i in range(n):
	for j in range(n):
		if M[i][j] not in couleurs:
			couleurs += [M[i][j]]
			nbcouleurs +=1

# Do not add colors !!!
colors = ['grey']
while len(colors)<nbcouleurs:
	colors += ['red','green','yellow','blue','magenta','cyan','white']

def prettyPrint(X, M):
	for i in range(n):
		#print top
		for j in range(n):
			print ("  ",end=''),
			print (colored(X[i][j][top].Value(),colors[X[i][j][top].Value()], "on_"+colors[X[i][j][top].Value()]),end=''),
			print ("  ",end=''), 
		print("")
		#print left center and right
		for j in range(n):
			print (colored(X[i][j][left].Value(),colors[X[i][j][left].Value()], "on_"+colors[X[i][j][left].Value()]),end=''),
			for e in [top, bottom, right, left]:
				if X[i][j][e].Value() != 0:
					if M[i][j]!=0:
						print (""+ colored(X[i][j][e].Value(),colors[X[i][j][e].Value()], "on_"+colors[X[i][j][e].Value()])+ colored(X[i][j][e].Value(),colors[X[i][j][e].Value()], "on_"+colors[X[i][j][e].Value()])+ colored(X[i][j][e].Value(),colors[X[i][j][e].Value()], "on_"+colors[X[i][j][e].Value()])+"",end=''),
						break
					else:
						print (""+ colored(X[i][j][e].Value(),colors[X[i][j][e].Value()], "on_"+colors[X[i][j][e].Value()])+ colored(X[i][j][e].Value(),colors[X[i][j][e].Value()], "on_"+colors[X[i][j][e].Value()])+ colored(X[i][j][e].Value(),colors[X[i][j][e].Value()], "on_"+colors[X[i][j][e].Value()])+"",end=''),
						break
			print (colored(X[i][j][right].Value(),colors[X[i][j][right].Value()], "on_"+colors[X[i][j][right].Value()]),end=''), 
		print("")
		#print bottom
		for j in range(n):
			print ("  ",end=''),
			print (colored(X[i][j][bottom].Value(),colors[X[i][j][bottom].Value()], "on_"+colors[X[i][j][bottom].Value()]),end=''),
			print ("  ",end=''), 
		print("")



def prettyPrintM(M):
	for i in range(n):
		for j in range(n):
			print (M[i][j],end=''),
		print("")
def prettyPrettyM(M):
	for i in range(n):
		for j in range(n):
			print( colored(M[i][j], colors[M[i][j]], "on_"+colors[M[i][j]]),end=''),
		print("")

def flatten(matr):
    rows = len(matr)
    cols = len(matr[0])
    elements = len(matr[0][0])
    return [matr[i][j][e] for e in range (elements) for j in range(cols) for i in range(rows)]


def accesM(M,i,j,edge):
	return M[4*n*i+4*j+e]

# Creates the solver.
solver = pywrapcp.Solver("freeFlow")

# Create variables 
X  = [[[solver.IntVar(0, nbcouleurs +1, "X[%i][%i][%i]"  % (i,j,e)) for e in range(4)] for j in range(n)] for i in range(n)]

#Add constraints

# On fait la premiere ligne
for j in range (n):
	solver.Add(X[0][j][top] == 0)

# On fait la derniere ligne
for j in range (n):
	solver.Add(X[n-1][j][bottom] == 0)

# On fait la premiere colonne
for i in range (n):
	solver.Add(X[i][0][left] == 0)

# On fait la derniere colonne
for i in range (n):
	solver.Add(X[i][n-1][right] == 0)

#Only one edge with a color for cases in initial points
for i in range(n):
	for j in range(n):
		if M[i][j]!=0:
				Mij=M[i][j]
				allowed = [(Mij,0,0,0),(0,Mij,0,0),(0,0,Mij,0),(0,0,0,Mij)]
				solver.Add(solver.AllowedAssignments(tuple(X[i][j]), allowed ))

for i in range(n-1):
	for j in range(n-1):
		# if M[i][j]==0:
			solver.Add(X[i][j][bottom] == X[i+1][j][top])
			solver.Add(X[i][j+1][left] == X[i][j][right])

for j in range(n-1):
	solver.Add(X[n-1][j+1][left] == X[n-1][j][right])

for i in range(n-1):
		solver.Add(X[i][n-1][bottom] == X[i+1][n-1][top])

allowed=[]
for i in range (1,nbcouleurs +1):
	allowed.extend([(i,i,0,0),
				(i,0,i,0),
				(i,0,0,i),
				(0,i,i,0),
				(0,i,0,i),
				(0,0,i,i)])

for i in range(n):
	for j in range(n):
		if M[i][j]==0:
			solver.Add(solver.AllowedAssignments(tuple(X[i][j]),allowed))

db = solver.Phase(flatten(X),
            solver.INT_VAR_SIMPLE,
            solver.ASSIGN_MAX_VALUE)

solver.NewSearch(db)
prettyPrettyM(M)
if solver.NextSolution():
	prettyPrint(X,M)
else:
	print ("No solution found :(")