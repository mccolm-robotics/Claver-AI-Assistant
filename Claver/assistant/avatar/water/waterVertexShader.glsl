#version 450 core

in vec3 position;

out vec4 clipSpace;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;


void main(){

    clipSpace = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0);
    gl_Position = clipSpace;

}