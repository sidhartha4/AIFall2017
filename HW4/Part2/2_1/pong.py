import random
import math
import numpy as np

paddle_height = 0.2
paddle_x = 1
action = [0, 0.04, -0.04] # change in paddle y coordinate
grid_size = 12

Q = np.zeros((11111, 2)) # Q values

alpha = 0 # learning rate
gamma = 0 # discount factor
r = 0 # reward
C = 0

def encode(ball_x, ball_y, velocity_x, velocity_y, paddle_height):
    ball_state = ball_x * grid_size + ball_y
    velocity_state = velocity_x * 3 + velocity_y
    state = (ball_state*6 + velocity_state)*12 + paddle_height
    return state

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

def move(state, act, discrete):
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
    if ball_x > 1 and ball_y >= paddle_y and ball_y <= paddle_y+paddle_height:
        ball_x = 2*paddle_x - ball_x
        velocity_x = -velocity_x + random.randrange(-0.015, 0.015)
        velocity_y += random.randrange(-0.03, 0.03)
        bounce = 1
        if math.fabs(velocity_x) < 0.03:
            velocity_x *= 0.03 / math.fabs(velocity_x)
        if math.fabs(velocity_x) > 1:
            velocity_x /= math.fabs(velocity_x)
        if math.fabs(velocity_y) > 1:
            velocity_y /= math.fabs(velocity_y)
    return ((ball_x, ball_y, velocity_x, velocity_y, paddle_y), bounce)


def pong_game(state, discrete):
    cnt = 0
    while state[0] <= 1:
        if discrete == 1:
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
        (state, bounce) = move(state, act, discrete)
        cnt += bounce
    return cnt

# ballx, bally, velocityx, velocityy, paddley
initial_state = (0.5, 0.5, 0.03, 0.01, 0.5-paddle_height/2)

# q train on discrete case
for i in range(1e5):
    pong_game(initial_state, 1)

# check error on continuous case
num = 0
total = 0.0
bounces = []
while num == 0 or total/num < 10.0:
    val = pong_game(initial_state, 0)
    bounces.append(val)
    num += 1
    total += val

print("num: ", num)
print("average: ", total/num)
