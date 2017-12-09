import random
import math

paddle_height = 0.2
paddle_x = 1
action = [0, 0.04, -0.04] # change in paddle y coordinate

def move(state, act):
    velocity_x = state[2]
    velocity_y = state[3]
    ball_x = state[0] + velocity_x
    ball_y = state[1] + velocity_y
    paddley_y = min(max(0, state[4]+action[act]), 1-paddle_height)
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
        if math.fabs(velocity_x) < 0.03:
            velocity_x *= 0.03 / math.fabs(velocity_x)
        if math.fabs(velocity_x) > 1:
            velocity_x /= math.fabs(velocity_x)
        if math.fabs(velocity_y) > 1:
            velocity_y /= math.fabs(velocity_y)


def pong_game(state):
    cnt = 0
    while state[0] <= 1:

# ballx, bally, velocityx, velocityy, paddley
initial_state = (0.5, 0.5, 0.03, 0.01, 0.5-paddle_height/2)
