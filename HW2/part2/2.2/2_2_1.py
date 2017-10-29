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



def defensiveHeuristicTwo(node, whoseMove):


	valMatBlack = [[1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], \
	[1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1],  [1, 1, 1, 1, 1, 1, 1, 1], \
	[1, 1, 1, 1, 1, 1, 1, 1], [10, 10, 10, 10, 10, 10, 10, 10]]

	valMatWhite = [[10, 10, 10, 10, 10, 10, 10, 10], [1, 1, 1, 1, 1, 1, 1, 1],  \
	[1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], \
	[1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1]]
	

	'''
	valMatBlack = [[5, 15, 15, 5, 5, 15, 15, 5], [2, 3, 3, 3, 3, 3, 3, 2], [4, 6, 6, 6, 6, 6, 6, 4], \
	[7, 10, 10, 10, 10, 10, 10, 7], [11, 15, 15, 15, 15, 15, 15, 11],  [16, 21, 21, 21, 21, 21, 21, 16], \
	[20, 28, 28, 28, 28, 28, 28, 20], [36, 36, 36, 36, 36, 36, 36, 36]]

	valMatWhite = [[36, 36, 36, 36, 36, 36, 36, 36], [20, 28, 28, 28, 28, 28, 28, 20],  \
	[16, 21, 21, 21, 21, 21, 21, 16], [11, 15, 15, 15, 15, 15, 15, 11], [7, 10, 10, 10, 10, 10, 10, 7], \
	[4, 6, 6, 6, 6, 6, 6, 4], [2, 3, 3, 3, 3, 3, 3, 2],[5, 15, 15, 5, 5, 15, 15, 5]]
	'''

	val = 0
	if whoseMove == 1:
		#if node[1] > node[2]:
			val = val + 2*(node[1] - node[2])

	else:
		#if node[2] > node[1]:
			val = val + 2*(node[2] - node[1])

	content = deepcopy(node[0])
	newBoard = deepcopy(content)


	i = 0




	for row in content:
		j = 0
		for col in row:
			if i == 1 and whoseMove == 2:
				if col == 1:
					val = val - 100
			if i == len(content)-2 and whoseMove == 1:
				if col == 2:
					val = val - 100

			if col == 1 and whoseMove == 1:

				val2 = 0

				if i+1 < len(content) and j+1 < len(row) and newBoard[i+1][j+1] == 1: 
					val2 = val2+1

				if i+1 < len(content) and j-1 >= 0 and newBoard[i+1][j-1] == 1: 
					val2 = val2+1
					
				if i-1 >= 0 and j+1 < len(row)  and newBoard[i-1][j+1] == 2: 
					val2 = val2-1
				
				if i-1 >= 0  and j-1 >= 0 and newBoard[i-1][j-1] == 2: 
					val2 = val2-1
				


				val3 = 0
					
				if i-1 >= 0 and j+1 < len(row)  and newBoard[i-1][j+1] == 1: 
					val3 = val3+0.25
				
				if i-1 >= 0  and j-1 >= 0 and newBoard[i-1][j-1] == 1: 
					val3 = val3+0.25
				
				if i-1 >= 0 and newBoard[i-1][j] == 1: 
					val3 = val3+0.25
				
				if i-2 >= 0  and j-1 >= 0 and newBoard[i-2][j-1] == 1: 
					val3 = val3+0.25
				
				if i-2 >= 0 and j+1 < len(row)  and newBoard[i-2][j+1] == 1: 
					val3 = val3+0.25
				
				if i-2 >= 0 and newBoard[i-2][j] == 1: 
					val3 = val3+0.25
				
				val = val + val3	


				if val2 > 0:
					val = val + valMatWhite[i][j]*1.5
				else:
					val = val + valMatWhite[i][j]




			elif col == 2 and whoseMove == 2:

				val2 = 0

				if i-1 >= 0 and j+1 < len(row) and newBoard[i-1][j+1] == 2: 
					val2 = val2+1

				if i-1 >= 0 and j-1 >= 0 and newBoard[i-1][j-1] == 2: 
					val2 = val2+1
					
				if i+1 < len(content) and j+1 < len(row)  and newBoard[i+1][j+1] == 1: 
					val2 = val2-1
				
				if i+1 < len(content) and j-1 >= 0 and newBoard[i+1][j-1] == 1: 
					val2 = val2-1


				val3 = 0
					
				if i+1 < len(content) and j+1 < len(row)  and newBoard[i+1][j+1] == 1: 
					val3 = val3+0.25
				
				if i+1 < len(content)  and j-1 >= 0 and newBoard[i+1][j-1] == 1: 
					val3 = val3+0.25
				
				if i+1 < len(content) and newBoard[i+1][j] == 1: 
					val3 = val3+0.25
				
				if i+2 < len(content)  and j-1 >= 0 and newBoard[i+2][j-1] == 1: 
					val3 = val3+0.25
				
				if i+2 < len(content) and j+1 < len(row)  and newBoard[i+2][j+1] == 1: 
					val3 = val3+0.25
				
				if i+2 < len(content) and newBoard[i+2][j] == 1: 
					val3 = val3+0.25
				
				val = val + val3	

				
				if val2 > 0:
					val = val + valMatBlack[i][j]*1.5
				else:
					val = val + valMatBlack[i][j]

			j = j+1
		i = i+1

	val = val + random.random()
	return val

