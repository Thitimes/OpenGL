import sys

from OpenGL.GL import *

from OpenGL.GLU import *

from OpenGL.GLUT import *

from math import pi, sin, cos

x1 = -0.2
x2 = 0.2
x3 = 0.2
x4 = -0.2
y1 = -0.2
y2 = -0.2
y3 = 0.2
y4 = 0.2

def display():

    #eye_pos = (0,0,2)
    #aimTo = (0,0,1)
    #gluLookAt(*eye_pos, *aimTo, 0, 1, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    eye_pos = (0,0,2)
    Il = (1,1,1)
    eye_at = (0,0,1)

   # gluLookAt(*eye_pos, *eye_at, 0, 1, 0)

    #light_ambient = [1.0, 1.0, 1.0, 1.0]
    #glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)

    #light_dif = [1.0, 1.0, 1.0, 1.0]
    #glLightfv(GL_LIGHT0, GL_DIFFUSE, light_dif)

    #light_spec = [1.0, 1.0, 1.0, 1.0]
   # glLightfv(GL_LIGHT0, GL_SPECULAR, light_spec)

    #light_pos = [0.2,0.2 ,1]
   # glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
    

    glRotate(30,x1, y1, 0.0)
    glRotate(30,x2, y2, 0.0)
    glRotate(30,x3, y3, 0.0)
    glRotate(30,x4, y4, 0.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glutSolidTeapot(0.75)
    glColor3f(0.0,1.0,1.0)
    glBegin(GL_POLYGON)
    
    glVertex3f(x1, y1, 0.0)
    glVertex3f( x2, y2, 0.0)
    glVertex3f(x3, y3, 0.0)
    glVertex3f(x4, y4, 0.0)
    
    glEnd()
    glFlush()

def keyboard(key, x, y):
    global x1,x2,x3,x4,y1,y2,y3,y4

    key = key.decode("utf-8")
    if key == 'h':
            if(x1 != 0):
                x1 = 0
                x2 = 0
                x3 = 0
                x4 = 0
                y1 = 0
                y2 = 0
                y3 = 0
                y4 = 0
            else:
                x1 = -0.2
                x2 = 0.2
                x3 = 0.2
                x4 = -0.2
                y1 = -0.2
                y2 = -0.2
                y3 = 0.2
                y4 = 0.2


        
       
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
    glutKeyboardFunc(keyboard)

    glutMainLoop()



if __name__ == "__main__":

    main()