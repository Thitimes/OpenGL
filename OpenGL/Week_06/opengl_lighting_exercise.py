import sys, os
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import numpy as np
import pandas as pd
import math as m

t_value = 0
isClicked = False
angle = 0
start_pos = [0,0]
def reshape(w, h):
    glViewport(0, 0, w, h)	
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, w/h, 0.1, 50)

def load_texture(filename):

    try:

        im = Image.open(filename)

    except:

        print("Error:", sys.exc_info()[0])

    w = im.size[0]

    h = im.size[1]

    image = im.tobytes("raw", "RGB", 0)

    tex_id = glGenTextures(1)

    glActiveTexture(GL_TEXTURE0)

    glBindTexture(GL_TEXTURE_2D, tex_id)

    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    glTexImage2D(GL_TEXTURE_2D, 0, 3, w, h, 0, GL_RGB, GL_UNSIGNED_BYTE, image)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    eye_pos = (0,1,2)
    Il = (1,1,1)
    eye_at = centroid

    gluLookAt(*eye_pos, *eye_at, 0, 1, 0)

    light_ambient = [1.0, 1.0, 1.0, 1.0]
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)

    light_dif = [1.0, 1.0, 1.0, 1.0]
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_dif)

    light_spec = [1.0, 1.0, 1.0, 1.0]
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_spec)

    light_pos = [m.cos((angle/180) * m.pi) * 5,0,m.sin((angle/180) * m.pi) * 5,1]
    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)

    mat_ambient = [0.05, 0.05, 0.05, 1.0]
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, mat_ambient)
    
    mat_diffuse = [0.86, 0.65, 0.13, 1.0]
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_diffuse)

    mat_specular = [1, 1, 0, 1.0]
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, mat_specular)

    mat_shininess = 50
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, mat_shininess)

    glRotatef(t_value, 0, 1, 0)
    glEnable(GL_TEXTURE_2D)

    glColor3f(1.0, 1.0, 0.0)

    glBegin(GL_QUADS)

    glTexCoord2f(0.0, 1.0); glVertex3f(0.0, 0.0, 0.0)

    glTexCoord2f(0.0, 0.0); glVertex3f(0.0, 8.0, 0.0)

    glTexCoord2f(1.0, 0.0); glVertex3f(10.0, 8.0, 0.0)

    glTexCoord2f(1.0, 1.0); glVertex3f(10.0, 0.0, 0.0)

    glEnd()

    glDisable(GL_TEXTURE_2D)

    glVertexPointer(3, GL_FLOAT, 0, positions)
    glColorPointer(3, GL_FLOAT, 0, colors)
    glNormalPointer(GL_FLOAT, 0, normals)
    glTexCoordPointer(2, GL_FLOAT, 0, uvs)
    glDrawArrays(GL_TRIANGLES, 0, n_vertices)      
    glutSwapBuffers()

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

def idle():
    global t_value
    t_value += 1
    glutPostRedisplay()

def mouseCB(button, state, x,y):
    global isClicked
    global start_pos
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        isClicked = True
        start_pos = [x,y]
    else:
        isClicked = False

def motionCB(x,y):
    global angle
    if isClicked == True:
        angle += (x - start_pos[0]) * 0.1
        glutPostRedisplay()


def gl_init():
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
    positions = df.values[:, 0:3]
    colors = df.values[:, 3:6]
    normals = df.values[:, 6:9]
    uvs = df.values[:, 9:11]
    print("no. of vertices: %d, no. of triangles: %d" % 
          (n_vertices, n_vertices//3))
    print("Centroid:", centroid)
    print("BBox:", bbox)

def main():
    image = "../texture_map/bunny_hair.jpg" 
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(1024, 768)
    glutCreateWindow("OpenGL Lighting Exercise")
    load_texture(Image)
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouseCB)
    glutMotionFunc(motionCB)
    gl_init()
    glutMainLoop()

if __name__ == "__main__":
    main()