def offensiveHeuristicTwo(content, whoseMove):

	val = 0
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

				if i+1 <len(content) and j+1 <len(row) and newBoard[i+1][j+1] == 1: 

					newBoard[i][j] = 0
					newBoard[i+1][j+1] = 2

					node = [newBoard, whitePieces-1, blackPieces]
					moveList.append(node)

				elif i+1 <len(content) and j+1 <len(row) and newBoard[i+1][j+1] == 0:

					newBoard[i][j] = 0
					newBoard[i+1][j+1] = 2

					node = [newBoard, whitePieces, blackPieces]
					moveList.append(node)

				newBoard = deepcopy(content)

				if i+1 <len(content) and j-1 >=0 and newBoard[i+1][j-1] == 1:				

					newBoard[i][j] = 0
					newBoard[i+1][j-1] = 2

					node = [newBoard, whitePieces-1, blackPieces]
					moveList.append(node)

				elif i+1 <len(content) and j-1 >=0 and newBoard[i+1][j-1] == 0:

					newBoard[i][j] = 0
					newBoard[i+1][j-1] = 2

					node = [newBoard, whitePieces, blackPieces]
					moveList.append(node)

				newBoard = deepcopy(content)

				if i+1 < len(content) and newBoard[i+1][j] == 0:

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
		
		elif strategy == "Def2":
			score = defensiveHeuristicTwo(node, whoseMove)

		retTot = [score, node]

		return retTot;



	if isMax == 1:
		
		#print("yeah1")
		moveList = MovesPossibleToMake(node,whoseMove)

		nodeStatus = deepcopy(node)

		newMove = deepcopy(whoseMove)

		newMax = 0

		v = [-1000000,nodeStatus]

		for i in moveList:

			nodeNew = deepcopy(i)

			evalTot = alphaBeta(nodeNew, newMove, strategy, newMax, depth+1, totDepth, maxVal, minVal)

			if v[0] < evalTot[0]:
				v[0] = evalTot[0]
				v[1] = i


			if v[0] >= minVal:
				break

			if maxVal < v[0]:
				maxVal = v[0]

		#print(maxVal)

		retTot = v 
		return retTot

	else:

		#print("yeah2")
		moveList = MovesPossibleToMake(node,whoseMove)

		nodeStatus = deepcopy(node)

		newMove = deepcopy(whoseMove)

		newMax = 1

		v = [1000000, nodeStatus]

		for i in moveList:

			nodeNew = deepcopy(i)
			
			evalTot = alphaBeta(nodeNew, newMove, strategy, newMax, depth+1, totDepth, maxVal, minVal)

			if v[0] > evalTot[0]:
				v[0] = evalTot[0]
				v[1] = i

			if v[0] <= maxVal:
				break

			if minVal > v[0]:
				minVal = v[0]


		retTot = v 
		return retTot







def miniMax(node, whoseMove, strategy, isMax, depth, totDepth):


	if depth == totDepth:
		score = None
		if strategy == "Def":
			score = defensiveHeuristicOne(node[0], whoseMove)
		elif strategy == "Off":
			score = offensiveHeuristicOne(node[0], whoseMove)

		elif strategy == "Def2":
			score = defensiveHeuristicTwo(node, whoseMove)

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

	Player1 = "Def2"
	Player2 = "Off"

	ka = 1
	printBoard(node[0])

	filetoWrite = open('workfile2.txt', 'w')


	while 1:


		if node[1] >= 3 and node[2] < 3:
			print("White wins")
			break

		if node[1] < 3 and node[2] >= 3:	

			print("Black wins")
			break

		matCheck = node[0][0]
		matCheck2 = node[0][len(node[0])-1]
		flagCheck = 0
		for i in matCheck:
			if i == 1:
				flagCheck = flagCheck + 1
				

		if flagCheck >= 3:

			print("White wins")
			break

		flagCheck = 0
	
		for i in matCheck2:
			if i == 2:
				flagCheck = flagCheck + 1
				

		if flagCheck >= 3:
			print("Black wins")
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
			
			moveChange = alphaBeta(Currnode, whoseMove, strategy, isMax, depth, totDepth, -100000, 100000)
			#moveChange = miniMax(Currnode, whoseMove, strategy, isMax, depth, totDepth)
			t2 = datetime.now()
			delta = t2 - t1
			

		else:
			
			t1 = datetime.now()
			moveChange = alphaBeta(Currnode, whoseMove, strategy, isMax, depth, totDepth, -100000, 100000)
			t2 = datetime.now()
			delta = t2 - t1

		node = moveChange[1]	

		print("--------------------------------------------------------------------------------")

		print("move number :" + str(ka))

		if ka%2 == 0 and ka != 0:
			print("Black move:")
		elif ka%2 == 1:
			print("White move:")
			

		if node != None:	
			printBoard(node[0])

			for iaa in node[0]:
				for jaa in iaa:
					filetoWrite.write(str(jaa)+" ")
				filetoWrite.write('\n')	

			filetoWrite.write('\n')

		else:
			print(node)

		print(moveChange)

		print(delta)

		print("-------------------------------------------------------------------------------")


		if whoseMove == 1:
			whoseMove = 2
		else:
			whoseMove = 1
		
		ka = ka + 1

	filetoWrite.close()


if __name__ == "__main__":
	
	main('input.txt')