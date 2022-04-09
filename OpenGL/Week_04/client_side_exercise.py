import sys, os
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import pandas as pd
import math as m
import time

win_w, win_h = 1024, 768

def reshape(w, h):
    global win_w, win_h

    win_w, win_h = w, h
    glViewport(0, 0, w, h)  
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, win_w/win_h, 0.01, 50)

wireframe, pause = False, True
def keyboard(key, x, y):
    global wireframe, pause

    key = key.decode("utf-8")
    if key == ' ':
        pause = not pause
        glutIdleFunc(None if pause else idle)
    elif key == 'w':
        wireframe = not wireframe
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE if wireframe else GL_FILL)
    elif key == 'q':
        os._exit(0)
    glutPostRedisplay()

tick, frame_cnt = 0, 0
def idle():
    global tick, frame_cnt

    tick += 1
    frame_cnt += 1
    glutPostRedisplay()

def display():
    global start_time, frame_cnt
    if frame_cnt == 20:
        print("%.2f fps" % (frame_cnt/(time.time()-start_time)), tick, end='\r')
        start_time = time.time()
        frame_cnt = 0    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    eye_pos = centroid + (0, 0, 1.5*max(bbox))
    gluLookAt(*eye_pos, *centroid, 0, 1, 0)
    light_pos = eye_pos

    glTranslatef(*centroid)
    glRotatef(tick, 0, 1, 0)
    glTranslatef(*(-centroid))
    gluLookAt( centroid[0], centroid[1]+2, centroid[2] + 6,centroid[0], centroid[1], centroid[2],0, 1, 0 )
    glScale( 0.5, 0.5, 0.5 )
    glTranslate( -4.5, 0, 0 )
    glVertexPointer(3, GL_FLOAT, 0, positions)
    glColorPointer(3, GL_FLOAT, 0, colors)
    glNormalPointer(GL_FLOAT, 0, normals)
    glTexCoordPointer(2, GL_FLOAT, 0, uvs)
    for i in range(5):
        for j in range(6):
            glTranslate( 1.5, 0, 0 )
            glDrawArrays(GL_TRIANGLES, 0, n_vertices)  
        glTranslate(-9,0,1.5)

    glutSwapBuffers()

def gl_init_models():
    global start_time
    global n_vertices, positions, colors, normals, uvs, centroid, bbox

    glClearColor(0, 0, 0, 0)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightModeli(GL_LIGHT_MODEL_LOCAL_VIEWER, GL_TRUE)
    al = [0.1, 0.1, 0.1, 1.0]
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, al)

    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_COLOR_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glEnableClientState(GL_TEXTURE_COORD_ARRAY)

    df = pd.read_csv("../models/bunny_uv.tri", delim_whitespace=True,
                     comment='#', header=None, dtype=np.float32)
    centroid = df.values[:, 0:3].mean(axis=0)
    bbox = df.values[:, 0:3].max(axis=0) - df.values[:, 0:3].min(axis=0)

    n_vertices = len(df.values)
    positions = np.ones((n_vertices, 3), np.float32)
    normals = np.zeros((n_vertices, 3), np.float32)
    positions[:, 0:3] = df.values[:, 0:3]
    colors = df.values[:, 3:6]
    normals[:, 0:3] = df.values[:, 6:9]
    uvs = df.values[:, 9:11]
    start_time = time.time() - 0.0001

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(win_w, win_h)
    glutCreateWindow("Client-side Vertex Arrays Exercise")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    gl_init_models()
    glutMainLoop()

if __name__ == "__main__":
    main()