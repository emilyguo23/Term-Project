
import random, math
from cmu_112_graphics import *
import numpy as np
import scipy.spatial

# This file contains all functions used to calculate random/flat terrain

#############################################
# Diamond-square algorithm for terrain generation
# citations : 
# https://www.morganmckinley.com/ie/article/learn-python-part-2-diamond-square-algorithm
# https://scipython.com/blog/cloud-images-using-the-diamond-square-algorithm/ 
#############################################

def generateHeights(n, scale = 1):
    # initialize constants
    # N = edge length of square array
    N = pow(2, n) + 1
    side = N - 1
    nSquares = 1

    # initialize array, random numbers in 4 corners
    # Note: Using np array instead of 2D list since 2D lists don't 
    # support 'vectorized' operations
    matrix = np.zeros((N, N))
    matrix[0::N-1, 0::N-1] = np.random.uniform(-1, 1, (2,2))
    
    # execute diamond-square operations until entire array is filled
    while (side > 1):
        side2 = side // 2
        # Diamond step --> gets mean of neighboring square plus a random value
        for ix in range(nSquares):
            for iy in range(nSquares):
                x0, x1 = ix * side, (ix + 1) * side, 
                y0, y1 = iy * side, (iy + 1) * side
                xc, yc = x0 + side2, y0 + side2
                matrix[yc, xc] = (matrix[y0, x0] + matrix[y0, x1] + 
                                    matrix[y1, x0] + matrix[y1, x1])/4
                matrix[yc, xc] += scale * np.random.uniform(-1,1)
        
        # Square step --> gets mean of neighboring diamond plus a random value
        for iy in range(2 * nSquares + 1):
            yc = side2 * iy
            for ix in range(nSquares + 1):
                xc = side * ix + side2 * (1 - iy % 2)
                if not (0 <= xc < N and 0 <= yc < N): # check if out of range
                    continue
                tot, ntot = 0., 0
                # only 3 neighbors at edges
                for (dx, dy) in ((-1,0), (1,0), (0,-1), (0,1)):
                    xs, ys = xc + dx * side2, yc + dy * side2
                    if not (0 <= xs < N and 0 <= ys < N): # check if out of range
                        continue
                    else:
                        tot += matrix[ys, xs]
                        ntot += 1
                matrix[yc, xc] += tot / ntot + scale * np.random.uniform(-1,1)
        side = side2
        nSquares *= 2
        scale /= 2 # after each iteration, magnitude of random value reduced
    return matrix


# returns n x n 2D list
def samplePoints(array, n):
    sample = []
    jump = len(array)//n # samples evenly distribution of points
    for i in range(0, len(array), jump):
        sample.append(array[i][::jump])
    return sample


#############################################
# Plotting points in isometric view
# Modified from : 15-112 #3DGraphicsDemo Code; TA-led mini lecture
#############################################

# calculates 3D vector (x,y,z) equivalent of tkinter coordinates 
def graph2Vecs(app, graph, z=0): 
    # takes in 2d ndarray of TKinter coordinates [x,y]
    # returns a 2d ndarray of vecs [x,y,z]
    ox, oy = app.origin
    vecs = np.empty((0,3))
    # matrix A 
    A = np.array([[math.cos(app.xAxisAngle), math.cos(app.yAxisAngle)],
                  [math.sin(app.xAxisAngle), math.sin(app.yAxisAngle)]])
    Ainv = np.linalg.inv(A)
    for point in graph: 
        # first adjust points
        x = point[0] - ox #x coord in graph (centered at 0,0)
        y = oy - point[1] #y coord in graph (centered at 0,0)
        # vector b 
        b = np.array([x,y])
        # vector v = [x  y  z]
        v = Ainv @ b
        v = np.append(v, z) #add on z coord 
        vecs = np.append(vecs, [v], axis=0)
    return vecs

# Rotate a vector in 3D space around an axis 
def rotateVec(app, vec, angle, axis): 
    # Rotation matrix adapted from 
    # https://developer.mozilla.org/en-US/docs/Web/CSS/transform-function/rotate3d()
    if angle % 360 == 0:
        return vec 
    a = deg2Rad(angle)
    x,y,z = axis[0], axis[1], axis[2] 
    # First row
    r11 = 1 + (1-math.cos(a))*(x**2 - 1)
    r12 = z*math.sin(a) + x*y*(1-math.cos(a))
    r13 = -y*math.sin(a) + x*z*(1-math.cos(a))
    # Second row 
    r21 = -z*math.sin(a) + x*y*(1-math.cos(a))
    r22 = 1 + (1-math.cos(a))*(y**2 - 1)
    r23 = x*math.sin(a) + y*z*(1-math.cos(a))
    # Third row 
    r31 = y*math.sin(a) + x*z*(1-math.cos(a))
    r32 = -x*math.sin(a) + y*z*(1-math.cos(a))
    r33 = 1 + (1-math.cos(a))*(z**2 - 1)
    # Rotation matrix 
    R = np.array([[r11, r12, r13], 
                  [r21, r22, r23],
                  [r31, r32, r33]])
    rotatedVec = R @ vec
    return rotatedVec

