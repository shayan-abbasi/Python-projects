import tkinter as tk
from tkinter import ttk
import random

WIDTH = 700
HEIGHT = 700

class Car:
    def __init__(self, direction):
        self.direction = direction
        self.speed = 3

        if direction == "N":
            self.x = 335
            self.y = -20
        elif direction == "S":
            self.x = 365
            self.y = HEIGHT + 20
        elif direction == "E":
            self.x = WIDTH + 20
            self.y = 335
        else:
            self.x = -20
            self.y = 365


class TrafficApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Traffic Light")

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
        self.canvas.pack()

        frame = tk.Frame(root)
        frame.pack()

        self.green = tk.IntVar(value=6)
        self.yellow = tk.IntVar(value=2)

        ttk.Label(frame, text="Green").pack(side="left")
        ttk.Entry(frame, textvariable=self.green, width=5).pack(side="left")

        ttk.Label(frame, text="Yellow").pack(side="left")
        ttk.Entry(frame, textvariable=self.yellow, width=5).pack(side="left")

        self.cars = {"N": [], "S": [], "E": [], "W": []}

        self.light = "N"
        self.mode = "GREEN"
        self.timer = self.green.get()

        self.update()

    def new_car(self):
        d = random.choice(["N", "S", "E", "W"])
        self.cars[d].append(Car(d))

    def move_cars(self):
        stop = {"N":290,"S":410,"E":410,"W":290}

        for d in self.cars:

            remove = []

            for car in self.cars[d]:

                go = (d == self.light and self.mode == "GREEN")

                if d == "N":
                    if go or car.y < stop[d]:
                        car.y += car.speed
                    if car.y > HEIGHT + 20:
                        remove.append(car)

                elif d == "S":
                    if go or car.y > stop[d]:
                        car.y -= car.speed
                    if car.y < -20:
                        remove.append(car)

                elif d == "E":
                    if go or car.x > stop[d]:
                        car.x -= car.speed
                    if car.x < -20:
                        remove.append(car)

                else:
                    if go or car.x < stop[d]:
                        car.x += car.speed
                    if car.x > WIDTH + 20:
                        remove.append(car)

            for car in remove:
                self.cars[d].remove(car)

    def draw(self):
        c = self.canvas
        c.delete("all")

        c.create_rectangle(300,0,400,HEIGHT,fill="gray")
        c.create_rectangle(0,300,WIDTH,400,fill="gray")

        lights = {
            "N":(350,260),
            "S":(350,440),
            "E":(440,350),
            "W":(260,350)
        }

        for d in lights:

            color = "red"

            if d == self.light:
                if self.mode == "GREEN":
                    color = "green"
                else:
                    color = "yellow"

            x,y = lights[d]

            c.create_oval(x-8,y-8,x+8,y+8,fill=color)

        for d in self.cars:
            for car in self.cars[d]:
                c.create_rectangle(car.x-6,car.y-10,car.x+6,car.y+10,fill="blue")

        c.create_text(350,20,text=self.light+" "+self.mode)

    def update(self):

        if random.random() < 0.05:
            self.new_car()

        self.timer -= 0.05

        if self.timer <= 0:

            if self.mode == "GREEN":
                self.mode = "YELLOW"
                self.timer = self.yellow.get()

            else:
                dirs = ["N","S","E","W"]
                i = dirs.index(self.light)
                i += 1
                if i > 3:
                    i = 0
                self.light = dirs[i]
                self.mode = "GREEN"
                self.timer = self.green.get()

        self.move_cars()
        self.draw()
        self.root.after(50,self.update)

root = tk.Tk()
app = TrafficApp(root)
root.mainloop()
