import random
import math
import numpy as np

paddle_height = 0.2
paddle_x = 1
action = [0, 0.04, -0.04] # change in paddle y coordinate
grid_size = 12.0
num_iter = int(1e1) # number of iterations to train on, used for debugging
run = False

Q = np.zeros((11111, 3)) # Q values
N = np.zeros((11111, 3), dtype=np.int) # N values

terminal = 11110
C = 100.0 # part of learning rate
gamma = 1.0 # discount factor
upto = 2 # try this many times for each
maxr = 2 # reward for this


def encode(ball_x, ball_y, velocity_x, velocity_y, paddle_height):
    ball_state = ball_x * grid_size + ball_y
    velocity_state = velocity_x * 3 + velocity_y
    state = (ball_state*6 + velocity_state)*12 + paddle_height
    return int(state)


def decode(state):
    paddle_height = state % 12
    state /= 12
    velocity_state = state % 6
    velocity_y = velocity_state % 3
    velocity_x = velocity_state / 3
    state /= 6
    ball_y = state % grid_size
    ball_x = state / 12
    return (ball_x, ball_y, velocity_x, velocity_y, paddle_height)


def get_discrete(state):
    if state[0] > paddle_x:
        return (-1, -1, -1, -1, -1)
    discreteb_x = math.floor(state[0] * grid_size)
    discreteb_y = math.floor(state[1] * grid_size)
    discretev_x = 0 if state[2] < 0 else 1 # -1 and 1
    if math.fabs(state[3]) < 0.015: # 0, -1, and 1
        discretev_y = 1
    elif state[3] < 0:
        discretev_y = 0
    else:
        discretev_y = 2
    discrete_p = math.floor(12 * state[4] / (1-paddle_height))
    if state[4] == 1-paddle_height:
        discrete_p = 11
    return (discreteb_x, discreteb_y, discretev_x, discretev_y, discrete_p)


def move(state, act):
    velocity_x = state[2]
    velocity_y = state[3]
    ball_x = state[0] + velocity_x
    ball_y = state[1] + velocity_y
    paddle_y = min(max(0, state[4]+action[act]), 1-paddle_height)
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
        ball_x = 2*paddle_x - ball_x
        velocity_x = -velocity_x + random.randrange(-15, 15)/1000.0
        velocity_y += random.randrange(-3, 3)/100.0
        bounce = 1
        if math.fabs(velocity_x) < 0.03:
            velocity_x *= 0.03 / math.fabs(velocity_x)
        if math.fabs(velocity_x) > 1:
            velocity_x /= math.fabs(velocity_x)
        if math.fabs(velocity_y) > 1:
            velocity_y /= math.fabs(velocity_y)
    return ((ball_x, ball_y, velocity_x, velocity_y, paddle_y), bounce)


def f(value, times):
    if times < upto:
        return maxr
    else:
        return value


def get_action(state, discrete, reward):
    if state[0] == -1:
        return -1
    biject = encode(*state)
    if discrete == 1:
        # train model
        arr = np.zeros(3, dtype=np.int)
        arr_bij = np.zeros(3, dtype=np.int)
        for i in range(3):
            (nxt, garb) = move(state, i)
            arr_bij[i] = encode(*nxt)
            arr[i] = Q[arr_bij[i]][i]
        mx = np.amax(arr)
        for i in range(3):
            arr[i] = f(arr[i], N[arr_bij[i]][i])
        action = np.argmax(arr)
        N[biject][action] += 1
        Q[biject][action] += C/(C+float(N[biject][action])) * (float(reward) + gamma * mx - Q[biject][action]);
        return action
    else:
        # test, get max action
        return np.argmax(Q[biject])


def pong_game(state, discrete):
    cnt = 0
    reward = 0
    pre_act = -1
    while True:
        print(state)
        discrete_state = get_discrete(state)
        print(discrete_state)
        nxt_act = get_action(discrete_state, discrete, reward)
        if nxt_act == -1:
            break
        (state, bounce) = move(state, nxt_act)
        pre_act = nxt_act
        cnt += bounce
        reward = bounce
    Q[encode(*state)][pre_act] = -1
    return cnt


# ball_x, ball_y, velocity_x, velocity_y, paddle_y
initial_state = (0.5, 0.5, 0.03, 0.01, 0.5-paddle_height/2)

# q train on discrete case
train_bounces = []
for i in range(num_iter):
    val = pong_game(initial_state, 1)
    train_bounces.append(val)
train_bounces = np.array(train_bounces)
print(train_bounces)
print(np.amax(train_bounces))

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
