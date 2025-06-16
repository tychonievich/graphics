#version 300 es

in vec4 position;
in vec4 color;

uniform float seconds;

out vec4 vColor;

void main() {
    vColor = color;
    gl_Position = position;
}
