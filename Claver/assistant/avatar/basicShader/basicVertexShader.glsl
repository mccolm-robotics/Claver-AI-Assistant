#version 450 core
in vec3 position;

out vec2 textureCoords;


uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;


void main(){
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0);
    textureCoords = vec2(position.x/2.0 + 0.5, position.z/2.0 + 0.5);

}