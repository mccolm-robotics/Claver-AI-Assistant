import numpy as np
from OpenGL.GL import *

vao_list = np.empty(0, dtype=np.uint32)

test = GLuint(0)
print(test)

vao_list = np.append(vao_list, test)

test1 = GLuint(5)

vao_list = np.append(vao_list, test1)

print(vao_list)

print(GLuint(vao_list[1]))

print("now iterating")
for x in np.nditer(vao_list):
    print(x)