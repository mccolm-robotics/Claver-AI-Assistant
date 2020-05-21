from pyrr import Vector3
test = Vector3([5.0, 3.0, 9.0])
dx = 3
trap = Vector3(test)
trap.y+=dx
print(trap[1])

