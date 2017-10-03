from array import array
from collections import deque
import Queue as queue
import time
from heapq import heappush
from heapq import heappop
from heapq import heapify

from datetime import datetime


# we use priority queue from python library

def main(name):

	numberOfColumns = 0
	px = py = 0
	finalState = ""
	currState = ""
	board = ""

	with open(name) as f:
		content = f.readlines()
	
	i = 0
	for row in content:
		row = row.strip()
		numberOfColumns = len(row)
		j = 0
		for val in row:
			if val == 'P':
				finalState += ' '
				currState += 'A'
				board += ' '
				px = j
				py = i

			elif val == '.':
				finalState += 'F'
				currState += ' '
				board += ' '


			elif val == 'B':

				finalState += 'F'
				currState += 'F'
				board += ' '

			elif val == 'b':
			
				finalState += ' '
				currState += 'F'
				board += ' '
			
			elif val == '%':
			
				finalState += ' '
				currState += ' '
				board += '%'
			
			else:

				finalState += ' '
				currState += ' '
				board += ' '
			j = j + 1
		i = i + 1



	deadlockArr = calculateDeadlock(board,finalState, numberOfColumns)


	t1 = datetime.now()
	
	saveStr, pushed, popped = bfsSolver(finalState, currState, numberOfColumns, px, py, board)



	print("-------------------------Solving " + name + "------------------------------")

	print("bfsSolver: ")
	print("Start Point: (" + str(py) + "," + str(px) + ")") 
	print("Length of travel: " + str(len(saveStr)))
	print("Path taken:")
	print(saveStr)

	print("Nodes expanded:" + str(popped))
	

	t2 = datetime.now()
	delta = t2 - t1
	print("running time: " +  str(delta.total_seconds()))
	t1 = t2

	print("-----------------------------------------------------------------")

	saveStr, pushed, popped = AStarSolver(finalState, currState, numberOfColumns, px, py, board, deadlockArr)

	print("AStarSolver: ")
	print("Start Point: (" + str(py) + "," + str(px) + ")") 
	print("Length of travel: " + str(len(saveStr)))
	print("Path taken:")
	print(saveStr)

	print("Nodes expanded:" + str(popped))

	t2 = datetime.now()
	delta = t2 - t1
	print("Running time: " +  str(delta.total_seconds()))

	print("-----------------------------------------------------------------")

# This function checks from which of the location can the boxes be pushed to a specific goal located at xa, ya

def checkPlacesReachable(listofzeros, board, xa, ya, numberOfColumns):

	directionsToMove = ((0, -1), ( 1, 0), (0,  1), (-1, 0))
	
	my_queue = deque([(xa,ya)])
	listofzeros[ya*numberOfColumns + xa] = 1
	visited = set([(xa,ya)])

	#print(str(xa) + " " + str(ya)) 
	while my_queue:
		x, y = my_queue.popleft()
		#print(str(x) + " " + str(y))
		for dxy in directionsToMove:
			dx, dy = dxy[0], dxy[1]
			
			if board[(y+dy) * numberOfColumns + x+dx] != '%':
				if board[(y+2*dy) * numberOfColumns + x+2*dx] != '%':
					
					pair = (x+dx,y+dy)
					if pair not in visited:

						listofzeros[(y+dy) * numberOfColumns + x+dx] = 1
						#print(str(x+dx) + " " + str(y+dy))
						visited.add(pair)
						my_queue.append(pair)	



	return listofzeros


# This is a top level function which checks from which of the location can the boxes be pushed 
# to any of the goals and returns 1 for every index from where box can be pushed to a goal and zero if not


def calculateDeadlock(board,finalState, numberOfColumns):
	listofzeros = [0] * len(finalState)
	
	listOfIndices = findOccurences(finalState, "F")
	
	for ja in listOfIndices:
		ya = ja/numberOfColumns
		xa = ja%numberOfColumns
		listofzeros = checkPlacesReachable(listofzeros, board, xa, ya, numberOfColumns)

	return listofzeros



# This is a function which checks if the state has reached the final state 


def goalStateReached(finalState, currState):
	for i in range(0,len(finalState)):
		if (finalState[i] == 'F') and (currState[i] != 'F'):
			return False
	return True

