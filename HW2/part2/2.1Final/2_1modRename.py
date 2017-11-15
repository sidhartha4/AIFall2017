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

# it is offensive
def offensiveHeuristicOne(content, whoseMove):

	val = 60
	for row in content:
		for col in row:
			if (col == 1 and whoseMove == 2) or (col == 2 and whoseMove == 1):
				val = val - 2;

	val = val + random.random()
	#2*(number_of_own_pieces_remaining) + random()
	return val


# it defends
def defensiveHeuristicTwo(node, whoseMove):


	valMatBlack = [[1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], \
	[1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1],  [1, 1, 1, 1, 1, 1, 1, 1], \
	[1, 1, 1, 1, 1, 1, 1, 1], [50, 50, 50, 50, 50, 50, 50, 50]]

	valMatWhite = [[50, 50, 50, 50, 50, 50, 50, 50], [1, 1, 1, 1, 1, 1, 1, 1],  \
	[1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], \
	[1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1]]
		

	val = 0
	if whoseMove == 1:
		#if node[1] > node[2]:
			val = val + 2.5*(node[1] - node[2])

	else:
		#if node[2] > node[1]:
			val = val + 2.5*(node[2] - node[1])

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
				#diagonal
				if i-1 >= 0 and j+1 < len(row)  and newBoard[i-1][j+1] == 1: 
					val3 = val3+0.3
				
				if i-1 >= 0  and j-1 >= 0 and newBoard[i-1][j-1] == 1: 
					val3 = val3+0.3
				
				#if i-1 >= 0 and newBoard[i-1][j] == 1: 
				#	val3 = val3+0.2
				
				if i-2 >= 0  and j-1 >= 0 and newBoard[i-2][j-1] == 1: 
					val3 = val3+0.2
				
				if i-2 >= 0 and j+1 < len(row)  and newBoard[i-2][j+1] == 1: 
					val3 = val3+0.2
				
				#if i-2 >= 0 and newBoard[i-2][j] == 1: 
				#	val3 = val3+0.25
				
				val = val + val3	


				if val2 > 0:
					val = val + valMatWhite[i][j]*1.5
				else:
					# if my pawn does not have enough defense
					val = val + valMatWhite[i][j]*0.8

				for index in range(0, 8):
					if(newBoard[0][index] == 1):
						val = 200


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
					val3 = val3+0.3
				
				if i+1 < len(content)  and j-1 >= 0 and newBoard[i+1][j-1] == 1: 
					val3 = val3+0.3
				
				#if i+1 < len(content) and newBoard[i+1][j] == 1: 
				#	val3 = val3+0.25
				
				if i+2 < len(content)  and j-1 >= 0 and newBoard[i+2][j-1] == 1: 
					val3 = val3+0.2
				
				if i+2 < len(content) and j+1 < len(row)  and newBoard[i+2][j+1] == 1: 
					val3 = val3+0.2
				
				#if i+2 < len(content) and newBoard[i+2][j] == 1: 
				#	val3 = val3+0.25
				
				val = val + val3	

				
				if val2 > 0:
					val = val + valMatBlack[i][j]*1.5
				else:
					val = val + valMatBlack[i][j]*0.8

				for index in range(0, 8):
					if(newBoard[7][index] == 2):
						val = 200

			j = j+1
		i = i+1

	val = val + random.random()
	return val

# it is offensive, it implements the research paper
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
					val3 = val3+0.1
				
				if i-1 >= 0  and j-1 >= 0 and newBoard[i-1][j-1] == 1: 
					val3 = val3+0.1
				
				if i-1 >= 0 and newBoard[i-1][j] == 1: 
					val3 = val3+0.1
				
				if i-2 >= 0  and j-1 >= 0 and newBoard[i-2][j-1] == 1: 
					val3 = val3+0.1
				
				if i-2 >= 0 and j+1 < len(row)  and newBoard[i-2][j+1] == 1: 
					val3 = val3+0.1
				
				if i-2 >= 0 and newBoard[i-2][j] == 1: 
					val3 = val3+0.1
				
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
					val3 = val3+0.1
				
				if i+1 < len(content)  and j-1 >= 0 and newBoard[i+1][j-1] == 1: 
					val3 = val3+0.1
				
				if i+1 < len(content) and newBoard[i+1][j] == 1: 
					val3 = val3+0.1
				
				if i+2 < len(content)  and j-1 >= 0 and newBoard[i+2][j-1] == 1: 
					val3 = val3+0.1
				
				if i+2 < len(content) and j+1 < len(row)  and newBoard[i+2][j+1] == 1: 
					val3 = val3+0.1
				
				if i+2 < len(content) and newBoard[i+2][j] == 1: 
					val3 = val3+0.1
				
				val = val + val3	

				
				if val2 > 0:
					val = val + valMatBlack[i][j]*1.5
				else:
					val = val + valMatBlack[i][j]

			j = j+1
		i = i+1

	val = val + random.random()
	return val



