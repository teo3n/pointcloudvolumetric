import math
import numpy as np

PI = 3.14159

def transform(m, v):
    return np.asarray(m * np.asmatrix(v).T)[:,0]

def magnitude(v):
    x, y, z = v
    return math.sqrt(np.sum(np.power(v, 2)))

def normalize(v):
    m = magnitude(v)
    if m == 0:
        return v
    return np.divide(v, m)

def identity():
    return np.matrix([[1.0, 0.0, 0.0, 0.0],
                     [0.0, 1.0, 0.0, 0.0],
                     [0.0, 0.0, 1.0, 0.0],
                     [0.0, 0.0, 0.0, 1.0]])

def orbit(th, phi, r):
    xp = r * math.sin(th) * math.cos(phi)
    # yp = r * math.sin(th) * math.sin(phi)
    yp = r * math.sin(phi)
    zp = r * math.cos(th)

    return xp, yp, zp

def ortho(l, r, b, t, n, f):
    dx = r - l
    dy = t - b
    dz = f - n
    rx = -(r + l) / (r - l)
    ry = -(t + b) / (t - b)
    rz = -(f + n) / (f - n)
    return np.matrix([[2.0/dx,0,0,rx],
                      [0,2.0/dy,0,ry],
                      [0,0,-2.0/dz,rz],
                      [0,0,0,1]])

def perspective(fovy, aspect, n, f):
    s = 1.0/math.tan(math.radians(fovy)/2.0)
    sx, sy = s / aspect, s
    zz = (f+n)/(n-f)
    zw = 2*f*n/(n-f)
    return np.matrix([[sx,0,0,0],
                      [0,sy,0,0],
                      [0,0,zz,zw],
                      [0,0,-1,0]])

def frustum(x0, x1, y0, y1, z0, z1):
    a = (x1+x0)/(x1-x0)
    b = (y1+y0)/(y1-y0)
    c = -(z1+z0)/(z1-z0)
    d = -2*z1*z0/(z1-z0)
    sx = 2*z0/(x1-x0)
    sy = 2*z0/(y1-y0)
    return np.matrix([[sx, 0, a, 0],
                      [ 0,sy, b, 0],
                      [ 0, 0, c, d],
                      [ 0, 0,-1, 0]])

def translate(xyz):
    x, y, z = xyz
    return np.matrix([[1,0,0,x],
                      [0,1,0,y],
                      [0,0,1,z],
                      [0,0,0,1]])

def scale(xyz):
    x, y, z = xyz
    return np.matrix([[x,0,0,0],
                      [0,y,0,0],
                      [0,0,z,0],
                      [0,0,0,1]])

def sincos(a):
    a = math.radians(a)
    return math.sin(a), math.cos(a)

def rotate(a, xyz):
    x, y, z = normalize(xyz)
    #x, y, z = xyz
    s, c = sincos(a)
    nc = 1 - c
    return np.matrix([[x*x*nc +   c, x*y*nc - z*s, x*z*nc + y*s, 0],
                      [y*x*nc + z*s, y*y*nc +   c, y*z*nc - x*s, 0],
                      [x*z*nc - y*s, y*z*nc + x*s, z*z*nc +   c, 0],
                      [           0,            0,            0, 1]])

def rotx(a):
    s, c = sincos(a)
    return np.matrix([[1,0,0,0],
                      [0,c,-s,0],
                      [0,s,c,0],
                      [0,0,0,1]])

def roty(a):
    s, c = sincos(a)
    return np.matrix([[c,0,s,0],
                      [0,1,0,0],
                      [-s,0,c,0],
                      [0,0,0,1]])

def rotz(a):
    s, c = sincos(a)
    return np.matrix([[c,-s,0,0],
                      [s,c,0,0],
                      [0,0,1,0],
                      [0,0,0,1]])

def lookat(eye, target, up):
    F = target[:3] - eye[:3]
    f = normalize(F)
    U = normalize(up[:3])
    s = np.cross(f, U)
    u = np.cross(s, f)
    M = np.matrix(np.identity(4))
    M[:3,:3] = np.vstack([s,u,-f])
    T = translate(-eye)
    return M * T

def viewport(x, y, w, h):
    x, y, w, h = map(float, (x, y, w, h))
    return np.matrix([[w/2, 0  , 0,x+w/2],
                      [0  , h/2, 0,y+h/2],
                      [0  , 0  , 1,    0],
                      [0  , 0  , 0,    1]])


def fpscam(eye, pitch, yaw):
    pitch = math.degrees(pitch)
    yaw = math.degrees(yaw)
    cosPitch = math.cos(pitch)
    sinPitch = math.sin(pitch)
    cosYaw = math.cos(yaw)
    sinYaw = math.sin(yaw)

    xAxis = [cosYaw, 0, -sinYaw]
    yAxis = [sinYaw * sinPitch, cosPitch, cosYaw * sinPitch]
    zAxis = [sinYaw * cosPitch, -sinPitch, cosPitch * cosYaw]

    return np.matrix([
        [xAxis[0], yAxis[0], zAxis[0], 0],
        [xAxis[1], yAxis[1], zAxis[1], 0],
        [xAxis[2], yAxis[2], zAxis[2], 0],
        [-np.dot(xAxis, eye), -np.dot(yAxis, eye), -np.dot(zAxis, eye), 1]])
