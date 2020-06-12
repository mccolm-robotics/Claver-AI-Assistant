#version 400

in vec3 position;
out vec3 textureCoords;

uniform mat4 transformationMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

void main(){

    gl_Position = projectionMatrix * viewMatrix * transformationMatrix * vec4(position, 1.0);

	textureCoords = position;
}
