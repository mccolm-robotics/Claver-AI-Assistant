import numpy as np

heights = np.empty(shape=[10, 10])

for i in range(10):
    for j in range(10):
        heights[i][j] = 5

print(heights[0].size - 1)