# This is a function which checks if the state to be added is correct or not 

def checkToAdd(board, frontState, numberOfColumns, x, y, dx, dy, visited, finalState):

	checker = 0
	if frontState[(y+dy) * numberOfColumns + x+dx] == " ":

		newState = array("c", frontState)
		newState[y * numberOfColumns + x] = ' '
		newState[(y+dy) * numberOfColumns + x+dx] = 'A'
		newState = newState.tostring()
		if newState not in visited:
			checker = 2

		return checker, newState
	else:				
		if board[(y+2*dy) * numberOfColumns + x+2*dx] == '%' or \
		frontState[(y+2*dy) * numberOfColumns + x+2*dx] == 'F':
			return checker, frontState


		newState = array("c", frontState)
		newState[y * numberOfColumns + x] = ' '
		newState[(y+dy) * numberOfColumns + x+dx] = 'A'
		newState[(y+2*dy) * numberOfColumns + x+2*dx] = 'F'
		
		newState = newState.tostring()

		if newState not in visited:
			if goalStateReached(finalState, newState):
				checker = 1
				return checker, newState

			checker = 2

		return checker, newState



# This is a top level function for bfs.

def bfsSolver(finalState, currState, numberOfColumns , px, py, board):
	my_queue = deque([(currState, [], px, py)])
	pushed = 0
	popped = 0
	#open = deque([(currState, "", px, py)])
	visited = set([currState])
	directionsToMove = ((0, -1), ( 1, 0), (0,  1), (-1, 0))
	pushed = pushed + 1
	while my_queue:
		cur, csol, x, y = my_queue.popleft()
		popped = popped + 1

		for dxy in directionsToMove:
			frontState = cur
			dx, dy = dxy[0], dxy[1]
			
			if board[(y+dy) * numberOfColumns + x+dx] != '%':
				checker, newState = checkToAdd(board, frontState, numberOfColumns, x, y, dx, dy, visited, finalState)	
				if checker == 1:
					newsol = list(csol)
					newsol.append((y+dy,x+dx))
					return newsol, pushed, popped
				elif checker == 2:
					newsol = list(csol)
					newsol.append((y+dy,x+dx))
					my_queue.append((newState, newsol, x+dx, y+dy))
					visited.add(newState)
					pushed = pushed + 1

	notFound = "Solution not Found"				
	return notFound, pushed, popped


# This is a function to find all occurences of a substring in a string

def findOccurences(s, ch):
	return [i for i, letter in enumerate(s) if letter == ch]


# This is a to check if the state to be added to the priority queue is correct or not

def checkToAddToAStar(board, frontState, numberOfColumns, x, y, dx, dy, finalState, deadlockArr):

	checker = 0
	dis = 1

	newState = array("c", frontState)

	if frontState[(y+dy) * numberOfColumns + x+dx] == " ":

		newState[y * numberOfColumns + x] = ' '
		newState[(y+dy) * numberOfColumns + x+dx] = 'A'
		newState = newState.tostring()
		checker = 2


	else:				
		if board[(y+2*dy) * numberOfColumns + x+2*dx] == '%' or \
		frontState[(y+2*dy) * numberOfColumns + x+2*dx] == 'F' or \
		deadlockArr[(y+2*dy) * numberOfColumns + x+2*dx] == 0:
			return checker, frontState, dis

		newState[y * numberOfColumns + x] = ' '
		newState[(y+dy) * numberOfColumns + x+dx] = 'A'
		newState[(y+2*dy) * numberOfColumns + x+2*dx] = 'F'
		
		newState = newState.tostring()

		if goalStateReached(finalState, newState):
			checker = 1
			return checker, newState, dis

		checker = 2

	listOfIndices = findOccurences(finalState, "F")
	listOfIndices2 = findOccurences(newState, "F")

	tot = 0
	#tot = 1000000
	#hungarianDistCal = []
	#dis = 10000000
	for ja in listOfIndices2:
		ya = ja/numberOfColumns
		xa = ja%numberOfColumns
		dis = 100000000
		#rowInHun = []
		for ka in listOfIndices:
			kya = ka/numberOfColumns
			kxa = ka%numberOfColumns
			
			#rowInHun.append(abs(kya - ya) + abs(kxa - xa)) 
			dis = min(dis, abs(kya - ya) + abs(kxa - xa))
			#dis = min(dis,abs(y+dy - ya) + abs(x+dx - xa) + abs(kya - ya) + abs(kxa - xa))
		#hungarianDistCal.append(rowInHun)
		tot = tot + dis
		#tot = min(tot, dis)
	#print(hungarianDistCal)
	'''
	m = Munkres()
	indexes = m.compute(hungarianDistCal)

	for row, column in indexes:
		value = hungarianDistCal[row][column]
		tot += value
	'''				


	return checker, newState, tot