# converts degrees to radians
def deg2Rad(deg): return deg * math.pi/180

# regular graph coordinate (with origin at 0,0) --> tkinter x coordinate
def g2x(x, originX): return x + originX

# regular graph coordinate (with origin at 0,0) --> tkinter y coordinate
def g2y(y, originY): return originY - y

#############################################
# Terrain Display
#############################################
# Modified rotate() function from 3DGraphicsDemo
def rotate(app, vecs, angle, rotAxis = (0,0,1)):
    newPoints = np.empty((0,3))
    for i in range(vecs.shape[0]):
        vector = vecs[i]
        if vector[0] == vector[1] == vector[2] == 0:
            rotatedVec = vector
        else:
            rotatedVec = rotateVec(app, vector, angle, rotAxis)
        newPoints = np.append(newPoints, [rotatedVec], axis = 0)
    vecs = newPoints
    return vecs

# [x, y, z] to [x, y]
# modified vecs2Graph from 3DGraphicsDemo
def vecs2Graph(app, vectorList): 
    graphPoints = np.empty((0,2))
    for vector in vectorList: 
        x, y, z = vector[0], vector[1], vector[2]
        # cosine gets x-components of vector, sine gets y-components
        newX = x*math.cos(app.xAxisAngle) + y*(math.cos(app.yAxisAngle))
        newY = (x*math.sin(app.xAxisAngle) 
            + y*(math.sin(app.yAxisAngle)) + z)
        # recenter around origin 
        newX = g2x(newX, app.origin[0])
        newY = g2y(newY, app.origin[1])
        newPoint = np.array([[newX, newY]])
        graphPoints = np.append(graphPoints, newPoint, axis = 0)
    return graphPoints

# modified graph2Vecs from 3DGraphicsDemo
# calculates 3D vector (x,y,z) equivalent of tkinter coordinates 
def graph2Point(app, point, z=0): 
    # takes in single 2d ndarray of TKinter coordinates [x,y]
    # returns a single 2d ndarray vector [x,y,z]
    ox, oy = app.origin
    vector = np.empty((0,3))
    # matrix A 
    A = np.array([[math.cos(app.xAxisAngle), math.cos(app.yAxisAngle)],
                  [math.sin(app.xAxisAngle), math.sin(app.yAxisAngle)]])
    Ainv = np.linalg.inv(A) 
    # first adjust points
    x = point[0] - ox #x coord in graph (centered at 0,0)
    y = oy - point[1] #y coord in graph (centered at 0,0)
    # vector b 
    b = np.array([x,y])
    # vector v = [x  y  z]
    v = Ainv @ b
    v = np.append(v, z) #add on z coord 
    vector = np.append(vector, [v], axis=0)
    return vector


#############################################
# Model
#############################################

# creates array of all [x,y,z] points to be plotted
def createPoints(app, origin):
    if app.upload == True: pass
    else:
        heights = samplePoints(app.heights, app.n)
        jump = 0.8*app.height//app.n
        points = []
        startX, startY = -app.scale*2, -app.scale*2
        for row in range(app.n + 1):
            for col in range(app.n):
                x, y = startX + (row * jump), startY + (col * jump)
                z = heights[row][col] * app.scale
                points.append([x,y,z])
        points = np.array(points)
        for i in range(points.shape[0]):
            points[i] = points[i] + np.array(origin)
        return(points)

class Polygon(object):
    def __init__(self, coords):
        self.coords = coords
        self.color = None
        self.altitude = None
        self.level = None
        self.indexes = None
    def setColor(self, color = None):
        self.color = color
    def setAltitude(self, zVal):
        self.altitude = zVal
    def setLevel(self, level):
        self.level = level

def createPolygons(app, vectorXY):
    polyList = []
    for row in range(len(vectorXY) - app.n):
        if row != len(vectorXY) - app.n - 1:
            if ((row + 1) % app.n != 0):
                x0, y0 = vectorXY[row]
                x1, y1 = vectorXY[row + 1]
                x3, y3 = vectorXY[row + app.n]
                x2, y2 = vectorXY[row + app.n + 1]
                coords = [(x0, y0), (x1, y1), (x2, y2), (x3, y3)]
                polygon = Polygon(coords)
                polygon.indexes = [row, row + 1, row + app.n + 1, row + app.n]
                polyList.append(polygon)
    return polyList

