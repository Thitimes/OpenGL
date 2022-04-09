from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pandas as pd
import numpy as np

prog_id = None

def printShaderInfoLog(shader, prompt=""):
    result = glGetShaderiv(shader, GL_COMPILE_STATUS)

    if not result:

        print("%s: %s" % (prompt, glGetShaderInfoLog(shader).decode("utf-8")))

        exit()

def printProgramInfoLog(program, prompt=""):
    result = glGetProgramiv(program, GL_LINK_STATUS)

    if not result:

        print("%s: %s" % (prompt, glGetProgramInfoLog(program).decode("utf-8")))

        exit()

def compileProgram(vertex_code, fragment_code):
    prog_id = glCreateProgram()
    vert_id = glCreateShader(GL_VERTEX_SHADER)
    frag_id = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(vert_id, vertex_code)
    glShaderSource(frag_id, fragment_code)
    glCompileShader(vert_id)
    printShaderInfoLog(vert_id, "Vertex Shader")
    glCompileShader(frag_id)
    printShaderInfoLog(frag_id, "Fragment Shader")
    glAttachShader(prog_id, vert_id)
    glAttachShader(prog_id, frag_id)
    glLinkProgram(prog_id)
    printProgramInfoLog(prog_id, "Link Program")
    return prog_id

def gl_init():
    global prog_id
    global n_vertices, positions, colors, normals, uvs, centroid, bbox

    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_COLOR_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glEnable(GL_DEPTH_TEST)

    df = pd.read_csv("../models/bunny_uv.tri", delim_whitespace=True, 
                     comment='#', header=None, dtype=np.float32)
    centroid = df.values[:, 0:3].mean(axis=0)
    bbox = df.values[:, 0:3].max(axis=0) - df.values[:, 0:3].min(axis=0)

    n_vertices = len(df.values)
    positions = df.values[:, 0:3]
    colors = df.values[:, 3:6]
    normals = df.values[:, 6:9]
    uvs = df.values[:, 9:11]
    

    vert_code = '''
#version 120
varying vec3 normal;

void main()
{
    gl_Position =  gl_ProjectionMatrix * gl_ModelViewMatrix * gl_Vertex;
    normal = gl_Normal.xyz;
}
                '''
    frag_code = ''' 
#version 120
varying vec3 normal;
void main()
{
    gl_FragColor.rgb = 0.5 * (normal+1);
}
                '''                
    prog_id = compileProgram(vert_code, frag_code)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, 800/600, 0.01, 100)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 3, 0, 0, 0, 0, 1, 0)
    glUseProgram(prog_id)
    glVertexPointer(3, GL_FLOAT, 0, positions)
    glColorPointer(3, GL_FLOAT, 0, colors)
    glNormalPointer(GL_FLOAT, 0, normals)
    glDrawArrays(GL_TRIANGLES, 0, n_vertices)
    glutSwapBuffers()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutInitWindowPosition(50, 50)    
    glutCreateWindow("GLSL Shaders Exercise")
    glutDisplayFunc(display)
    gl_init()
    glutMainLoop()

if __name__ == "__main__":
    main()    