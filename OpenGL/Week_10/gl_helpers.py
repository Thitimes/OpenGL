from numpy import array, ndarray, zeros, dot, cross, float32, identity
from numpy.linalg import norm
from math import sqrt, sin, cos, tan, acos, pi

def Identity():
    return array(((1, 0, 0, 0),
                  (0, 1, 0, 0),
                  (0, 0, 1, 0),
                  (0, 0, 0, 1)), dtype=float32)

def normalize(v):
    l = norm(v)
    if l == 0:
        return v
    else:
        return v/l

def Translate(tx, ty, tz):
    # Fix me!
    return array(((1, 0, 0, tx),
                  (0, 1, 0, ty),
                  (0, 0, 1, tz),
                  (0, 0, 0, 1)), dtype=float32)

def Scale(sx, sy, sz):
    # Fix me!
    return array(((sx, 0, 0, 0),
                  (0, sy, 0, 0),
                  (0, 0, sz, 0),
                  (0, 0, 0, 1)), dtype=float32)

def Rotate(angle, x, y, z):
    # Fix me!
    c = cos((angle/180)*pi)
    s = sin((angle/180)*pi)
    x2 = pow(x,2)
    y2 = pow(y,2)
    z2 = pow(z,2)
    return array(((((x2*(1-c))+c), (((x*y)*(1-c))-(z*s)), (((x*z)*(1-c)) + (y*s)), 0),
                  (((y*x)*(1-c)+(z*s)), ((y2*(1-c))+c), (((y*z)*(1-c))-(x*s)), 0),
                  ((((z*x)*(1-c))-(y*s)), (((z*y)*(1-c))+(x*s)), ((z2*(1-c))+c), 0),
                  (0, 0, 0, 1)), dtype=float32)

def LookAt(eyex, eyey, eyez, atx, aty, atz, upx, upy, upz):
    # Fix me!
    eye = array((eyex,eyey,eyez)) 
    at = array((atx,aty,atz))
    up = array((upx,upy, upz))
    nZ = normalize(eye - at)
    nY = normalize(up)
    nX = normalize(cross(nY,nZ))
    nY = normalize(cross(nZ,nX))
    return array(((nX[0], nX[1], nX[2], -dot(nX,eye)),
                  (nY[0], nY[1], nY[2], -dot(nY,eye)),
                  (nZ[0], nZ[1], nZ[2], -dot(nZ,eye)),
                  (0, 0, 0, 1)), dtype=float32)

def Perspective(fovy, aspect, zNear, zFar):
    # Fix me!
    return array(((1/tan(((fovy/180)*pi)/2)/aspect, 0, 0, 0),
                  (0, (1/tan(((fovy/180)*pi)/2)), 0, 0),
                  (0, 0, -(zFar+zNear)/(zFar-zNear), (-2*zNear*zFar)/(zFar-zNear)),
                  (0, 0, -1, 0)), dtype=float32)

def Frustum(left, right, bottom, top, near, far):
    # Fix me!
    return array((((2*near)/(right-left), 0, (right+left)/(right-left), 0),
                  (0, (2*near)/(top-bottom), (top+bottom)/(top-bottom), 0),
                  (0, 0, -((far+near)/(far-near)), (2*far*near)/(far-near)),
                  (0, 0, 0, 1)), dtype=float32)

def Ortho(left, right, bottom, top, near, far):
    # Fix me!
    return array(((2/(right-left), 0, 0, -((right+left)/(right-left))),
                  (0, 2/(top/bottom), 0, -((top+bottom)/(top-bottom))),
                  (0, 0, -2/(far-near),-((far+near)/(far-near)) ),
                  (0, 0, 0, 1)), dtype=float32)