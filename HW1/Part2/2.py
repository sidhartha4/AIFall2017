from array import array
from collections import deque
 

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
	open = deque([(currState, [], px, py)])
	#open = deque([(currState, "", px, py)])
	visited = set([currState])
	directionsToMove = ((0, -1), ( 1, 0),
	        (0,  1), (-1, 0))

	while open:
		cur, csol, x, y = open.popleft()

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
					open.append((newState, newsol, x+dx, y+dy))
					visited.add(newState)

	notFound = "Solution not Found"				
	return notFound

	
if __name__ == "__main__":
	
	main('sokoban1.txt')
	main('sokoban2.txt')
	main('sokoban3.txt')
	main('sokoban4.txt')
	