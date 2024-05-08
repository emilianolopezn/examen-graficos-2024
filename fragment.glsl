#version 330 core
in vec3 fragmentColor;
out vec4 fragColor;
void main()
{
    fragColor = vec4(fragmentColor.x, fragmentColor.y, fragmentColor.z, 1.0f);
}