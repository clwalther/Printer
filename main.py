# libaraires only for dev purposes
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri    as mtr
from mpl_toolkits.mplot3d import Axes3D

class Printer:
    def __init__(self, xSize, ySize, zSize):
        self.fileLines = []
        self.filePath  = ""

        self.faces    = []
        self.vertices = []

        self.samplePoints = []

        self.generatedFaces    = []
        self.generatedVertices = []
        
        self.xLength = xSize
        self.yLength = ySize
        self.zLength = zSize

        self.position = [0, 0, 0]
    
    def print(self, filePath):
        # reading and modifying data
        self.read(filePath)
        self.trimData()
        self.decreaseFacesValue()
        self.normalizeData()
        # generate support structures
        self.generateInnerSupport()
        self.generateOuterSupport(3)

    # reading and modifiying data
    def read(self, filePath):
        with open(filePath, 'r') as context:
            self.fileLines = context.readlines()
    
    def trimData(self):
        whiteSpace = ' '
        for line in self.fileLines:
            lineAsArray = line.split(whiteSpace)
            self.formatData(lineAsArray)
            
    def formatData(self, lineAsArray):
        lineKey    = lineAsArray[0]
        lineValues = lineAsArray[1:]

        if lineKey == 'v':
            tempArray = self.tempAppendData(lineValues)
            self.vertices.append(tempArray)

        elif lineKey == 'f':
            tempArray = self.tempAppendData(lineValues)
            self.faces.append(tempArray)

    def tempAppendData(self, lineValues):
        tempArray = []
        for values in lineValues:
            tempArray.append(float(values))
        return tempArray

    def decreaseFacesValue(self):
        for faceIndex in range(len(self.faces)):
            for verticeIndex in range(len(self.faces[faceIndex])):
                self.faces[faceIndex][verticeIndex] -= 1

    def normalizeData(self):
        minPoint = self.getMinPoint()
        self.resetPoints(minPoint)
    
    def getMinPoint(self):
        minPoint = [self.vertices[0][0], self.vertices[0][1], self.vertices[0][2]]

        for point in self.vertices:
            minPoint[0] = min(minPoint[0], point[0])
            minPoint[1] = min(minPoint[1], point[1])
            minPoint[2] = min(minPoint[2], point[2])
        return minPoint

    def getMaxPoint(self):
        maxPoint = [self.vertices[0][0], self.vertices[0][1], self.vertices[0][2]]

        for point in self.vertices:
            maxPoint[0] = max(maxPoint[0], point[0])
            maxPoint[1] = max(maxPoint[1], point[1])
            maxPoint[2] = max(maxPoint[2], point[2])
        return maxPoint

    def resetPoints(self, minPoint):
        for verticeIndex in range(len(self.vertices)):
            self.vertices[verticeIndex][0] -= minPoint[0]
            self.vertices[verticeIndex][1] -= minPoint[1]
            self.vertices[verticeIndex][2] -= minPoint[2]

    # generate support structure
    def generateInnerSupport(self):
        pass

    def generateOuterSupport(self, density):
        maxPoint = self.getMaxPoint()
        samplePoints = self.generateSamplePoints(maxPoint, density)
        self.appendSamplePoints(samplePoints, density)

    def generateSamplePoints(self, maxPoint, density):
        samplePoints = []
        xValue = 0
        while xValue <= maxPoint[0]:
            yValue = 0
            while yValue <= maxPoint[1]:
                samplePoints.append((xValue, yValue))
                yValue += density * 3
            xValue += (3 * density)**0.5
        return samplePoints

    def appendSamplePoints(self, samplePoints, density):
        for point in samplePoints:
            hexPoints = self.getHexPoints(point[0], point[1], density)
            hexPoints = self.trimSampleInsert(hexPoints)
            self.samplePoints.extend(hexPoints)

    def getHexPoints(self, x, y, c):
        hexPoints= [[ 0.0 + x,  (c) + y, 0],
                    [ 0.0 + x, -(c) + y, 0],
                    [ (3 * c)**0.5 / 2 + x,  (c) / 2 + y, 0],
                    [ (3 * c)**0.5 / 2 + x, -(c) / 2 + y, 0],
                    [-(3 * c)**0.5 / 2 + x,  (c) / 2 + y, 0],
                    [-(3 * c)**0.5 / 2 + x, -(c) / 2 + y, 0]]
        return hexPoints
    
    def trimSampleInsert(self, listPoints):
        index = 0
        while index < len(listPoints):
            if listPoints[index] in self.samplePoints:
                listPoints.pop(index)
            else:
                index += 1
        return listPoints


# only for development
class Plot:
    def __init__(self):
        self.figure    = plt.figure(figsize=plt.figaspect(0.5))
        self.subplot = []

        self.subplot.append(self.figure.add_subplot(1, 2, 1, projection='3d'))
        self.subplot.append(self.figure.add_subplot(1, 2, 2, projection='3d'))

    def plotVertices(self, vertices, subplot=0):
        for vertice in vertices:
            self.subplot[subplot].plot(vertice[0], vertice[1], vertice[2], 'X')

    def plotMesh(self, vertices, faces, subplot=0):
        for face in faces:
            vertices = np.array(face)
            xValue = vertices[:,0].append(vertices[0])
            yValue = vertices[:,1].append(vertices[1])
            zValue = vertices[:,2].append(vertices[2])
            self.subplot[subplot].plot(xValue, yValue, zValue)

    def plotSurface(self, vertices, faces, subplot=0):
        vertices = np.array(vertices)
        triang = mtr.Triangulation(vertices[:,0], vertices[:,1], triangles=faces)
        self.subplot[subplot].plot_trisurf(triang, vertices[:,2])
    
    def show(self):
        plt.show()

def main():
    plot    = Plot()
    printer = Printer(1000, 1000, 1000)

    printer.print('./objects/cube.obj')

    plot.plotVertices(printer.samplePoints, subplot=1)
    plot.plotSurface(printer.vertices, printer.faces, subplot=0)  
    plot.plotMesh(printer.generatedVertices, printer.generatedFaces, subplot=1)  
    plot.show()

if __name__ == '__main__':
    main()