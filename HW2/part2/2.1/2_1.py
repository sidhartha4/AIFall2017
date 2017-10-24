from array import array
from collections import deque
import Queue as queue
import time
from heapq import heappush
from heapq import heappop
from heapq import heapify
import random
from copy import deepcopy

from datetime import datetime



def defensiveHeuristicOne(content, whoseMove):

	val = 0
	for row in content:
		for col in row:
			if col == whoseMove:
				val = val + 2;

	val = val + random.random()
	#2*(number_of_own_pieces_remaining) + random()
	return val

def offensiveHeuristicOne(content, whoseMove):

	val = 60
	for row in content:
		for col in row:
			if (col == 1 and whoseMove == 2) or (col == 2 and whoseMove == 1):
				val = val - 2;

	val = val + random.random()
	#2*(number_of_own_pieces_remaining) + random()
	return val

def MovesPossibleToMake(node, whoseMove):

	content = node[0]
	whitePieces = node[1]
	blackPieces = node[2]


	#print(whoseMove)
	moveList = []
	i = 0
	for row in content:
		j = 0

		for col in row:			
			
			if col == 1 and whoseMove == 1:
			
				newBoard = deepcopy(content)	
			
				if i-1 >=0 and j+1 < len(row) and newBoard[i-1][j+1] == 2: 

					newBoard[i][j] = 0
					newBoard[i-1][j+1] = 1

					node = [newBoard, whitePieces, blackPieces-1]
					moveList.append(node)

				elif i-1 >=0 and j+1 < len(row) and newBoard[i-1][j+1] == 0:

					newBoard[i][j] = 0
					newBoard[i-1][j+1] = 1

					node = [newBoard, whitePieces, blackPieces]
					moveList.append(node)

				newBoard = deepcopy(content)


				if i-1 >=0 and j-1 >= 0 and newBoard[i-1][j-1] == 2:				

					newBoard[i][j] = 0
					newBoard[i-1][j-1] = 1

					node = [newBoard, whitePieces, blackPieces-1]
					moveList.append(node)

				elif i-1 >=0 and j-1 >= 0 and newBoard[i-1][j-1] == 0:

					newBoard[i][j] = 0
					newBoard[i-1][j-1] = 1

					node = [newBoard, whitePieces, blackPieces]
					moveList.append(node)

				newBoard = deepcopy(content)

				if i-1 >=0 and newBoard[i-1][j] == 0:

					newBoard[i][j] = 0
					newBoard[i-1][j] = 1

					node = [newBoard, whitePieces, blackPieces]
					moveList.append(node)

	
			elif col == 2 and whoseMove == 2:
	
				newBoard = deepcopy(content)	

				if i+1 <len(row) and j+1 <len(row) and newBoard[i+1][j+1] == 1: 

					newBoard[i][j] = 0
					newBoard[i+1][j+1] = 2

					node = [newBoard, whitePieces-1, blackPieces]
					moveList.append(node)

				elif i+1 <len(row) and j+1 <len(row) and newBoard[i+1][j+1] == 0:

					newBoard[i][j] = 0
					newBoard[i+1][j+1] = 2

					node = [newBoard, whitePieces, blackPieces]
					moveList.append(node)

				newBoard = deepcopy(content)

				if i+1 <len(row) and j-1 >=0 and newBoard[i+1][j-1] == 1:				

					newBoard[i][j] = 0
					newBoard[i+1][j-1] = 2

					node = [newBoard, whitePieces-1, blackPieces]
					moveList.append(node)

				elif i+1 <len(row) and j-1 >=0 and newBoard[i+1][j-1] == 0:

					newBoard[i][j] = 0
					newBoard[i+1][j-1] = 2

					node = [newBoard, whitePieces, blackPieces]
					moveList.append(node)

				newBoard = deepcopy(content)

				if i+1 < len(row) and newBoard[i+1][j] == 0:

					newBoard[i][j] = 0
					newBoard[i+1][j] = 2

					node = [newBoard, whitePieces, blackPieces]
					moveList.append(node)

			j = j+1

		i = i+1



	return moveList


def printBoard(board):

	print("-----------------------------------------")
	for j in board:
		
		stri = ""
		for k in j:
			stri = stri + str(k)
		print(stri)
	print("-----------------------------------------")






