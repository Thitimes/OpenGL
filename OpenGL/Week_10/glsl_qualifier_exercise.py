import sys, os, time
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import pandas as pd

win_w, win_h = 1024, 768

def create_shaders():
    global prog_id, vao, vbo

    vert_code = b'''
#version 140
void main()
{
    gl_Projection =  gl_Vertex;
   // Fix me!
}'''
    frag_code = b'''
#version 140
void main()
{
    // Fix me!
}'''
    prog_id = compileProgram(vert_code, frag_code)

    # Fix me!
    # Implement VAO and VBO here.

wireframe, pause = False, True
normal_color_on = False
def keyboard(key, x, y):
    global wireframe, pause, normal_color_on

    key = key.decode("utf-8")
    if key == ' ':
        pause = not pause
        glutIdleFunc(None if pause else idle)
    elif key == 'w':
        wireframe = not wireframe
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE if wireframe else GL_FILL)
    if key == 'n':
        normal_color_on = not normal_color_on
    elif key == 'q':
        os._exit(0)
    glutPostRedisplay()

def reshape(w, h):
    global win_w, win_h, proj_mat

    win_w, win_h = w, h
    glViewport(0, 0, w, h)  
    gluPerspective(60, win_w/win_h, 0.01, 10)

def display():
    global start_time, frame_cnt
    if frame_cnt == 20:
        print("%.2f fps" % (frame_cnt/(time.time()-start_time)), end='\r')
        start_time = time.time()
        frame_cnt = 0 

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    gluLookAt(*eye_pos, *centroid, 0, 1, 0)
    glRotatef(tick, 0, 1, 0)

    glUseProgram(prog_id)
    glBindVertexArray(vao)
    glDrawArrays(GL_TRIANGLES, 0, n_vertices)
    glutSwapBuffers()

frame_cnt, tick = 0, 0
def idle():
    global frame_cnt, tick

    frame_cnt += 1
    tick += 1
    glutPostRedisplay()

def init_model():
    global n_vertices, positions, colors, normals, uvs, centroid, bbox, eye_pos
    global start_time

    glClearColor(0.01, 0.01, 0.2, 1)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

    df = pd.read_csv("../models/bunny_uv.tri", delim_whitespace=True,
                     comment='#', header=None, dtype=np.float32)
    centroid = df.values[:, 0:3].mean(axis=0)
    bbox = df.values[:, 0:3].max(axis=0) - df.values[:, 0:3].min(axis=0)
    eye_pos = centroid + (0, 0, 1.2*max(bbox))

    positions = df.values[:, 0:3]
    colors = df.values[:, 3:6]
    normals = df.values[:, 6:9]
    uvs = df.values[:, 9:11]

    n_vertices = len(positions)
    print("no. of vertices: %d, no. of triangles: %d" % 
          (n_vertices, n_vertices//3))
    print("Centroid:", centroid)
    print("BBox:", bbox)
    start_time = time.time() - 1e-4

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(win_w, win_h)
    glutInitWindowPosition(50, 0)    
    glutCreateWindow("GLSL Qualifier Exercise")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutIdleFunc(idle)
    init_model()
    create_shaders()
    glutMainLoop()

if __name__ == "__main__":
    main()