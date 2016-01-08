import sys
from ortools.constraint_solver import pywrapcp
from termcolor import colored

n = 9
top = 0
bottom = 1
left = 2
right = 3	


M=[[0 for col in range (n)] for ligne in range(n)]

M[2][0]=1
M[7][3]=1

M[8][0]=2
M[1][1]=2

M[4][1]=3
M[0][8]=3

M[2][3]=4
M[0][6]=4

M[3][3]=5
M[0][7]=5

M[5][4]=6
M[7][6]=6

M[8][5]=7
M[7][8]=7

M[4][7]=8
M[7][7]=8

M[6][6]=9
M[6][8]=9

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

def prettyPrint(X):
	for i in range(n):
		#print top
		for j in range(n):
			print "  ",
			print colored(X[i][j][top].Value(),colors[X[i][j][top].Value()]),
			print "  ", 
		print
		#print left and right
		for j in range(n):
			print colored(X[i][j][left].Value(),colors[X[i][j][left].Value()]),
			print " "+ colored(X[i][j][left].Value(),colors[X[i][j][left].Value()])+" ",
			print colored(X[i][j][right].Value(),colors[X[i][j][right].Value()]), 
		print
		#print bottom
		for j in range(n):
			print "  ",
			print colored(X[i][j][bottom].Value(),colors[X[i][j][bottom].Value()]),
			print "  ", 
		print

def prettyPrintM(M):
	for i in range(n):
		for j in range(n):
			print M[i][j],
		print

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

if solver.NextSolution():
	prettyPrint(X)
else:
	print "No solution found :("