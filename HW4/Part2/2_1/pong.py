import random
import math
import time
import numpy as np

paddle_height = 0.2
paddle_x = 1.0
action = [0.0, 0.04, -0.04] # change in paddle y coordinate
grid_size = 12.0
num_iter = int(1e5) # number of iterations to train on, used for debugging
run = False
terminal = int(grid_size * grid_size * 2 * 3 * 12 + 1)

Q = np.zeros((terminal+5, 3)) # Q values
N = np.zeros((terminal+5, 3), dtype=np.int) # N values

C = 120.0 # part of learning rate
gamma = 0.999 # discount factor
upto = 3 # try this many times for each
maxr = 1.0 # reward for this


def encode(ball_x, ball_y, velocity_x, velocity_y, paddle_y):
    ball_state = ball_x * grid_size + ball_y
    velocity_state = velocity_x * 3 + velocity_y
    state = (ball_state*6 + velocity_state)*grid_size + paddle_y
    return int(state)


def get_discrete(ball_x, ball_y, velocity_x, velocity_y, paddle_y):
    if ball_x > paddle_x:
        return (-1, -1, -1, -1, -1)
    discreteb_x = min(math.floor(ball_x * grid_size), grid_size-1)
    discreteb_y = min(math.floor(vall_y * grid_size), grid_size-1)
    discretev_x = 0 if velocity_x < 0 else 1 # -1 and 1
    if math.fabs(velocity_y) < 0.015: # 0, -1, and 1
        discretev_y = 1
    elif velocity_y < 0:
        discretev_y = 0
    else:
        discretev_y = 2
    discrete_p = math.floor(grid_size * paddle_y / (1-paddle_height))
    if paddle_y == 1-paddle_height:
        discrete_p = grid_size-1
    return (discreteb_x, discreteb_y, discretev_x, discretev_y, discrete_p)


def move(ball_x, ball_y, velocity_x, velocity_y, paddle_y, act):
    ball_x += velocity_x
    ball_y += velocity_y
    paddle_y = min(max(0, paddle_y+action[act]), 1-paddle_height)
    bounce = 0
    if ball_y < 0:
        ball_y *= -1
        velocity_y *= -1
    if ball_y > 1:
        ball_y = 2-ball_y
        velocity_y *= -1
    if ball_x < 0:
        ball_x *= -1
        velocity_x *= -1
    if ball_x > paddle_x and ball_y >= paddle_y and ball_y <= paddle_y+paddle_height:
        ball_x = 2.0*paddle_x - ball_x
        velocity_x = -velocity_x + float(random.randrange(-15, 15))/1000.0
        velocity_y += float(random.randrange(-3, 3))/100.0
        bounce = 1
        if math.fabs(velocity_x) < 0.03:
            velocity_x *= 0.03 / math.fabs(velocity_x)
        if math.fabs(velocity_x) > 1:
            velocity_x = -1 if velocity_x < 0 else 1
        if math.fabs(velocity_y) > 1:
            velocity_y = -1 if velocity_y < 0 else 1
    return ball_x, ball_y, velocity_x, velocity_y, paddle_y, bounce


def pong_game(state, discrete):
    cnt = 0
    arr = np.zeros(3, dtype = np.int)
    discrete_state = get_discrete(state)
    biject = encode(*discrete_state)
    while state[0] <= paddle_x:
        '''
        print("state:", state)
        print("discrete_state:", discrete_state)
        print("biject:", biject)
        '''
        # get next action
        if discrete == 1:
            # train model
            for i in range(3):
                if N[biject][i] < upto:
                    arr[i] = maxr
                else:
                    arr[i] = Q[biject][i]
            nxt_act = np.random.choice(np.flatnonzero(arr == np.amax(arr)))
        else:
            # test, get max action
            nxt_act = np.argmax(Q[biject])
        # get next state
        (state, bounce) = move(state, nxt_act)
        discrete_state = get_discrete(state)
        new_bij = encode(*discrete_state)
        if discrete == 1:
            # update number times visited and Q value
            N[biject][nxt_act] += 1
            Q[biject][nxt_act] += C/(C+float(N[biject][nxt_act])) * (float(bounce) + gamma * np.amax(Q[new_bij]) - Q[biject][nxt_act]);
        biject = new_bij
        cnt += bounce
    return cnt


start_time = time.time()
# ball_x, ball_y, velocity_x, velocity_y, paddle_y
initial_state = (0.5, 0.5, 0.03, 0.01, 0.5-paddle_height/2)

# q train on discrete case
for i in range(3):
    Q[terminal][i] = -1
train_bounces = []
for i in range(num_iter):
    val = pong_game(initial_state, 1)
    # print("Game number "+ str(i) + ": " + str(val))
    train_bounces.append(val)
train_bounces = np.array(train_bounces)
np.set_printoptions(threshold = np.inf)
print(train_bounces)
print("max bounces: " + str(np.amax(train_bounces)))
print("training avg: " + str(float(np.sum(train_bounces)) / num_iter))

# check error on continuous case
num = 0
total = 0.0
bounces = []
while run and (num == 0 or total/num < 10.0):
    val = pong_game(initial_state, 0)
    bounces.append(val)
    num += 1
    total += val

print("num: ", num)
if num != 0:
    print("average: ", total/num)

print("total time: " + str(time.time() - start_time) + " seconds")
