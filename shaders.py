import glfw
from OpenGL.GL import *
import numpy as np
from ctypes import c_void_p

def leer_archivo(ruta):
    contenido = ''
    with open(ruta, 'r') as file: 
        contenido = file.read()
    return contenido

def framebuffer_size_callback(window, ancho, alto):
    glViewport(0,0,ancho,alto)

def main():
    ancho = 400
    alto = 400
    glfw.init()
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR,3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR,3)
    glfw.window_hint(glfw.OPENGL_PROFILE,glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
    window = glfw.create_window(ancho, alto,"Shaders",None,None)
    if window is None:
        glfw.terminate()
        exit()
    glfw.make_context_current(window)
    glfw.set_framebuffer_size_callback(window,framebuffer_size_callback)
    codigo_vertex = leer_archivo('vertex.glsl')
    codigo_fragment = leer_archivo('fragment.glsl')
    vertex_shader = glCreateShader(GL_VERTEX_SHADER)
    glShaderSource(vertex_shader, codigo_vertex)
    glCompileShader(vertex_shader)
    exito = glGetShaderiv(vertex_shader, GL_COMPILE_STATUS)
    if not exito:
        info_log = glGetShaderInfoLog(vertex_shader)
        print(info_log)
        exit()
    fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(fragment_shader,codigo_fragment)
    glCompileShader(fragment_shader)
    exito = glGetShaderiv(fragment_shader, GL_COMPILE_STATUS)
    if not exito:
        info_log = glGetShaderInfoLog(fragment_shader)
        print(info_log)
        exit()  
    programa_shader = glCreateProgram()
    glAttachShader(programa_shader, vertex_shader)
    glAttachShader(programa_shader, fragment_shader)
    glLinkProgram(programa_shader)
    exito = glGetProgramiv(programa_shader, GL_LINK_STATUS)
    if not exito:
        info_log = glGetProgramInfoLog(programa_shader)
        print(info_log)
        exit()
    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)
    vertices = np.array( 
        [-0.5, -0.5, 0.0,  
         0.5, -0.5, 0.0,  
         0.0, 0.5, 0.0],  
        dtype="float32")
    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)
    glBindVertexArray(VAO)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,0,c_void_p(0))
    glEnableVertexAttribArray(0)
    colores = np.array( 
        [1.0, 0.0, 0.0, 
         0.0, 1.0, 0.0,  
         0.0, 0.0, 1.0]  
        , dtype="float32")
    color_VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, color_VBO)
    glBufferData(GL_ARRAY_BUFFER, colores.nbytes, colores, GL_STATIC_DRAW)
    glVertexAttribPointer(1,3,GL_FLOAT,GL_FALSE,0,c_void_p(0))
    glEnableVertexAttribArray(1)
    while not glfw.window_should_close(window):
        glClearColor(0.2,0.3,0.3,1.0)
        glClear(GL_COLOR_BUFFER_BIT)
        glUseProgram(programa_shader)
        glBindVertexArray(VAO)
        glDrawArrays(GL_TRIANGLES,0,3)
        glfw.swap_buffers(window)
        glfw.poll_events()
    glDeleteVertexArrays(1, [VAO])
    glDeleteBuffers(1, [VBO])
    glDeleteProgram(programa_shader)
    glfw.terminate()
    return 0

if __name__ == '__main__':
   main()