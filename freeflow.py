#########################################################################
## TP d'optimisation 15 janvier 2015 Victor Duprez                     ##
## Define the matrix to solve in file data.py and launch this file     ##
#########################################################################

from __future__ import print_function
import sys
from ortools.constraint_solver import pywrapcp
from termcolor import colored
from data import *


def findNbCouleurs(M):
	couleurs=[]
	nbcouleurs=0
	for i in range(len(M)):
		for j in range(len(M)):
			if M[i][j] not in couleurs:
				couleurs += [M[i][j]]
				nbcouleurs +=1
	return [nbcouleurs, couleurs]

def getListColorsToDraw(nbcouleurs):
	colors = ['grey']
	while len(colors)<nbcouleurs:
		colors += ['red','green','yellow','blue','magenta','cyan','white']
	return colors

def prettyDrawSolution(X, M):
	for i in range(n):
		#print top
		for j in range(n):
			print ("  ",end=''),
			print (colored(X[i][j][top].Value(),'grey', "on_"+colors[X[i][j][top].Value()]),end=''),
			print ("  ",end=''), 
		print("")
		#print left center and right
		for j in range(n):
			print (colored(X[i][j][left].Value(),'grey', "on_"+colors[X[i][j][left].Value()]),end=''),
			for e in [top, bottom, right, left]:
				if X[i][j][e].Value() != 0:
					if M[i][j]!=0:
						print (""+ colored(X[i][j][e].Value(),'grey', "on_"+colors[X[i][j][e].Value()])+ colored(X[i][j][e].Value(),'grey', "on_"+colors[X[i][j][e].Value()])+ colored(X[i][j][e].Value(),colors[X[i][j][e].Value()], "on_"+colors[X[i][j][e].Value()])+"",end=''),
						break
					else:
						print (""+ colored(X[i][j][e].Value(),'grey', "on_"+colors[X[i][j][e].Value()])+ colored(X[i][j][e].Value(),'grey', "on_"+colors[X[i][j][e].Value()])+ colored(X[i][j][e].Value(),colors[X[i][j][e].Value()], "on_"+colors[X[i][j][e].Value()])+"",end=''),
						break
			print (colored(X[i][j][right].Value(),'grey', "on_"+colors[X[i][j][right].Value()]),end=''), 
		print("")
		#print bottom
		for j in range(n):
			print ("  ",end=''),
			print (colored(X[i][j][bottom].Value(),'grey', "on_"+colors[X[i][j][bottom].Value()]),end=''),
			print ("  ",end=''), 
		print("")

def prettyPrintM(M):
	for i in range(n):
		for j in range(n):
			print (M[i][j],end=''),
		print("")

def prettyDrawM(M):
	for i in range(n):
		for j in range(n):
			print("|"+ colored(M[i][j], 'grey', "on_"+colors[M[i][j]]),end=''),
		print("")
		for j in range(n):
			print("+-",end=''),
		print("")

def flatten(matr):
    rows = len(matr)
    cols = len(matr[0])
    elements = len(matr[0][0])
    return [matr[i][j][e] for e in range (elements) for j in range(cols) for i in range(rows)]

def displayMenu():
	print("#################################################################################")
	print("#################################################################################")
	print("")
	print(" WELCOME TO FLOW FREE SOLVER BY Victor DUPREZ")
	print("")
	print("#################################################################################")
	print("#################################################################################")
	print("What do you want to do?")
	print("1. Display puzzle to solve")
	print("2. Change puzzle to solve")
	print("3. Display solution to puzzle")
	print("4. Display menu")
	print("5. Display data choices")
	
def makeChoice():
	global M
	global n
	choice = input('Make your choice: ')
	print("")
	if choice == 1:
		print("1. Puzzle to solve is:")
		prettyDrawM(M)
		makeChoice()
	elif choice == 2:
		print("2. Change puzzle to solve: Add your puzzle to data.py file and enter the choice number you attributed it:")
		choix=input()
		[M,n]=initialPuzzle(choix)
		makeChoice()
	elif choice == 3:
		print("3. Solution to puzzle is:")
		solve()
		makeChoice()
	elif choice == 4:
		displayMenu()
		makeChoice()
	elif choice == 5:
		displayDataChoices()
		makeChoice()

def displayDataChoices():
	choix =1
	while initialPuzzle(choix)!=[[0],0]:
		print("Initial puzzle n "+str(choix))
		[M,n]=initialPuzzle(choix)
		prettyDrawM(M)
		print("")
		choix+=1

def solve():
	solver = pywrapcp.Solver("freeFlow")

	# Create variables 
	X  = [[[solver.IntVar(0, nbcouleurs +1, "X[%i][%i][%i]"  % (i,j,e)) for e in range(4)] for j in range(n)] for i in range(n)]

	###########################################################################################################
	# Add constraints
	# First line top edges must be 0
	for j in range (n):
		solver.Add(X[0][j][top] == 0)

	# Last line bottom edges must be 0
	for j in range (n):
		solver.Add(X[n-1][j][bottom] == 0)

	# First column left edges must be 0
	for i in range (n):
		solver.Add(X[i][0][left] == 0)

	# Last column right edges must be 0
	for i in range (n):
		solver.Add(X[i][n-1][right] == 0)

	# When case is an begining or ending point (i.e. M[i][j]!=0) only one edge can be not null
	for i in range(n):
		for j in range(n):
			if M[i][j]!=0:
					Mij=M[i][j]
					allowed = [(Mij,0,0,0),(0,Mij,0,0),(0,0,Mij,0),(0,0,0,Mij)]
					solver.Add(solver.AllowedAssignments(tuple(X[i][j]), allowed ))

	# Adjacent edges between cases must be equals
	for i in range(n-1):
		for j in range(n-1):
				solver.Add(X[i][j][bottom] == X[i+1][j][top])
				solver.Add(X[i][j+1][left] == X[i][j][right])
	for j in range(n-1):
		solver.Add(X[n-1][j+1][left] == X[n-1][j][right])
	for i in range(n-1):
			solver.Add(X[i][n-1][bottom] == X[i+1][n-1][top])

	# Regular cases (! begining or ending) can only have two edges colored and in the same color
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


	###########################################################################################################
	# Solve the model


	db = solver.Phase(flatten(X),
	            solver.INT_VAR_SIMPLE,
	            solver.ASSIGN_MAX_VALUE)

	solver.NewSearch(db)
	if solver.NextSolution():
		print("Solution found in: "+str(solver.WallTime())+"ms")
		prettyDrawSolution(X,M)
		
		return 1
	else:
		print ("No solution found :(")
		return 0

###########################################
## Useful variables
###########################################

top = 0
bottom = 1
left = 2
right = 3	

[M,n]=initialPuzzle(1)
[nbcouleurs, couleurs]=findNbCouleurs(M)
colors=getListColorsToDraw(nbcouleurs)

###########################################
## Start Menu
###########################################

displayMenu()
makeChoice()