class Math:
    def __init__(self):
        pass

    def createTransformationMatrix(self, translation, rx, ry, rz, scale):
        ...
        return modelMatrix

    def createViewMatrix(self, camera):
        ...
        return viewMatrix


public static Matrix4f createTransformationMatrix(Vector2f translation, Vector2f scale) {
		Matrix4f matrix = new Matrix4f();
		matrix.setIdentity();
		Matrix4f.translate(translation, matrix, matrix);
		Matrix4f.scale(new Vector3f(scale.x, scale.y, 1f), matrix, matrix);
		return matrix;
	}

