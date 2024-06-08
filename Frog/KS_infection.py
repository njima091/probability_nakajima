import tkinter as tk
import random

# Parameters
WIDTH = 1000
HEIGHT = 1000
STEP_SIZE = 10
CIRCLE_SIZE = STEP_SIZE//3
DELAY = 20  # in milliseconds

class RandomWalk:
    def __init__(self, master, canvas, start_x, start_y, color):
        self.master = master
        self.canvas = canvas
        self.start_x = start_x + WIDTH//2
        self.start_y = start_y + HEIGHT//2
        self.color = color
        self.object = None
        self.current_x = self.start_x
        self.current_y = self.start_y
        self.draw_initial_point()

    def draw_initial_point(self):
        if self.color == "red":
            self.object = self.canvas.create_oval(
                self.start_x - CIRCLE_SIZE, self.start_y - CIRCLE_SIZE,
                self.start_x + CIRCLE_SIZE, self.start_y + CIRCLE_SIZE,
                fill=self.color
            )

    def step(self):
        direction = random.choice(['up', 'down', 'left', 'right'])
        if direction == 'up':
            new_x, new_y = self.current_x, self.current_y - STEP_SIZE
        elif direction == 'down':
            new_x, new_y = self.current_x, self.current_y + STEP_SIZE
        elif direction == 'left':
            new_x, new_y = self.current_x - STEP_SIZE, self.current_y
        else:  # direction == 'right'
            new_x, new_y = self.current_x + STEP_SIZE, self.current_y

        self.current_x, self.current_y = new_x, new_y
        if self.color == "red":
            self.canvas.delete(self.object)
            
            self.object = self.canvas.create_oval(
                new_x - CIRCLE_SIZE, new_y - CIRCLE_SIZE, new_x + CIRCLE_SIZE, new_y + CIRCLE_SIZE, fill=self.color
            )

    def change_color(self, new_color):
        self.color = new_color

# Initialize Tkinter root and canvas
root = tk.Tk()
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
canvas.pack()

# Draw the grid on the canvas
for x in range(0, WIDTH, STEP_SIZE):
    canvas.create_line(x, 0, x, HEIGHT, fill="lightgrey")
for y in range(0, HEIGHT, STEP_SIZE):
    canvas.create_line(0, y, WIDTH, y, fill="lightgrey")

# Create multiple RandomWalkApp instances
app = {}

for x in range(-3*WIDTH, 2*WIDTH, STEP_SIZE):
    for y in range(-3*HEIGHT, 2*HEIGHT, STEP_SIZE):
        if not (x == 0 and y == 0):
            app[(x, y)] = RandomWalk(root, canvas, x, y, "blue")

app[(0, 0)] = RandomWalk(root, canvas, 0, 0, "red")

def time_pass():
    positions = {}
    for key in app:
        walker = app[key]
        walker.step()
        pos = (walker.current_x, walker.current_y)
        if pos in positions:
            positions[pos].append(walker)
        else:
            positions[pos] = [walker]

    # Check for overlap and change color if needed
    for pos in positions:
        walkers_at_pos = positions[pos]
        if any(walker.color == "red" for walker in walkers_at_pos):
            for walker in walkers_at_pos:
                walker.change_color("red")

    root.after(DELAY, time_pass)

# Start the movement
time_pass()

root.mainloop()
