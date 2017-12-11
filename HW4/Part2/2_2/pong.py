import random
import math
import time
import numpy as np

paddle_height = 0.2
paddle_x = 1.0
action = [0.0, 0.04, -0.04] # change in paddle y coordinate
oppact = [0,0, 0.02, -0.02] # change in paddle y coordinate for opponent
grid_size = 12.0
num_iter = int(1e5) # number of iterations to train on, used for debugging
test_iter = int(1e3) # number iterations to test on
terminal = int(math.pow(grid_size, 4)*2*3 + 1)

Q = np.zeros((terminal+5, 3)) # Q values
N = np.zeros((terminal+5, 3), dtype=np.int) # N values

C = 120.0 # part of learning rate
gamma = 0.75 # discount factor
upto = 5 # try this many times for each
maxr = 1e9 # reward for this


def encode(ball_x, ball_y, velocity_x, velocity_y, paddle_y, opp_y):
    if ball_x > paddle_x:
        return terminal
    discreteb_x = min(math.floor(ball_x * grid_size), grid_size-1)
    discreteb_y = min(math.floor(ball_y * grid_size), grid_size-1)
    discretev_x = 0 if velocity_x < 0 else 1 # -1 and 1
    if math.fabs(velocity_y) < 0.015: # 0, -1, and 1
        discretev_y = 1
    elif velocity_y < 0:
        discretev_y = 0
    else:
        discretev_y = 2
    discrete_p = min(math.floor(grid_size * paddle_y / (1-paddle_height)), grid_size-1)
    discrete_opp = min(math.floor(grid_size * opp_y / (1-paddle_height)), grid_size-1)
    discreteb_x, discreteb_y, discretev_x, discretev_y, discrete_p
    ball_state = discreteb_x * grid_size + discreteb_y
    velocity_state = discretev_x * 3 + discretev_y
    state = ((ball_state*6 + velocity_state)*grid_size + discrete_p)*grid_size + discrete_opp
    return int(state)


def move(ball_x, ball_y, velocity_x, velocity_y, paddle_y, opp_y, act):
    ball_x += velocity_x
    ball_y += velocity_y
    paddle_y = min(max(0, paddle_y+action[act]), 1-paddle_height)
    opp = 2
    for i in xrange(2):
        if math.fabs(opp_y + oppact[i] + paddle_height/2 - ball_y) <= math.fabs(opp_y + oppact[(i+1)%3] + paddle_height/2 - ball_y) and math.fabs(opp_y + oppact[i] + paddle_height/2 - ball_y) <= math.fabs(opp_y + oppact[(i+2)%3] + paddle_height/2 - ball_y): 
            opp = i
    opp_y += oppact[opp]
    bounce = 0
    if ball_y < 0:
        ball_y = -ball_y
        velocity_y = -velocity_y
    if ball_y > 1:
        ball_y = 2.0-ball_y
        velocity_y = -velocity_y
    if ball_x < 0:
        if ball_y >= opp_y and ball_y <= opp_y+paddle_height:
            ball_x = -ball_x
            velocity_x = -velocity_x
        else:
            bounce = 1
    if ball_x > paddle_x:
        if ball_y >= paddle_y and ball_y <= paddle_y+paddle_height:
            ball_x = 2.0 - ball_x
            velocity_x = -velocity_x + float(random.randrange(-15, 15))/1000.0
            velocity_y += float(random.randrange(-3, 3))/100.0
            if math.fabs(velocity_x) < 0.03:
                velocity_x = -0.03 if velocity_x < 0 else 0.03
            if math.fabs(velocity_x) > 1:
                velocity_x = -1 if velocity_x < 0 else 1
            if math.fabs(velocity_y) > 1:
                velocity_y = -1 if velocity_y < 0 else 1
        else:
            bounce = -1
    return ball_x, ball_y, velocity_x, velocity_y, paddle_y, opp_y, bounce


def pong_game(ball_x, ball_y, velocity_x, velocity_y, paddle_y, opp_y, discrete):
    arr = np.zeros(3, dtype = np.int)
    biject = encode(ball_x, ball_y, velocity_x, velocity_y, paddle_y, opp_y)
    bounce = 0
    while bounce == 0:
        # print biject, ball_x, ball_y, velocity_x, velocity_y, paddle_y
        # get next action
        if discrete == 1:
            # compute exploration function value
            for i in xrange(3):
                if N[biject][i] < upto:
                    arr[i] = maxr
                else:
                    arr[i] = Q[biject][i]
            nxt_act = np.random.choice(np.flatnonzero(arr == arr.max()))
            #nxt_act = np.argmax(arr)
        else:
            # test, get max action
            nxt_act = np.argmax(Q[biject])
        # get next state
        ball_x, ball_y, velocity_x, velocity_y, paddle_y, opp_y, bounce = move(ball_x, ball_y, velocity_x, velocity_y, paddle_y, opp_y, nxt_act)
        new_bij = encode(ball_x, ball_y, velocity_x, velocity_y, paddle_y, opp_y)
        if discrete == 1:
            # update number times visited and Q value
            N[biject][nxt_act] += 1
            Q[biject][nxt_act] += C/(C+N[biject][nxt_act]) * (bounce + gamma * Q[new_bij].max() - Q[biject][nxt_act]);
        biject = new_bij
    return max(0, bounce) # 1 = win, -1 = 0 = lose


start_time = time.time()
# q train on discrete case
for i in xrange(3):
    Q[terminal][i] = -1
init_paddle = 0.5-paddle_height/2
train_wins = []
for i in xrange(num_iter):
    val = pong_game(0.5, 0.5, 0.03, 0.01, init_paddle, init_paddle, 1)
    # print("Game number "+ str(i) + ": " + str(val))
    train_wins.append(val)
train_wins = np.array(train_wins)
np.set_printoptions(threshold = np.inf)
print(train_wins)
print("training avg win: " + str(float(np.sum(train_wins)) / num_iter))

# check error on continuous case
total = 0.0
wins = []
for i in xrange(test_iter):
    val = pong_game(0.5, 0.5, 0.03, 0.01, init_paddle, init_paddle, 0)
    wins.append(val)

wins = np.array(wins)
print(wins)
print("num: ", test_iter)
print("average: ", float(np.sum(wins))/test_iter)
print("total time: " + str(time.time() - start_time) + " seconds")