#this functions figures out ll the moves
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

#this functions implements alphabeta
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
			retTot = [transpositionTabBlack[positionNow], node]
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
		if whoseMove == 1:
			transpositionTabWhite[positionNow] = v[0]
		else:
			transpositionTabBlack[positionNow] = v[0]
		
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


		if whoseMove == 1:
			transpositionTabWhite[positionNow] = v[0]
		else:
			transpositionTabBlack[positionNow] = v[0]

		return retTot





#this function implements minimax
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


	if whoseMove == 1:
		global miniMaxNodesWhite
		miniMaxNodesWhite = miniMaxNodesWhite + 1
	else:
		global miniMaxNodesBlack
		miniMaxNodesBlack = miniMaxNodesBlack + 1


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




def main(name, Player1, Player2, Player1SearchType, Player2SearchType, totDepth1, totDepth2, fileName):

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


	#print(contentReal)
	whoseMove = 1;


	node = [contentReal, whitePieces, blackPieces, stringReal]


	ka = 1
	#printBoard(node[0])

	transpositionTabWhite.clear()
	transpositionTabBlack.clear()

	totalTimeWhite = 0
	totalTimeBlack = 0
	totalMoveWhite = 0
	totalMoveBlack = 0

	global miniMaxNodesWhite

	miniMaxNodesWhite = 0
	global miniMaxNodesBlack
	miniMaxNodesBlack = 0

	WinnerWho = 0

	filetoWrite = open(fileName, 'w')


	while 1:


		if node[1] != 0 and node[2] == 0:
			WinnerWho = 1
		#	print("White wins")
			break

		if node[1] == 0 and node[2] != 0:	
			WinnerWho = 2
		#	print("Black wins")
			break

		matCheck = node[0][0]
		matCheck2 = node[0][len(node[0])-1]
		flagCheck = 0
		for i in matCheck:
			if i == 1:
				WinnerWho = 1
		#		print("White wins")
				flagCheck = 1
				break

		if flagCheck == 1:
			break

		flagCheck = 0
	
		for i in matCheck2:
			if i == 2:
				WinnerWho = 2
		#		print("Black wins")
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
		isMax = 1

		moveChange = None
		delta = None

		if whoseMove == 1:

			t1 = datetime.now()

			if Player1SearchType == "min":
				#moveChange = alphaBeta(Currnode, whoseMove, strategy, isMax, depth, totDepth, -100000, 100000)
				moveChange = miniMax(Currnode, whoseMove, strategy, isMax, depth, totDepth1)
			elif Player1SearchType == "alphaB":
				moveChange = alphaBeta(Currnode, whoseMove, strategy, isMax, depth, totDepth1, -100000, 100000)

			t2 = datetime.now()

			delta = t2 - t1
			
			totalTimeWhite = totalTimeWhite + delta.total_seconds()
			
			totalMoveWhite = totalMoveWhite + 1
	


		else:
			
			t1 = datetime.now()


			if Player2SearchType == "min":
				moveChange = miniMax(Currnode, whoseMove, strategy, isMax, depth, totDepth2)
			elif Player2SearchType == "alphaB":
				moveChange = alphaBeta(Currnode, whoseMove, strategy, isMax, depth, totDepth2, -100000, 100000)

			
			t2 = datetime.now()
			delta = t2 - t1

			totalTimeBlack = totalTimeBlack + delta.total_seconds()
			totalMoveBlack = totalMoveBlack + 1

		node = moveChange[1]	

		#print("--------------------------------------------------------------------------------")
		if ka%5 == 0:
			print("move number :" + str(ka))

		#if ka%2 == 0 and ka != 0:
		#	print("Black move:")
		#elif ka%2 == 1:
		#	print("White move:")
			

		if node != None:	
		#	printBoard(node[0])

			for iaa in node[0]:
				for jaa in iaa:
					filetoWrite.write(str(jaa)+" ")
				filetoWrite.write('\n')	

			filetoWrite.write('\n')

		#else:
		#	print(node)

		#print(moveChange)

		#print(delta)

		#print("-------------------------------------------------------------------------------")


		if whoseMove == 1:
			whoseMove = 2
		else:
			whoseMove = 1
		
		ka = ka + 1

	filetoWrite.close()


	print("------------------------------------Final Results-------------------------------------------")
	print("A.")

	if WinnerWho == 1:
		print("White Player wins")
	else: 
		print("Black Player wins")

	printBoard(node[0])
	print("------------------------------------")

	print("B.")
	print("White Player")
	if Player1SearchType == "min":
		print("Number of nodes expanded: "+ str(miniMaxNodesWhite))
	elif Player1SearchType == "alphaB":
		print("Number of nodes expanded: "+ str(len(transpositionTabWhite)))
	print("Black Player")
	if Player2SearchType == "min":
		print("Number of nodes expanded: "+ str(miniMaxNodesBlack))
	elif Player2SearchType == "alphaB":
		print("Number of nodes expanded: "+ str(len(transpositionTabBlack)))

	print("------------------------------------")

	print("C.")

	TotalNodesExp = 0

	print("White Player")
	
	if Player1SearchType == "min":
	
		print("Average Number of nodes expanded per move: "+ str(float(miniMaxNodesWhite)/totalMoveWhite))
	
		TotalNodesExp = TotalNodesExp + miniMaxNodesWhite
	
	elif Player1SearchType == "alphaB":

		print("Average Number of nodes expanded per move: "+ str(float(len(transpositionTabWhite))/totalMoveWhite))
	
		TotalNodesExp = TotalNodesExp + len(transpositionTabWhite)

	print("Average amount of time to make a move: "+ str(float(totalTimeWhite)/totalMoveWhite))

	print("Black Player")
	
	if Player2SearchType == "min":
	
		print("Average Number of nodes expanded per move: "+ str(float(miniMaxNodesBlack)/totalMoveBlack))
	
		TotalNodesExp = TotalNodesExp + miniMaxNodesBlack
	
	elif Player2SearchType == "alphaB":
	
		print("Average Number of nodes expanded per move: "+ str(float(len(transpositionTabBlack))/totalMoveBlack))
	
		TotalNodesExp = TotalNodesExp + len(transpositionTabBlack)

	print("Average amount of time to make a move: "+ str(float(totalTimeBlack)/totalMoveBlack))


	print("Total: ")
	
	print("Average Number of nodes expanded per move: "+ str(float(TotalNodesExp)/(totalMoveBlack+totalMoveWhite)))
	
	print("Average amount of time to make a move: "+ str(float(totalTimeBlack+totalTimeWhite)/(totalMoveBlack+totalMoveWhite)))


	#The average number of nodes expanded per move and the average 
	#amount of time to make a move.
	
	print("------------------------------------")

	print("D.")
	#The number of opponent workers captured by each player, as well as the 
	#total number of moves required till the win.

	print("White captured " + str(16-node[2]) + " black pieces")
	print("Black captured " + str(16-node[1]) + " white pieces")
	print("Total Number of moves: "+ str(totalMoveBlack+totalMoveWhite))



	print("------------------------------------Final Results-End------------------------------------------")



