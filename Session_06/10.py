import turtle
import random

t = turtle.Turtle()
t.speed(0)
t.penup()
t.color("brown")

x = 0.0
y = 0.0

for i in range(5000):
    px = x.__mul__(100)
    py = y.__mul__(100).__sub__(150)
    
    t.goto(px, py)
    t.dot(2)
    
    r = random.random()
    
    if r < 0.1:
        nx = x.__mul__(0.05)
        ny = y.__mul__(0.6)
    elif r < 0.2:
        nx = x.__mul__(0.05)
        ny = y.__mul__(-0.5).__add__(1.0)
    elif r < 0.6:
        nx = x.__mul__(0.46).__sub__(y.__mul__(0.32))
        ny = x.__mul__(0.39).__add__(y.__mul__(0.38)).__add__(0.6)
    else:
        nx = x.__mul__(0.47).__sub__(y.__mul__(0.15))
        ny = x.__mul__(0.17).__add__(y.__mul__(0.42)).__add__(1.1)
        
    x = nx
    y = ny

turtle.done()