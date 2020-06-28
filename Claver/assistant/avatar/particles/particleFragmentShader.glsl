#version 140

out vec4 out_colour;

in vec2 textureCoords;

uniform sampler2D particleTexture;

void main(){

	out_colour = texture(particleTexture, textureCoords);

}
