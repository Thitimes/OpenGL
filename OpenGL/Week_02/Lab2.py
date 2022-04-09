import sys

from OpenGL.GL import *

from OpenGL.GLU import *

from OpenGL.GLUT import *

from math import pi, sin, cos

def display():


    
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0.0,1.0,1.0)
    glBegin(GL_POLYGON)
    glVertex3f(-0.5, -0.5, 0.0)
    glVertex3f( 0.5, -0.5, 0.0)
    glVertex3f( 0.5, 0.5, 0.0)
    glVertex3f(-0.5, 0.5, 0.0)
    glEnd()
    glBegin(GL_POLYGON)
    glColor3f(1.0,1.0,0.0)
    for i in range(256):
        theta = 2 * pi * i / 256
        x = 0.3 * cos(theta)
        y = 0.3 * sin(theta)
        glVertex2f(x, y)
    glEnd()
    glFlush()



def main():

    glutInit(sys.argv)

    glutInitDisplayMode(GLUT_RGBA | GLUT_SINGLE)
    
    glutInitWindowSize(800,800)
    
    glutCreateWindow("A Basic OpenGL Template with GLUT")
    glClearColor(1.0,1.0,0.0,0.0)

    glutDisplayFunc(display)



    glutMainLoop()



if __name__ == "__main__":

    main()