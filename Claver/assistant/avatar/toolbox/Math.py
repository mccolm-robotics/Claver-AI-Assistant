import pyrr
from pyrr import Matrix44


def createTransformationMatrix(position, rotX, rotY, rotZ, scale, clock):
    if rotX == 0 and rotY == 0 and rotZ == 0:
        return Matrix44.from_translation(position) * Matrix44.from_scale([scale, scale, scale])
    return Matrix44.from_translation(position) * pyrr.matrix44.create_from_axis_rotation((rotX, rotY, rotZ), clock) * Matrix44.from_scale([scale, scale, scale])


def createProjectionMatrix(fov, width, height, near, far):
    return Matrix44.perspective_projection(fov, width / height, near, far)


def createViewMatrix(camera):
    position = camera.getPosition()                     # Eye coordinates (location of the camera)
    target = (0.0, 0.0, 0.0)                            # Target coordinates (where the camera is looking)
    up = (0.0, 1.0, 0.0)                                # A vector representing the 'up' direction.
    return Matrix44.look_at(position, target, up)       # Calculate the view matrix
