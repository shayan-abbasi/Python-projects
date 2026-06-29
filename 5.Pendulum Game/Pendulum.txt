import tkinter as tk
import math

WIDTH = 600
HEIGHT = 450
CART_Y = 320

class Pendulum:
    def __init__(self):
        self.angle = 0.1
        self.angle_vel = 0.0
        self.length = 120
        self.gravity = 9.8

    def update(self, cart_acc, dt):
        angle_acc = (self.gravity * math.sin(self.angle) - cart_acc * math.cos(self.angle)) / self.length
        self.angle_vel = self.angle_vel + angle_acc * dt
        self.angle_vel = self.angle_vel * 0.995
        self.angle = self.angle + self.angle_vel * dt

    def is_fallen(self):
        if self.angle > 1.0 or self.angle < -1.0:
            return True
        return False

class Cart:
    def __init__(self):
        self.x = WIDTH / 2
        self.vel = 0.0
        self.acc = 0.0
        self.force = 0.0

    def update(self, dt):
        self.acc = self.force / 5.0
        self.vel = self.vel + self.acc * dt
        self.vel = self.vel * 0.9
        self.x = self.x + self.vel * dt

        if self.x < 50:
            self.x = 50
            self.vel = 0.0
        if self.x > WIDTH - 50:
            self.x = WIDTH - 50
            self.vel = 0.0

class Controller:
    def __init__(self):
        self.kp = 50.0
        self.kd = 10.0

    def compute(self, angle, angle_vel):
        force = self.kp * angle + self.kd * angle_vel
        if force > 200:
            force = 200
        if force < -200:
            force = -200
        return force

class Simulation:
    def __init__(self):
        self.pendulum = Pendulum()
        self.cart = Cart()
        self.controller = Controller()
        self.running = False
        self.dt = 0.03

    def reset(self):
        self.pendulum = Pendulum()
        self.cart = Cart()
        self.running = False

    def step(self):
        self.cart.update(self.dt)
        self.pendulum.update(self.cart.acc, self.dt)

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Inverted Pendulum")
        self.sim = Simulation()

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
        self.canvas.pack()

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Start", width=8, command=self.start).pack(side="left", padx=3)
        tk.Button(btn_frame, text="Stop",  width=8, command=self.stop).pack(side="left", padx=3)
        tk.Button(btn_frame, text="Reset", width=8, command=self.reset).pack(side="left", padx=3)

        tk.Label(root, text="Use  ←  →  keys to move cart").pack()

        self.status = tk.Label(root, text="Press Start", font=("Arial", 12), fg="blue")
        self.status.pack()

        self.root.bind("<Left>",  self.push_left)
        self.root.bind("<Right>", self.push_right)

        self.draw()

    def push_left(self, event):
        self.sim.cart.force = -150

    def push_right(self, event):
        self.sim.cart.force = 150

    def start(self):
        self.sim.running = True
        self.status.config(text="Running...", fg="green")
        self.loop()

    def stop(self):
        self.sim.running = False
        self.status.config(text="Stopped", fg="orange")

    def reset(self):
        self.sim.reset()
        self.status.config(text="Press Start", fg="blue")
        self.draw()

    def loop(self):
        if self.sim.running == True:
            self.sim.step()
            self.sim.cart.force = self.sim.cart.force * 0.8

            if self.sim.pendulum.is_fallen() == True:
                self.sim.running = False
                self.status.config(text="FALLEN! Press Reset", fg="red")

            self.draw()
            self.root.after(30, self.loop)

    def draw(self):
        self.canvas.delete("all")

        self.canvas.create_line(0, CART_Y + 20, WIDTH, CART_Y + 20, fill="black", width=2)

        cx = self.sim.cart.x

        self.canvas.create_rectangle(cx - 40, CART_Y - 25, cx + 40, CART_Y, fill="steelblue", outline="black")
        self.canvas.create_oval(cx - 18 - 7, CART_Y - 7, cx - 18 + 7, CART_Y + 7, fill="gray")
        self.canvas.create_oval(cx + 18 - 7, CART_Y - 7, cx + 18 + 7, CART_Y + 7, fill="gray")

        angle = self.sim.pendulum.angle
        length = self.sim.pendulum.length
        px = cx + length * math.sin(angle)
        py = CART_Y - 25 - length * math.cos(angle)

        self.canvas.create_line(cx, CART_Y - 25, px, py, fill="black", width=3)
        self.canvas.create_oval(px - 10, py - 10, px + 10, py + 10, fill="orange", outline="black")

        self.canvas.create_text(10, 15, anchor="w", text="Angle: " + str(round(math.degrees(angle), 1)) + " deg", font=("Arial", 10))
        self.canvas.create_text(10, 35, anchor="w", text="Cart X: " + str(round(cx, 1)), font=("Arial", 10))


root = tk.Tk()
app = GUI(root)
root.mainloop()