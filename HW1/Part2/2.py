from array import array
from collections import deque
import Queue as queue
import time
from heapq import heappush
from heapq import heappop
from heapq import heapify

#from munkres import Munkres, print_matrix



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

	
	saveStr = bfsSolver(finalState, currState, numberOfColumns, px, py, board)

	print("bfsSolver: ")
	print("Start Point: (" + str(py) + "," + str(px) + ")") 
	print(len(saveStr))
	print(saveStr)
	
	
	saveStr = AStarSolver(finalState, currState, numberOfColumns, px, py, board)

	print("AStarSolver: ")
	print("Start Point: (" + str(py) + "," + str(px) + ")") 
	print(len(saveStr))
	print(saveStr)
	


def goalStateReached(finalState, currState):
	for i in range(0,len(finalState)):
		if (finalState[i] == 'F') and (currState[i] != 'F'):
			return False
	return True


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


def bfsSolver(finalState, currState, numberOfColumns , px, py, board):
	my_queue = deque([(currState, [], px, py)])
	#open = deque([(currState, "", px, py)])
	visited = set([currState])
	directionsToMove = ((0, -1), ( 1, 0), (0,  1), (-1, 0))

	while my_queue:
		cur, csol, x, y = my_queue.popleft()

		for dxy in directionsToMove:
			frontState = cur
			dx, dy = dxy[0], dxy[1]
			
			if board[(y+dy) * numberOfColumns + x+dx] != '%':
				checker, newState = checkToAdd(board, frontState, numberOfColumns, x, y, dx, dy, visited, finalState)	
				if checker == 1:
					newsol = list(csol)
					newsol.append((y+dy,x+dx))
					return newsol
				elif checker == 2:
					newsol = list(csol)
					newsol.append((y+dy,x+dx))
					my_queue.append((newState, newsol, x+dx, y+dy))
					visited.add(newState)

	notFound = "Solution not Found"				
	return notFound



def findOccurences(s, ch):
	return [i for i, letter in enumerate(s) if letter == ch]


def checkToAddToAStar(board, frontState, numberOfColumns, x, y, dx, dy, finalState):

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
		frontState[(y+2*dy) * numberOfColumns + x+2*dx] == 'F':
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

def remove_task(priority_queue, entry_finder, task):
	'Mark an existing task as REMOVED.  Raise KeyError if not found.'
	entry = entry_finder[task]
	del entry_finder[task]
	priority_queue.remove(entry)
	heapify(priority_queue)
	return priority_queue,entry_finder

def pop_task(priority_queue, entry_finder):
	'Remove and return the lowest priority task. Raise KeyError if empty.'
	
	priority, count, task, px, py, csol,disTravelled = heappop(priority_queue)
	del entry_finder[task]
	return priority, task, px, py, csol, priority_queue, entry_finder, disTravelled

	raise KeyError('pop from an empty priority queue')


def AStarSolver(finalState, currState, numberOfColumns , px, py, board):

	priority_queue = []
	entry_finder = {}

	cSolution = []
	
	priority_queue, entry_finder = add_task(priority_queue, entry_finder, currState, 0, px, py, cSolution,0)

	directionsToMove = ((0, -1), ( 1, 0), (0,  1), (-1, 0))
	
	val = 0
	while 1:
		if len(priority_queue) == 0:
			break
		dis, cur, x, y, csol, priority_queue, entry_finder, disTravelled = pop_task(priority_queue, entry_finder)
		#print(dis)
		if val != dis:
			val = dis
			print(val)
			print(len(priority_queue))

		for dxy in directionsToMove:
			frontState = cur
			dx, dy = dxy[0], dxy[1]
			
			#print()

			if board[(y+dy) * numberOfColumns + x+dx] != '%':
				checker, newState, disSol = checkToAddToAStar(board, frontState, numberOfColumns, x, y, dx, dy, finalState)	
				
				if checker == 1:
					newsol = list(csol)
					newsol.append((y+dy,x+dx))
					return newsol
				elif checker == 2:
					newsol = list(csol)
					newsol.append((y+dy,x+dx))
					priority_queue, entry_finder = add_task(priority_queue, entry_finder, newState, disTravelled+disSol, x+dx, y+dy, newsol, disTravelled+1)
					

	notFound = "Solution not Found"				
	return notFound


if __name__ == "__main__":
	
	main('sokoban1.txt')
	main('sokoban2.txt')
	main('sokoban3.txt')
	main('sokoban4.txt')