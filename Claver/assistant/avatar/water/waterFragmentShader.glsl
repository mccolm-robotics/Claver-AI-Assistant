#version 450 core

in vec4 clipSpace;
in vec2 textureCoords;

out vec4 out_Colour;

uniform sampler2D reflectionTexture;
uniform sampler2D refractionTexture;
uniform sampler2D dudvMap;

uniform float moveFactor;

const float waveStrength = .003;

void main()
{

    vec2 normalizedDeviceCoords = (clipSpace.xy / clipSpace.w) / 2.0 + 0.5;
    vec2 refractTexCoords = vec2(normalizedDeviceCoords.x, normalizedDeviceCoords.y);
    vec2 reflectTexCoords = vec2(normalizedDeviceCoords.x, -normalizedDeviceCoords.y);

    vec2 distortion1 = (texture(dudvMap, vec2(textureCoords.x + moveFactor, textureCoords.y)).rg * 2.0 - 1.0) * waveStrength;
    vec2 distortion2 = (texture(dudvMap, vec2(-textureCoords.x + moveFactor, textureCoords.y + moveFactor)).rg * 2.0 - 1.0) * waveStrength;
    vec2 totalDistortion = distortion1 + distortion2;

    refractTexCoords += totalDistortion;
    refractTexCoords = clamp(refractTexCoords, 0.001, 0.999);

    reflectTexCoords += totalDistortion;
    reflectTexCoords.x = clamp(reflectTexCoords.x, 0.001, 0.999);
    reflectTexCoords.y = clamp(reflectTexCoords.y, -0.999, -0.001);

    vec4 reflectColour = texture(reflectionTexture, reflectTexCoords);
    vec4 refractColour = texture(refractionTexture, refractTexCoords);

    out_Colour = mix(reflectColour, refractColour, 0.5);

}