def alphaBeta(node, whoseMove, strategy, isMax, depth, totDepth, maxVal, minVal):


	if depth == totDepth:
		score = None
		if strategy == "Def":
			score = defensiveHeuristicOne(node[0], whoseMove)
		elif strategy == "Off":
			score = offensiveHeuristicOne(node[0], whoseMove)

		retTot = [score, node]

		return retTot;



	if isMax == 1:
		
		moveList = MovesPossibleToMake(node,whoseMove)

		nodeStatus = deepcopy(node)

		newMove = deepcopy(whoseMove)

		newMax = 0

		for i in moveList:

			nodeNew = deepcopy(i)

			evalTot = alphaBeta(nodeNew, newMove, strategy, newMax, depth+1, totDepth, maxVal, minVal)

			if maxVal < evalTot[0]:
				nodeStatus = i
				maxVal = evalTot[0]

			if evalTot[0] >= minVal:
				break
		#print(maxVal)

		retTot = [maxVal, nodeStatus] 
		return retTot

	else:

		moveList = MovesPossibleToMake(node,whoseMove)

		nodeStatus = deepcopy(node)

		newMove = deepcopy(whoseMove)

		newMax = 1

		for i in moveList:

			nodeNew = deepcopy(i)
			
			evalTot = alphaBeta(nodeNew, newMove, strategy, newMax, depth+1, totDepth, maxVal, minVal)

			if minVal > evalTot[0]:
				nodeStatus = i
				minVal = evalTot[0]

			if evalTot[0] <= maxVal:
				break


		retTot = [minVal, nodeStatus] 
		return retTot







def miniMax(node, whoseMove, strategy, isMax, depth, totDepth):


	if depth == totDepth:
		score = None
		if strategy == "Def":
			score = defensiveHeuristicOne(node[0], whoseMove)
		elif strategy == "Off":
			score = offensiveHeuristicOne(node[0], whoseMove)

		retTot = [score, node]

		return retTot;



	if isMax == 1:
		
		moveList = MovesPossibleToMake(node,whoseMove)

		maxVal = -1000000
		nodeStatus = None

		newMove = deepcopy(whoseMove)

		newMax = 0

		for i in moveList:

			nodeNew = deepcopy(i)

			evalTot = miniMax(nodeNew, newMove, strategy, newMax, depth+1, totDepth)

			if maxVal < evalTot[0]:
				nodeStatus = i
				maxVal = evalTot[0]

		#print(maxVal)

		retTot = [maxVal, nodeStatus] 
		return retTot

	else:

		moveList = MovesPossibleToMake(node,whoseMove)

		minVal = 1000000
		nodeStatus = None

		newMove = deepcopy(whoseMove)

		newMax = 1

		for i in moveList:

			nodeNew = deepcopy(i)
			
			evalTot = miniMax(nodeNew, newMove, strategy, newMax, depth+1, totDepth)

			if minVal > evalTot[0]:
				nodeStatus = i
				minVal = evalTot[0]

		retTot = [minVal, nodeStatus] 
		return retTot


def main(name):

	with open(name) as f:
		content = f.readlines()
	
	i = 0

	pieces = 0
	contentReal = []


	for row in content:

		row = row.strip()
		numberOfColumns = len(row)
		pieces = 2*numberOfColumns

		rowReal = []

		for col in row:
			rowReal.append(int(col))


		contentReal.append(rowReal)


	print(contentReal)
	whoseMove = 1;


	node = [contentReal,pieces,pieces]

	Player1 = "Off"
	Player2 = "Off"

	ka = 1
	printBoard(node[0])

	while 1:


		if node[1] != 0 and node[2] == 0:
			print("White wins")
			break

		if node[1] == 0 and node[2] != 0:	

			print("Black wins")
			break

		matCheck = node[0][0]
		matCheck2 = node[0][len(node[0])-1]
		flagCheck = 0
		for i in matCheck:
			if i == 1:
				print("White wins")
				flagCheck = 1
				break

		if flagCheck == 1:
			break

		flagCheck = 0
	
		for i in matCheck2:
			if i == 2:
				print("Black wins")
				flagCheck = 1
				break

		if flagCheck == 1:
			break


		Currnode = deepcopy(node)

		strategy = None

		if whoseMove == 1:
			strategy = Player1
		else:
			strategy = Player2

		depth = 0
		totDepth = 3
		isMax = 1

		moveChange = None
		delta = None

		if whoseMove == 1:

			t1 = datetime.now()
			moveChange = miniMax(Currnode, whoseMove, strategy, isMax, depth, totDepth)
			t2 = datetime.now()
			delta = t2 - t1
			

		else:
			
			t1 = datetime.now()
			moveChange = alphaBeta(node, whoseMove, strategy, isMax, depth, totDepth, -100000, 100000)
			t2 = datetime.now()
			delta = t2 - t1

		node = moveChange[1]	

		print("--------------------------------------------------------------------------------")

		print("move number :" + str(ka))

		if ka%2 == 0 and ka != 0:
			print("Black move:")
		elif ka%2 == 1:
			print("White move:")
			
		printBoard(node[0])

		print(moveChange)

		print(delta)

		print("-------------------------------------------------------------------------------")


		if whoseMove == 1:
			whoseMove = 2
		else:
			whoseMove = 1
		
		ka = ka + 1



if __name__ == "__main__":
	
	main('input.txt')