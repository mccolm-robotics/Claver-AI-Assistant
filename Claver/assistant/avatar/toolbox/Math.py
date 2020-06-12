import pyrr
from pyrr import Matrix44
from pyrr import Vector3


def createTransformationMatrix(position, rotX=0, rotY=0, rotZ=0, scale=1):
    if rotX == 0 and rotY == 0 and rotZ == 0:
        return Matrix44.from_translation(position) * Matrix44.from_scale([scale, scale, scale])
    return Matrix44.from_translation(position) * pyrr.matrix44.create_from_axis_rotation((rotX, rotY, rotZ), rotY) * Matrix44.from_scale([scale, scale, scale])

def create2DTransformationMatrix(position, scale):
    scaleTransform = Vector3((scale[0], scale[1], 1.0))
    positionTransform = Vector3((position[0], position[1], 0))
    return Matrix44.from_translation(positionTransform) * Matrix44.from_scale(scaleTransform)

def createProjectionMatrix(fov, width, height, near, far):
    return Matrix44.perspective_projection(fov, width / height, near, far)


def createViewMatrix(camera):
    position = camera.getPosition()  # Eye coordinates (location of the camera)
    # front = camera.getFront()
    # target = position + front                           # Target coordinates (where the camera is looking)
    target = list(camera.getPlayer().getPosition())
    target[1] = 2.5
    up = (0.0, 1.0, 0.0)  # A vector representing the 'up' direction.
    return Matrix44.look_at(position, target, up)  # Calculate the view matrix


def barryCentric(p1, p2, p3, pos):
    # pos is a Vector2
    p1 = Vector3(p1)
    p2 = Vector3(p2)
    p3 = Vector3(p3)
    det = (p2.z - p3.z) * (p1.x - p3.x) + (p3.x - p2.x) * (p1.z - p3.z)
    l1 = ((p2.z - p3.z) * (pos[0] - p3.x) + (p3.x - p2.x) * (pos[1] - p3.z)) / det
    l2 = ((p3.z - p1.z) * (pos[0] - p3.x) + (p1.x - p3.x) * (pos[1] - p3.z)) / det
    l3 = 1.0 - l1 - l2
    return l1 * p1.y + l2 * p2.y + l3 * p3.y
