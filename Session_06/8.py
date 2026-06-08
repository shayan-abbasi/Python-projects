import turtle
import random

screen = turtle.Screen()
t = turtle.Turtle()
t.speed(0)
t.hideturtle()
t.penup()


vertices = [
    (0, 200, "blue"),    
    (-200, -200, "red"),  
    (200, -200, "green") 
]


for x, y, color in vertices:
    t.goto(x, y)
    t.dot(10, color)


current_x, current_y = -200, -200


for _ in range(5000):
  
    target_x, target_y, target_color = random.choice(vertices)
    
  
    current_x = (current_x + target_x) / 2
    current_y = (current_y + target_y) / 2
    
    
    t.goto(current_x, current_y)
    t.dot(2, target_color)

    
    if _ % 50 == 0:
        screen.update()

turtle.done()