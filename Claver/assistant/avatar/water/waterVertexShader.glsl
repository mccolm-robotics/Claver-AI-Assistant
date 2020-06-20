#version 450 core

in vec3 position;

out vec4 clipSpace;
out vec2 textureCoords;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

const float tiling = 6.0;

void main(){

    clipSpace = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0);
    gl_Position = clipSpace;
    textureCoords = vec2(position.x/2.0 + 0.5, position.y/2.0 + 0.5) * tiling;
}