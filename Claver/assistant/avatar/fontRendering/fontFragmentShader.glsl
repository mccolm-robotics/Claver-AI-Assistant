#version 330

in vec2 pass_textureCoords;

out vec4 out_colour;

uniform vec3 colour;
uniform sampler2D fontAtlas;

// Small text: Width=0.46   Edge 0.19
// Large text: Width=0.51   Edge 0.02
const float width = 0.5;
const float edge = 0.1;

//const float borderWidth = 0;
//const float borderEdge = 0.4;
const float borderWidth = 0.7;
const float borderEdge = 0.1;

const float innerWidth = 0.5;
const float innerEdge = 0.1;

const vec2 offset = vec2(0, 0);

const vec3 outlineColour = vec3(0.8, 0.8, 0.8);

void main(){

    //float distance = 1.0 - texture(fontAtlas, pass_textureCoords).a;
    //float alpha = 1.0 - smoothstep(width, width + edge, distance);

    //float distance2 = 1.0 - texture(fontAtlas, pass_textureCoords + offset).a;
    //float outlineAlpha = 1.0 - smoothstep(borderWidth, borderWidth + borderEdge, distance2);

    //float overallAlpha = alpha + (1.0 - alpha) * outlineAlpha;
    //vec3 overallColour = mix(outlineColour, colour, alpha / overallAlpha);

    //out_colour = vec4(overallColour, overallAlpha);

    float distance = 1.0 - texture(fontAtlas, pass_textureCoords).a;

    float outlineAlpha = 1.0 - smoothstep(borderWidth, borderWidth + borderEdge, distance);
    float innerAlpha = smoothstep(innerWidth, innerWidth + innerEdge, distance);

    float overallAlpha = outlineAlpha * innerAlpha;
    out_colour = vec4(outlineColour, overallAlpha);
}
