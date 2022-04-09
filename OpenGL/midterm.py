import sys

from OpenGL.GL import *

from OpenGL.GLU import *

from OpenGL.GLUT import *

from math import pi, sin, cos

def display():

    #eye_pos = (0,0,2)
    #aimTo = (0,0,1)
    #gluLookAt(*eye_pos, *aimTo, 0, 1, 0)
    
    x1 = -0.2
    x2 = 0.2
    x3 = 0.2
    x4 = -0.2
    y1 = -0.2
    y2 = -0.2
    y3 = 0.2
    y4 = 0.2
    glRotate(30,x1, y1, 0.0)
    glRotate(30,x2, y2, 0.0)
    glRotate(30,x3, y3, 0.0)
    glRotate(30,x4, y4, 0.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0.0,1.0,1.0)
    glBegin(GL_POLYGON)
    
    glVertex3f(x1, y1, 0.0)
    glVertex3f( x2, y2, 0.0)
    glVertex3f(x3, y3, 0.0)
    glVertex3f(x4, y4, 0.0)
    
    glEnd()
    glFlush()


def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60,0,0,2)

def main():

    glutInit(sys.argv)

    glutInitDisplayMode(GLUT_RGBA | GLUT_SINGLE)
    
    glutInitWindowSize(800,600)
    
    glutCreateWindow("A Basic OpenGL Template with GLUT")
    glClearColor(1.0,1.0,0.0,0.0)
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)


    glutMainLoop()



if __name__ == "__main__":

    main()