# takes in array of 2D points, returns index of nearest array value using k-dimensional trees
def nearestPoint(array, point):
    tree = scipy.spatial.cKDTree(array)
    dist, index = tree.query(point)
    return index

def dist(x0, y0, x1, y1):
    dist = math.sqrt((x1 - x0)**2 + (y1 - y0)**2)
    return dist

def distanceList(app, polygonList, pointsList):
    altList = np.zeros((len(polygonList), 2))
    for i in range(len(polygonList)):
        polygon = polygonList[i]
        index1, index2, index3, index4 = polygon.indexes
        coord1 = pointsList[index1]
        coord2 = pointsList[index2]
        coord3 = pointsList[index3]
        coord4 = pointsList[index4]
        zVal = (coord1[2] + coord2[2] + coord3[2] + coord4[2])/4
        altList[i] = np.array((zVal, i))
    sortedIndex = np.lexsort((altList[:,1],altList[:,0]))
    altList = altList[sortedIndex]
    return altList

#############################################
# View
#############################################

def drawAxes(app, canvas):
    ox, oy = app.origin
    for px, py in app.axesPoints:
        canvas.create_line(ox,oy,px,py, fill = 'red')

def highlightVertex(app, canvas, vectorXY):
    if app.highlightedVertex == None: return
    index = app.highlightedVertex
    [x, y] = vectorXY[index].tolist()
    offset = 6
    x0, x1 = x - offset, x + offset
    y0, y1 = y - offset, y + offset
    if app.multiselect == True:
        fill = 'blue'
    else: fill = 'red'
    if x0 <= app.mouseX <= x1 and y0 <= app.mouseY <= y1:
        canvas.create_oval(x0,y0,x1,y1, fill = fill, outline = 'white')

def drawPolygons(app, canvas, polygonList, pointsList):
    sortedList = distanceList(app, polygonList, pointsList)
    for i in range(len(sortedList)):
        index = int(sortedList[i][1])
        polygon = polygonList[index]
        v1, v2, v3, v4 = polygon.coords
        if polygon.color != None:
            color = polygon.color
        else: color ='#edf6f9'
        canvas.create_polygon(v1, v2, v3, v4, fill = color, 
                                outline = '#6c757d', width = 0.1)

def printText(app, canvas):
    if app.mode == 'terrainMode' or app.mode == 'flatMode':
        canvas.create_text(app.width//2, app.height - 90,
                            text = """Hover over a vertex to select. Once red/blue circle appears, click and drag to edit!""", 
                            font = "Avenir 20")
        canvas.create_text(app.width//2, app.height - 60,
                            text = """Press Tab to toggle multi-select mode. Press "h" and "q" for additional help.""", 
                            font = "Avenir 20")
    if app.mode == 'colorMode':
        canvas.create_text(app.width - 150, 55,
        text = """Press "q" for additional help.\nPress "c" for color references.""", 
        font = "Avenir 20")
        canvas.create_text(400, 125, 
        text = "To un-select altitude level, hit Enter.",
        font = 'Avenir 20')
    if app.mode == 'finishMode':
        font = 'Avenir 30'
        canvas.create_text(app.width/2, 75, 
                    text="""Complete!""", font = 'Avenir 60')
        canvas.create_text(app.width/2, 130, 
                    text="""Save or start again!""", font = font, fill = 'blue2')

def drawMultiselectToggle(app, canvas):
    if app.multiselect == True:
        color = 'DeepSkyBlue2'
        text = 'MultiSelect ON'
    elif app.multiselect == False:
        color = 'IndianRed1'
        text = 'MultiSelect OFF'
    canvas.create_rectangle(50, 50, 210, 100, fill = color, width = 3)
    canvas.create_text(130, 75, text = text, font = "Avenir 20", fill = 'white')


#############################################
# Flat Points
#############################################

def createFlatPoints(app, origin):
    jump = app.height//app.n
    points = []
    startX, startY = -app.scale*2, -app.scale*2
    for row in range(app.n + 1):
        for col in range(app.n):
            x, y = startX + (row * jump), startY + (col * jump)
            z = 0
            points.append([x,y,z])
    points = np.array(points)
    for i in range(points.shape[0]):
        points[i] = points[i] + np.array(origin)
    return(points)

