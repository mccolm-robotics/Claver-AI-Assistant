#version 450 core

in vec4 clipSpace;

out vec4 out_Colour;

uniform sampler2D reflectionTexture;
uniform sampler2D refractionTexture;

void main()
{

    vec2 normalizedDeviceCoords = (clipSpace.xy / clipSpace.w) / 2.0 + 0.5;
    vec2 refractTexCoords = vec2(normalizedDeviceCoords.x, normalizedDeviceCoords.y);
    vec2 reflectTexCoords = vec2(normalizedDeviceCoords.x, -normalizedDeviceCoords.y);

    vec4 reflectColour = texture(reflectionTexture, reflectTexCoords);
    vec4 refractColour = texture(refractionTexture, refractTexCoords);

    out_Colour = mix(reflectColour, refractColour, 0.5);

}