
paddle_height = 0.2
x_coord = 1
action = [0, 0.04, -0.04] # change in paddle y coordinate

def pong_game(state):
    cnt = 0
    while state[0] <= 1:

initial_state = (0.5, 0.5, 0.03, 0.01, 0.5-paddle_height/2)
