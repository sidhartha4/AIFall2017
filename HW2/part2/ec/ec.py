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
from bisect import bisect


'''


Re-search and search speed 
improvements are done with transposition tables, move ordering 
(in order to provide better Alpha-Beta pruning), and Null
Move Heuristic (speeds the Negamax algorithm by identifying 
cutoffs, points in the game tree where the current position 
is so good for the side to move that the best play by the other side would have avoided it).




'''

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
	[1, 1, 1, 1, 1, 1, 1, 1], [50, 50, 50, 50, 50, 50, 50, 50]]

	valMatWhite = [[50, 50, 50, 50, 50, 50, 50, 50], [1, 1, 1, 1, 1, 1, 1, 1],  \
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
					val = val - 50
			if i == len(content)-2 and whoseMove == 1:
				if col == 2:
					val = val - 50

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


def offensiveHeuristicTwo(node, whoseMove):

	valMatBlack = [[1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [2, 2, 2, 2, 2, 2, 2, 2], \
	[2, 2, 2, 2, 2, 2, 2, 2], [3, 3, 3, 3, 3, 3, 3, 3],  [3, 3, 3, 3, 3, 3, 3, 3], \
	[4, 4, 4, 4, 4, 4, 4, 4], [100, 100, 100, 100, 100, 100, 100, 100]]

	valMatWhite = [[100, 100, 100, 100, 100, 100, 100, 100], [4, 4, 4, 4, 4, 4, 4, 4],  \
	[3, 3, 3, 3, 3, 3, 3, 3], [3, 3, 3, 3, 3, 3, 3, 3], [2, 2, 2, 2, 2, 2, 2, 2], \
	[2, 2, 2, 2, 2, 2, 2, 2], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1]]
	

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
			val = val + 4*(node[1] - node[2])

	else:
		#if node[2] > node[1]:
			val = val + 4*(node[2] - node[1])

	content = deepcopy(node[0])
	newBoard = deepcopy(content)


	i = 0


	for row in content:
		j = 0
		for col in row:
			if i == 1 and whoseMove == 2:
				if col == 1:
					val = val - 50
			if i == len(content)-2 and whoseMove == 1:
				if col == 2:
					val = val - 50

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




def MovesPossibleToMake(node, whoseMove,strategy):

	#print(len(transpositionTabWhite))

	content = node[0]
	whitePieces = node[1]
	blackPieces = node[2]
	stringForm = node[3]

	#print(whoseMove)
	moveList = []
	i = 0
	for row in content:
		j = 0

		for col in row:			
			
			if col == 1 and whoseMove == 1:
			
				newBoard = deepcopy(content)	
			
				newstringForm = deepcopy(stringForm)

				if i-1 >=0 and j+1 < len(row) and newBoard[i-1][j+1] == 2: 

					newBoard[i][j] = 0
					newBoard[i-1][j+1] = 1

					newstringFormFinal = array("c", newstringForm)

					newstringFormFinal[(i-1)*len(row)+j+1] = "1"
					newstringFormFinal[i*len(row)+j] = "0"

					newstringFormFinal = newstringFormFinal.tostring()

					node = [newBoard, whitePieces, blackPieces-1, newstringFormFinal]
					moveList.append(node)
					

					'''
					if keyHere not in transpositionTabWhite:
						transpositionTabWhite.add(keyHere)
						print("1")
					else:
						print("-------------key----------------")
						print(keyHere)
						print("-----------------------------")
						print("2")

					'''

					'''

					if newstringFormFinal not in transpositionTabWhite:

						node = [newBoard, whitePieces, blackPieces-1, newstringFormFinal]
						moveList.append(node)
						transpositionTabWhite.add(newstringFormFinal)
					'''


					'''
					newstringFormFinal = newstringForm[:(i-1)*len(row)+j+1] + "1" + \
					newstringForm[(i-1)*len(row)+j+2 : i*len(row)+j] + "0" + \
					newstringForm[i*len(row)+j+1 :]

					node = [newBoard, whitePieces, blackPieces-1, newstringFormFinal]
					moveList.append(node)

					
					if newstringFormFinal in transpositionTabWhite:
						transpositionTabWhite[newstringFormFinal] = \
						transpositionTabWhite[newstringFormFinal] + 1
					else:
						transpositionTabWhite[newstringFormFinal] = 1
						node = [newBoard, whitePieces, blackPieces-1, newstringFormFinal]
						moveList.append(node)
					'''



				elif i-1 >=0 and j+1 < len(row) and newBoard[i-1][j+1] == 0:

					newBoard[i][j] = 0
					newBoard[i-1][j+1] = 1

					newstringFormFinal = array("c", newstringForm)

					newstringFormFinal[(i-1)*len(row)+j+1] = "1"
					newstringFormFinal[i*len(row)+j] = "0"

					newstringFormFinal = newstringFormFinal.tostring()

					node = [newBoard, whitePieces, blackPieces, newstringFormFinal]
					moveList.append(node)


				newBoard = deepcopy(content)

				newstringForm = deepcopy(stringForm)


				if i-1 >=0 and j-1 >= 0 and newBoard[i-1][j-1] == 2:				

					newBoard[i][j] = 0
					newBoard[i-1][j-1] = 1

					newstringFormFinal = array("c", newstringForm)

					newstringFormFinal[(i-1)*len(row)+j-1] = "1"
					newstringFormFinal[i*len(row)+j] = "0"

					newstringFormFinal = newstringFormFinal.tostring()

					node = [newBoard, whitePieces, blackPieces-1, newstringFormFinal]
					moveList.append(node)


				elif i-1 >=0 and j-1 >= 0 and newBoard[i-1][j-1] == 0:

					newBoard[i][j] = 0
					newBoard[i-1][j-1] = 1


					newstringFormFinal = array("c", newstringForm)

					newstringFormFinal[(i-1)*len(row)+j-1] = "1"
					newstringFormFinal[i*len(row)+j] = "0"

					newstringFormFinal = newstringFormFinal.tostring()

					node = [newBoard, whitePieces, blackPieces, newstringFormFinal]
					moveList.append(node)



				newBoard = deepcopy(content)

				newstringForm = deepcopy(stringForm)


				if i-1 >=0 and newBoard[i-1][j] == 0:

					newBoard[i][j] = 0
					newBoard[i-1][j] = 1


					newstringFormFinal = array("c", newstringForm)

					newstringFormFinal[(i-1)*len(row)+j] = "1"
					newstringFormFinal[i*len(row)+j] = "0"

					newstringFormFinal = newstringFormFinal.tostring()

					node = [newBoard, whitePieces, blackPieces, newstringFormFinal]
					moveList.append(node)


	
			elif col == 2 and whoseMove == 2:
	
				newBoard = deepcopy(content)	

				newstringForm = deepcopy(stringForm)


				if i+1 <len(content) and j+1 <len(row) and newBoard[i+1][j+1] == 1: 

					newBoard[i][j] = 0
					newBoard[i+1][j+1] = 2


					newstringFormFinal = array("c", newstringForm)

					newstringFormFinal[(i+1)*len(row)+j+1] = "2"
					newstringFormFinal[i*len(row)+j] = "0"

					newstringFormFinal = newstringFormFinal.tostring()


					node = [newBoard, whitePieces-1, blackPieces, newstringFormFinal]
					moveList.append(node)


				elif i+1 <len(content) and j+1 <len(row) and newBoard[i+1][j+1] == 0:

					newBoard[i][j] = 0
					newBoard[i+1][j+1] = 2

					newstringFormFinal = array("c", newstringForm)

					newstringFormFinal[(i+1)*len(row)+j+1] = "2"
					newstringFormFinal[i*len(row)+j] = "0"

					newstringFormFinal = newstringFormFinal.tostring()


					node = [newBoard, whitePieces, blackPieces, newstringFormFinal]
					moveList.append(node)


				newBoard = deepcopy(content)

				newstringForm = deepcopy(stringForm)


				if i+1 <len(content) and j-1 >=0 and newBoard[i+1][j-1] == 1:				

					newBoard[i][j] = 0
					newBoard[i+1][j-1] = 2

					newstringFormFinal = array("c", newstringForm)

					newstringFormFinal[(i+1)*len(row)+j-1] = "2"
					newstringFormFinal[i*len(row)+j] = "0"

					newstringFormFinal = newstringFormFinal.tostring()


					node = [newBoard, whitePieces-1, blackPieces, newstringFormFinal]
					moveList.append(node)


				elif i+1 <len(content) and j-1 >=0 and newBoard[i+1][j-1] == 0:

					newBoard[i][j] = 0
					newBoard[i+1][j-1] = 2

					newstringFormFinal = array("c", newstringForm)

					newstringFormFinal[(i+1)*len(row)+j-1] = "2"
					newstringFormFinal[i*len(row)+j] = "0"

					newstringFormFinal = newstringFormFinal.tostring()

					node = [newBoard, whitePieces, blackPieces, newstringFormFinal]
					moveList.append(node)


				newBoard = deepcopy(content)

				newstringForm = deepcopy(stringForm)

				if i+1 < len(content) and newBoard[i+1][j] == 0:

					newBoard[i][j] = 0
					newBoard[i+1][j] = 2


					newstringFormFinal = array("c", newstringForm)

					newstringFormFinal[(i+1)*len(row)+j] = "2"
					newstringFormFinal[i*len(row)+j] = "0"

					newstringFormFinal = newstringFormFinal.tostring()

					node = [newBoard, whitePieces, blackPieces, newstringFormFinal]
					moveList.append(node)


			j = j+1

		i = i+1

	#return moveList

	finalList = []
	scoreList = []

	ja = 0

	for ia in moveList:

		score = 0

		if strategy == "Def":
			score = defensiveHeuristicOne(node[0], whoseMove)
		elif strategy == "Off":
			score = offensiveHeuristicOne(node[0], whoseMove)

		elif strategy == "Def2":
			score = defensiveHeuristicTwo(node, whoseMove)

		elif strategy == "Off2":
			score = offensiveHeuristicTwo(node, whoseMove)

		
		score = -1*score


		if ja != 0:
			index = bisect(scoreList, score)
			finalList.insert(index, ia)
			scoreList = scoreList.insert(index,score)
		else:
			finalList.append(ia)
			scoreList.append(score)
		
	
	return finalList


def printBoard(board):

	print("-----------------------------------------")
	for j in board:
		
		stri = ""
		for k in j:
			stri = stri + str(k)
		print(stri)
	print("-----------------------------------------")




transpositionTabWhite = dict()
transpositionTabBlack = dict()


def alphaBeta(node, whoseMove, strategy, isMax, depth, totDepth, maxVal, minVal):

	positionNow = ""
	if whoseMove == 1:
		positionNow = node[3]+str(depth)

		if positionNow in transpositionTabWhite:
			retTot = [transpositionTabWhite[positionNow], node]
			#print("evalAl")
			return retTot

	else:

		positionNow = node[3]+str(depth)

		if positionNow in transpositionTabBlack:
			retTot = [transpositionTabWhite[positionNow], node]
			#print("evalAl")
			return retTot


	if depth == totDepth:
		
		score = 0
		
		if strategy == "Def":
			score = defensiveHeuristicOne(node[0], whoseMove)
		elif strategy == "Off":
			score = offensiveHeuristicOne(node[0], whoseMove)
		
		elif strategy == "Def2":
			score = defensiveHeuristicTwo(node, whoseMove)

		elif strategy == "Off2":
			score = offensiveHeuristicTwo(node, whoseMove)

		retTot = [score, node]

		return retTot;



	if isMax == 1:
		
		#print("yeah1")
		moveList = MovesPossibleToMake(node,whoseMove,strategy)



		if len(moveList) == 0:
			score = 0
		
			if strategy == "Def":
				score = defensiveHeuristicOne(node[0], whoseMove)
			elif strategy == "Off":
				score = offensiveHeuristicOne(node[0], whoseMove)
			
			elif strategy == "Def2":
				score = defensiveHeuristicTwo(node, whoseMove)

			elif strategy == "Off2":
				score = offensiveHeuristicTwo(node, whoseMove)

			retTot = [score, node]

			return retTot;
 


		nodeStatus = deepcopy(node)

		newMove = deepcopy(whoseMove)

		newMax = 0

		v = [-1000000,nodeStatus]
		#print(len(moveList))


		for i in moveList:

		#	for ja in i[0]:
		#		print(ja)
			


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
		transpositionTabWhite[positionNow] = v[0]
		return retTot

	else:

		#print("yeah2")
		moveList = []
		if whoseMove == 1:
			moveList = MovesPossibleToMake(node,2,strategy)
		else:
			moveList = MovesPossibleToMake(node,1,strategy)


		if len(moveList) == 0:
			score = 0
		
			if strategy == "Def":
				score = defensiveHeuristicOne(node[0], whoseMove)
			elif strategy == "Off":
				score = offensiveHeuristicOne(node[0], whoseMove)
			
			elif strategy == "Def2":
				score = defensiveHeuristicTwo(node, whoseMove)

			elif strategy == "Off2":
				score = offensiveHeuristicTwo(node, whoseMove)

			retTot = [score, node]

			return retTot;



		nodeStatus = deepcopy(node)

		newMove = deepcopy(whoseMove)

		newMax = 1

		
		v = [1000000, nodeStatus]

		#print(len(moveList))



		for i in moveList:

		#	for ja in i[0]:
		#		print(ja)
			
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
		transpositionTabWhite[positionNow] = v[0]
		return retTot







def miniMax(node, whoseMove, strategy, isMax, depth, totDepth):


	if depth == totDepth:
		score = 0
		if strategy == "Def":
			score = defensiveHeuristicOne(node[0], whoseMove)
		elif strategy == "Off":
			score = offensiveHeuristicOne(node[0], whoseMove)
		elif strategy == "Def2":
			score = defensiveHeuristicTwo(node, whoseMove)
		elif strategy == "Off2":
			score = offensiveHeuristicTwo(node, whoseMove)


		retTot = [score, node]

		return retTot;



	if isMax == 1:
		
		moveList = MovesPossibleToMake(node,whoseMove,strategy)


		if len(moveList) == 0:
			score = 0
		
			if strategy == "Def":
				score = defensiveHeuristicOne(node[0], whoseMove)
			elif strategy == "Off":
				score = offensiveHeuristicOne(node[0], whoseMove)
			
			elif strategy == "Def2":
				score = defensiveHeuristicTwo(node, whoseMove)

			elif strategy == "Off2":
				score = offensiveHeuristicTwo(node, whoseMove)

			retTot = [score, node]

			return retTot;



		maxVal = -1000000
		nodeStatus = deepcopy(node)

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

		moveList = []
		if whoseMove == 1:
			moveList = MovesPossibleToMake(node,2,strategy)
		else:
			moveList = MovesPossibleToMake(node,1,strategy)


		if len(moveList) == 0:
			score = 0
		
			if strategy == "Def":
				score = defensiveHeuristicOne(node[0], whoseMove)
			elif strategy == "Off":
				score = offensiveHeuristicOne(node[0], whoseMove)
			
			elif strategy == "Def2":
				score = defensiveHeuristicTwo(node, whoseMove)

			elif strategy == "Off2":
				score = offensiveHeuristicTwo(node, whoseMove)

			retTot = [score, node]

			return retTot;



		minVal = 1000000
		nodeStatus = deepcopy(node)

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


def main(name, Player1, Player2, Player1SearchType, Player2SearchType):

	with open(name) as f:
		content = f.readlines()
	
	i = 0

	pieces = 0
	contentReal = []
	stringReal = ""
	whitePieces = 0
	blackPieces = 0
	for row in content:

		row = row.strip()
		numberOfColumns = len(row)
		pieces = 2*numberOfColumns

		rowReal = []

		for col in row:
			if col == "1":
				whitePieces = whitePieces + 1
			elif col == "2":
				blackPieces = blackPieces + 1

			rowReal.append(int(col))
			stringReal = stringReal + col

		contentReal.append(rowReal)


	print(contentReal)
	whoseMove = 1;


	node = [contentReal, whitePieces, blackPieces, stringReal]


	ka = 1
	printBoard(node[0])

	#transpositionTabWhite.clear()
	#transpositionTabBlack.clear()

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
		totDepth2 = 3
		isMax = 1

		moveChange = None
		delta = None

		if whoseMove == 1:

			t1 = datetime.now()

			if Player1SearchType == "min":
				#moveChange = alphaBeta(Currnode, whoseMove, strategy, isMax, depth, totDepth, -100000, 100000)
				moveChange = miniMax(Currnode, whoseMove, strategy, isMax, depth, totDepth)
			elif Player1SearchType == "alphaB":
				moveChange = alphaBeta(Currnode, whoseMove, strategy, isMax, depth, totDepth, -100000, 100000)

			t2 = datetime.now()

			delta = t2 - t1
			

		else:
			
			t1 = datetime.now()


			if Player2SearchType == "min":
				#moveChange = alphaBeta(Currnode, whoseMove, strategy, isMax, depth, totDepth, -100000, 100000)
				moveChange = miniMax(Currnode, whoseMove, strategy, isMax, depth, totDepth2)
			elif Player2SearchType == "alphaB":
				moveChange = alphaBeta(Currnode, whoseMove, strategy, isMax, depth, totDepth2, -100000, 100000)

			#moveChange = alphaBeta(Currnode, whoseMove, strategy, isMax, depth, totDepth2, -100000, 100000)
			
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



if __name__ == "__main__":

	Player1 = "Def2"
	Player2 = "Off"
	
	main('input.txt', Player1, Player2, "alphaB", "alphaB")

	Player3 = "Off2"
	Player4 = "Def"

	#main('input.txt', Player3, Player4, "alphaB", "alphaB")
	