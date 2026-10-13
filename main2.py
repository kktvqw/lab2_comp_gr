import numpy as np
from PIL import Image
from math import floor
scale = 5000
#color = np.random.randint(0, 255)
img_mat = np.zeros((1000, 1000, 3), dtype = np.uint8)

zbuf = np.full((1000, 1000), np.inf, dtype = np.float32)

def normal(x0, y0, z0, x1, y1, z1, x2, y2, z2):
    a = [x1 - x2, y1 - y2, z1 - z2] 
    b = [x1 - x0, y1 - y0, z1 - z0]
    return -np.cross(a, b)

def cut(n):
    p = [0, 0, 1]
    return np.dot(n, p) / (np.linalg.norm(n) * np.linalg.norm(p))

def bar_cord(x, y, x0, y0, x1, y1, x2, y2): 
    lambda0 = ((x - x2) * (y1 - y2) - (x1 - x2) * (y - y2)) / ((x0 - x2) * (y1 - y2) - (x1 - x2) * (y0 - y2))
    lambda1 = ((x0 - x2) * (y - y2) - (x - x2) * (y0 - y2)) / ((x0 - x2) * (y1 - y2) - (x1 - x2) * (y0 - y2))
    lambda2 = 1.0 - lambda0 - lambda1
    return lambda0, lambda1, lambda2

def make_triangle(x0, y0, z0, x1, y1, z1, x2, y2, z2):
    #color = np.random.randint(0, 255)
    xmin = int(min(x0, x1, x2))
    if(xmin < 0): xmin = 0

    ymin = int(min(y0, y1, y2))
    if(ymin < 0): ymin = 0

    xmax = int(max(x0, x1, x2))+1
    if(xmax > 1000): xmax = 1000
    ymax = int(max(y0, y1, y2))+1
    if(ymax > 1000): ymax = 1000

    for x in range(xmin, xmax):
        for y in range(ymin, ymax):
            bc0, bc1, bc2 = bar_cord(x + 0.5, y + 0.5, x0, y0, x1, y1, x2, y2)
            if(bc0 >= 0 and bc1 >= 0 and bc2 >= 0):
                z = bc0 * z0 + bc1 * z1 + bc2 * z2
                if(z < zbuf[y, x]):
                    zbuf[y, x] = z
                    img_mat[y, x] = [(-255) * cut(normal(x0, y0, z0, x1, y1, z1, x2, y2, z2)), 0, 140]


v = []
f = []
file = open('model.obj')
for s in file:
   spl = s.split()
   if (spl[0] == 'v'):
        v.append([float(spl[1]), float(spl[2]), float(spl[3])])
   elif (spl[0] == 'f'):
        f.append([spl[1].split('/')[0], spl[2].split('/')[0], spl[3].split('/')[0]])

for i in range(len(v)):
    x = v[i][0] * scale + 500
    y = -v[i][1] * scale + 500
    img_mat[int(y), int(x)] = [145, 0, 128]

for i in range(len(f)):
    x0 = v[int(f[i][0]) - 1][0] * scale + 500
    y0 = -v[int(f[i][0]) - 1][1] * scale + 500
    z0 = v[int(f[i][0]) - 1][2] * scale + 500
    x1 = v[int(f[i][1]) - 1][0] * scale + 500
    y1 = -v[int(f[i][1]) - 1][1] * scale + 500
    z1 = v[int(f[i][1]) - 1][2] * scale + 500
    x2 = v[int(f[i][2]) - 1][0] * scale + 500
    y2 = -v[int(f[i][2]) - 1][1] * scale + 500
    z2 = v[int(f[i][2]) - 1][2] * scale + 500

    if(cut(normal(x0, y0, z0, x1, y1, z1, x2, y2, z2)) < 0):
        make_triangle(x0, y0, z0, x1, y1, z1, x2, y2, z2)

img = Image.fromarray(img_mat)
img.save('img.png')
