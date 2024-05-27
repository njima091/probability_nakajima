import random
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

MAX_LENGTH = 100
ZERO_PROBABILITY = 0.1

zero_set = set()
time_grid = {}

# Initialize zero_set and time_grid
for x in range(-MAX_LENGTH-3, MAX_LENGTH+3):
    for y in range(-MAX_LENGTH-3, MAX_LENGTH+3):
        for z in range(-MAX_LENGTH-3, MAX_LENGTH+3):
            if random.random() < ZERO_PROBABILITY and abs(x) + abs(y) + abs(z) < MAX_LENGTH:
                zero_set.add((x, y, z))
            time_grid[(x, y, z)] = abs(x) + abs(y) + abs(z)

# Update function
def update_function(length):
    global time_grid
    
    for x in range(-length-1, length+1):
        for y in range(-length+abs(x)-1, length-abs(x)+1):
            for z in range(-length+abs(x)+abs(y)-1, length-abs(x)-abs(y)+1):
                neighbors = [
                    (x-1, y, z), (x+1, y, z), (x, y-1, z), (x, y+1, z), (x, y, z-1), (x, y, z+1)
                ]
                min_value = min(time_grid.get(neighbor, float('inf')) for neighbor in neighbors)
                if (x, y, z) in zero_set:
                    time_grid[(x, y, z)] = min(time_grid[(x, y, z)], min_value)
                else:
                    time_grid[(x, y, z)] = min(time_grid[(x, y, z)], min_value + 1)

# Apply the update function iteratively
for number in range(1, MAX_LENGTH):
    update_function(number)

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(-MAX_LENGTH, MAX_LENGTH)
ax.set_ylim(-MAX_LENGTH, MAX_LENGTH)
ax.set_zlim(-MAX_LENGTH, MAX_LENGTH)

# Initialize a plot which we will update during animation
points = ax.scatter([], [], [], c='b', s=10)

# Adding the wireframe mesh for all integer Z values
X, Y, Z = np.meshgrid(np.arange(-MAX_LENGTH, MAX_LENGTH, 1),
                      np.arange(-MAX_LENGTH, MAX_LENGTH, 1),
                      np.arange(-MAX_LENGTH, MAX_LENGTH, 1))

def draw_wireframe(ax, X, Y, Z):
    for z in range(-MAX_LENGTH, MAX_LENGTH, 25):  # Adjust step size for visibility
        ax.plot_wireframe(X[:, :, z], Y[:, :, z], Z[:, :, z], color='gray', alpha=0.1)

draw_wireframe(ax, X, Y, Z)

def update(t):
    xs, ys, zs = [], [], []
    for (x, y, z), time in time_grid.items():
        if time < t:
            xs.append(x)
            ys.append(y)
            zs.append(z)
    
    points._offsets3d = (xs, ys, zs)
    ax.set_title(f'Time = {t}')
    angle = 20 + t % 360
    ax.view_init(30, angle)
    return points,

# Create animation
ani = FuncAnimation(fig, update, frames=np.arange(1, MAX_LENGTH//2), interval=10)

# Show or save animation
#plt.show()
ani.save('time_grid_animation.gif', writer='pillow')
