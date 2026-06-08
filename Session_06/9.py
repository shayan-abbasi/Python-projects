import turtle
import random

t = turtle.Turtle()
t.speed(0)
t.color("green")
t.penup()

x = 0.0
y = 0.0

for _ in range(3000):
    
    t.goto(x * 30, y * 30 - 150) 
    t.dot(2)
    
    r = random.random()
    
    if r < 0.01:
        nx = 0
        ny = 0.16 * y
    elif r < 0.86:
        nx = 0.85 * x + 0.04 * y
        ny = -0.04 * x + 0.85 * y + 1.6
    elif r < 0.93:
        nx = 0.2 * x - 0.26 * y
        ny = 0.23 * x + 0.22 * y + 1.6
    else:
        nx = -0.15 * x + 0.28 * y
        ny = 0.26 * x + 0.24 * y + 0.44
    
    x = nx
    y = ny

turtle.done()