if __name__ == "__main__":

	'''
	Player1 = "Off"
	Player2 = "Off"
	print("Match1: Off vs Off")
	main('input.txt', Player1, Player2, "min", "alphaB", 3, 4, "workfile1.txt")

	Player1 = "Off2"
	Player2 = "Def"
	print("Match2: Off2 vs Def")

	main('input.txt', Player1, Player2, "alphaB", "alphaB", 4, 4, "workfile2.txt")


	Player1 = "Def2"
	Player2 = "Off"
	print("Match3: Def2 vs Off")

	main('input.txt', Player1, Player2, "alphaB", "alphaB", 4, 4, "workfile3.txt")


	Player1 = "Off2"
	Player2 = "Off"
	print("Match4: Off2 vs Off")

	main('input.txt', Player1, Player2, "alphaB", "alphaB", 4, 4, "workfile4.txt")
	'''


	Player1 = "Def2"
	Player2 = "Def"
	print("Match5: Def2 vs Def")
	print("yeah")
	main('input.txt', Player1, Player2, "alphaB", "alphaB", 3, 3, "workfile5.txt")


	Player1 = "Off2"
	Player2 = "Def2"
	print("Match6: Off2 vs Def2")

	main('input.txt', Player1, Player2, "alphaB", "alphaB", 4, 4, "workfile6.txt")


#	Player3 = "Off2"
#	Player4 = "Def"

	#main('input.txt', Player3, Player4, "alphaB", "alphaB")
	