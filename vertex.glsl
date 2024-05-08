#version 330 core
layout (location = 0) in vec3 posicion;
in vec3 entradaColor;
out vec3 fragmentColor;
void main()
{
    gl_Position = vec4(posicion.x, posicion.y, posicion.z, 1.0f);

    fragmentColor = entradaColor;
}