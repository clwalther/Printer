# only for development
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri    as mtr
from mpl_toolkits.mplot3d import Axes3D
import datetime

class Plot:
    def __init__(self):
        self.figure = plt.figure(figsize=plt.figaspect(0.5))
        self.subplot = []

        self.subplot.append(self.figure.add_subplot(1, 2, 1, projection='3d'))
        self.subplot.append(self.figure.add_subplot(1, 2, 2, projection='3d'))

    def vertices(self, vertices, subplot=0):
        for vertice in vertices:
            self.subplot[subplot].plot(vertice[0], vertice[1], vertice[2], 'X')
    
    def line(self, vertices, subplot=0):
        vertices = np.array(vertices)
        self.subplot[subplot].plot(vertices[:,0], vertices[:,1], vertices[:,2])

    def mesh(self, vertices, faces, subplot=0):
        for face in faces:
            pathX = []
            pathY = []
            pathZ = []
            for vertice in face:
                pathX.append(vertices[vertice][0])
                pathY.append(vertices[vertice][1])
                pathZ.append(vertices[vertice][2])
            pathX.append(pathX[0])
            pathY.append(pathY[0])
            pathZ.append(pathZ[0])
            self.subplot[subplot].plot(pathX, pathY, pathZ)

    def surface(self, vertices, faces, subplot=0):
        vertices = np.array(vertices)
        triang = mtr.Triangulation(vertices[:,0], vertices[:,1], triangles=faces)
        self.subplot[subplot].plot_trisurf(triang, vertices[:,2])
    
    def show(self):
        plt.show()

class Timer:
    def __init__(self):
        self.timestamps = []

    def start(self):
        self.firstCheckpoint = datetime.datetime.today()
        self.prevCheckpoint  = datetime.datetime.today()

    def checkpoint(self):
        currCheckpoint = datetime.datetime.today()
        delta = currCheckpoint - self.prevCheckpoint
        print(delta)
        delta = currCheckpoint - self.firstCheckpoint
        self.timestamps.append(delta)
        self.prevCheckpoint = datetime.datetime.today()

    def printTimestamps(self):
        for timestamp in self.timestamps:
            print(timestamp)