# add to priority queue function

def add_task(priority_queue, entry_finder, task, priority, px, py, csol, disTravelled):
	'Add a new task or update the priority of an existing task'
	if task in entry_finder:
		#print("init priority")
		#print(entry_finder[task][0])
		#print("priority")
		#print(priority)
		if priority >= entry_finder[task][0]:
			#print("I am not adding")
			return priority_queue, entry_finder

		#print("init priority")
		#print(entry_finder[task][0])
		#print("priority")
		#print(priority)
		#print("I am adding")
		priority_queue, entry_finder = remove_task(priority_queue, entry_finder, task)

	#print("priority")
	#print(priority)
	#print("I am adding")

	count = time.time()
	entry = [priority, count, task, px, py, csol, disTravelled]
	entry_finder[task] = entry
	heappush(priority_queue, entry)

	return priority_queue, entry_finder


# Remove from priority queue function supporter

def remove_task(priority_queue, entry_finder, task):
	'Mark an existing task as REMOVED.  Raise KeyError if not found.'
	entry = entry_finder[task]
	del entry_finder[task]
	priority_queue.remove(entry)
	heapify(priority_queue)
	return priority_queue,entry_finder

# Remove from priority queue function

def pop_task(priority_queue, entry_finder):
	'Remove and return the lowest priority task. Raise KeyError if empty.'
	
	priority, count, task, px, py, csol,disTravelled = heappop(priority_queue)
	del entry_finder[task]
	return priority, task, px, py, csol, priority_queue, entry_finder, disTravelled

	raise KeyError('pop from an empty priority queue')


# Top level function for A*


def AStarSolver(finalState, currState, numberOfColumns , px, py, board, deadlockArr):

	priority_queue = []
	entry_finder = {}

	cSolution = []
	
	priority_queue, entry_finder = add_task(priority_queue, entry_finder, currState, 0, px, py, cSolution,0)

	directionsToMove = ((0, -1), ( 1, 0), (0,  1), (-1, 0))
	
	pushed = 0
	popped = 0

	pushed = pushed + 1

	val = 0
	while 1:
		if len(priority_queue) == 0:
			break
		dis, cur, x, y, csol, priority_queue, entry_finder, disTravelled = pop_task(priority_queue, entry_finder)
		popped = popped + 1

		#print(dis)
		if val != dis:
			val = dis
			#print(val)
			#print(len(priority_queue))

		for dxy in directionsToMove:
			frontState = cur
			dx, dy = dxy[0], dxy[1]
			
			#print()

			if board[(y+dy) * numberOfColumns + x+dx] != '%':

				checker, newState, disSol = checkToAddToAStar(board, frontState, numberOfColumns, x, y, dx, dy, finalState, deadlockArr)	
				
				if checker == 1:
					newsol = list(csol)
					newsol.append((y+dy,x+dx))
					return newsol, pushed, popped

				elif checker == 2:
					newsol = list(csol)
					newsol.append((y+dy,x+dx))
					priority_queue, entry_finder = add_task(priority_queue, entry_finder, newState, disTravelled+disSol, x+dx, y+dy, newsol, disTravelled+1)
					pushed = pushed + 1

	notFound = "Solution not Found"				
	return notFound, pushed, popped


if __name__ == "__main__":
	
	main('sokoban1.txt')
	main('sokoban2.txt')
	main('sokoban3.txt')
	main('sokoban4.txt')
	#main('extra1.txt')
	