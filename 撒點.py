import numpy as np
import random
import matplotlib.pyplot as plt
import csv

def uniform_x_y (x1, y1, x2, y2):
    x = round(random.uniform(x1, x2), 3)
    y = round(random.uniform(y1, y2), 3)
    dot = [x, y]
    return dot

def inside(dot, a, b):
    x = dot[0]
    y = dot[1]
    if (x <= b[0] and x >= a[0] and y <= b[1] and y >= a[1]):
        return True
    return False
avoid = [[1, 1], [1, 4], [1, 5], [1, 6], [1, 7], [1, 8],
         [2, 5], [2, 6], [2, 7], [2, 8],
         [3, 6], [3, 7],
         [6, 1], [6, 8],
         [7, 1], [7, 7], [7, 8],
         [8, 1], [8, 2], [8, 5], [8, 6], [8, 7], [8, 8]]

dots = []
for i in range(1, 9):
    for j in range(1, 9):
        if [i, j] not in avoid:
            for _ in range(10):
                dot = uniform_x_y(i, j, i+1, j+1)
                while inside(dot, [5.11, 2.62], [6.72, 3.26]):
                    dot = uniform_x_y(i, j, i+1, j+1)
                dots.append(dot)

print(dots)   
x_coords = [dot[0] for dot in dots]
y_coords = [dot[1] for dot in dots]

# Plot the dots
plt.figure(figsize=(8, 8))
plt.scatter(y_coords, x_coords, s=10, c='blue', marker='o')

# Set plot limits and labels
plt.xlim(0, 10)
plt.ylim(0, 10)
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Randomly Generated Dots')

# Display the plot
plt.grid(True)
plt.show()

with open('dots.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['x', 'y'])  # Write the header
    writer.writerows(dots)