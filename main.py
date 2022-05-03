from plot import Plot

class Printer:
    def __init__(self, xSize, ySize, zSize):
        # init (printer specific)
        self.xLength = xSize
        self.yLength = ySize
        self.zLength = zSize

        # post-init (file specific)
        self.fileLines = []
        self.filePath  = ""

        self.innerDenstiy = 3
        self.outerDensity = 3

        # read
        self.faces    = []
        self.vertices = []
                
        # generate
        self.generatedFaces    = []
        self.generatedVertices = []

        self.outerSamplePoints = []

        # execution
        self.position = [0, 0, 0]
    
    def print(self, filePath, innerDenstiy, outerDensity):
        # init
        self.filePath     = filePath
        self.innerDenstiy = innerDenstiy
        self.outerDensity = outerDensity
        # utils
        self.minPoint = self.getMinPoint()
        # reading and modifying data
        self.readData()
        self.trimData()
        self.formatFacesValue()
        self.normalizeData()
        # utils
        self.minPoint = self.getMinPoint()
        self.maxPoint = self.getMaxPoint()
        # generate support structures
        self.generateInnerSupport()
        self.generateOuterSupport()

    # utils
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

    def getHexPoints(self, X, Y, C):
        hexPoints= [[ 0.0 + X,  (C) + Y, 0],
                    [ 0.0 + X, -(C) + Y, 0],
                    [ (3 * C)**0.5 / 2 + X,  (C) / 2 + Y, 0],
                    [ (3 * C)**0.5 / 2 + X, -(C) / 2 + Y, 0],
                    [-(3 * C)**0.5 / 2 + X,  (C) / 2 + Y, 0],
                    [-(3 * C)**0.5 / 2 + X, -(C) / 2 + Y, 0]]
        return hexPoints

    # reading and modifiying data
    def readData(self):
        with open(self.filePath, 'r') as context:
            self.fileLines = context.readlines()

    def trimData(self):
        whiteSpace = ' '
        for line in self.fileLines:
            lineAsArray = line.split(whiteSpace)
            self.formatData(lineAsArray)

    def formatData(self, lineAsArray):
        lineKey    = lineAsArray[0]
        lineValues = self.tempAppendData(lineAsArray[1:])

        if lineKey == 'v':
            self.vertices.append(tempArray)

        elif lineKey == 'f':
            self.faces.append(tempArray)

    def tempAppendData(self, array):
        returnArray = []
        for values in array:
            returnArray.append(float(values))
        return returnArray

    def formatFacesValue(self):
        for faceIndex in range(len(self.faces)):
            for verticeIndex in range(len(self.faces[faceIndex])):
                self.faces[faceIndex][verticeIndex] = int(self.faces[faceIndex][verticeIndex]) - 1

    def normalizeData(self):
        for verticeIndex in range(len(self.vertices)):
            self.vertices[verticeIndex][0] -= self.minPoint[0]
            self.vertices[verticeIndex][1] -= self.minPoint[1]
            self.vertices[verticeIndex][2] -= self.minPoint[2]

    # generate support structure
    # inner
    def generateInnerSupport(self):
        pass

    # outer
    def generateOuterSupport(self):
        rootPoints = self.generateSamplePoints()

    def generateOuterRootPoints(self):
        pass


def main():
    plot    = Plot()
    printer = Printer(1000, 1000, 1000)

    printer.print('./objects/cube.obj', innerDenstiy=3, outerDensity=3)

    plot.plotVertices(printer.samplePoints, subplot=1)
    plot.plotSurface(printer.vertices, printer.faces, subplot=0)  
    plot.plotMesh(printer.vertices, printer.faces, subplot=1)  
    plot.show()

if __name__ == '__main__':
    main()