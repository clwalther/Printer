from plot import Plot

class Printer:
    def __init__(self, xSize, ySize, zSize):
        # init (printer specific)
        self.xLength = xSize
        self.yLength = ySize
        self.zLength = zSize

        # post-init (file specific)
        self.filePath  = ""

        self.innerDenstiy = 3
        self.outerDensity = 3

        self.pillarCompHeight = 0.6
        self.pillarRadius = 0.4

        # read
        self.fileLines = []
        self.faces     = []
        self.vertices  = []

        # generate
        self.generatedFaces    = []
        self.generatedVertices = []

        self.outerSamplePoints = {}

        # execution
        self.position = [0, 0, 0]

    def print(self, filePath, innerDenstiy, outerDensity):
        # init
        self.filePath     = filePath
        self.innerDenstiy = innerDenstiy
        self.outerDensity = outerDensity
        # reading and modifying data
        self.readData()
        self.trimData()
        self.formatFacesValue()
        self.minPoint = self.getMinPoint() # utils
        self.normalizeData()
        self.maxPoint = self.getMaxPoint() # utils
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

    # CONSTRUCT AND GENERATE
    def getHexPoints(self, X, Y, Z, C):
        hexPoints= [[ 0.0 + X,  (C) + Y, Z],
                    [ (3)**0.5 * (C) / 2 + X,  (C) / 2 + Y, Z],
                    [ (3)**0.5 * (C) / 2 + X, -(C) / 2 + Y, Z],
                    [ 0.0 + X, -(C) + Y, Z],
                    [-(3)**0.5 * (C) / 2 + X, -(C) / 2 + Y, Z],
                    [-(3)**0.5 * (C) / 2 + X,  (C) / 2 + Y, Z]]
        return hexPoints

    def constructPolygon(self, face, vertices):
        polygon = []
        for vertice in face:
            polygon.append(vertices[vertice])
        return polygon

    # INTERSECTION
    def pointInPolygon(self, POLYGON, POINT):
        odd = False
        POLYGON.append(POLYGON[0])
        for index in range(len(POLYGON)-1):
            if self.checkHeightPointPolygon(POLYGON, POINT, index):
                if self.checkRayIntersectPolygon(POLYGON, POINT, index):
                    odd = not odd
        return odd

    def checkHeightPointPolygon(self, POLYGON, POINT, INDEX):
        return (POLYGON[INDEX][1] <= POINT[1] and POLYGON[INDEX+1][1] > POINT[1]) or (POLYGON[INDEX][1] > POINT[1] and POLYGON[INDEX+1][1] <= POINT[1])

    def checkRayIntersectPolygon(self, POLYGON, POINT, INDEX):
        return POINT[0] < POLYGON[INDEX][0] + ((POINT[1] - POLYGON[INDEX][1]) / (POLYGON[INDEX+1][1] - POLYGON[INDEX][1])) * (POLYGON[INDEX+1][0] - POLYGON[INDEX][0])

    def getPointLineIntersectPlane(self, LINE, POLYGON):
        A, B, C, D = self.getPlaneEqu(POLYGON)
        RESULT     = self.calcIntersectionPlaneLine(LINE, A, B, C, D)
        return RESULT

    def getPlaneEqu(self, POINTS):
        AB = (POINTS[1][0] - POINTS[0][0], POINTS[1][1] - POINTS[0][1], POINTS[1][2] - POINTS[0][2])
        AC = (POINTS[2][0] - POINTS[0][0], POINTS[2][1] - POINTS[0][1], POINTS[2][2] - POINTS[0][2])
    
        a = (AB[1] * AC[2]) - (AC[1] * AB[2])
        b = (AB[2] * AC[0]) - (AC[2] * AB[0])
        c = (AB[0] * AC[1]) - (AC[0] * AB[1])
        d = -(a * POINTS[0][0] + b * POINTS[0][1] + c * POINTS[0][2])
        return a, b, c, d

    def calcIntersectionPlaneLine(self, LINE, A, B, C, D):
        SUM = (-D) - (A * LINE[0][0]) + (B * LINE[0][1]) + (C * LINE[0][2])
        MUL = (A * (LINE[1][0] - LINE[0][0])) + (B * (LINE[1][1] - LINE[0][1])) + (C * (LINE[1][2] - LINE[0][2]))
        if not MUL == 0:
            X = LINE[0][0] + (LINE[1][0] - LINE[0][0]) * SUM / MUL
            Y = LINE[0][1] + (LINE[1][1] - LINE[0][1]) * SUM / MUL
            Z = LINE[0][2] + (LINE[1][2] - LINE[0][2]) * SUM / MUL
            return [X, Y, Z]
        else:
            return -1 # ERROR

    # MODIFY
    def listToStr(self, array):
        string = ""
        for elements in array:
            string += f"{str(elements)};"
        string = string[0:-1]
        return string

    def strToList(self, string, obj):
        array = list(map(obj, string.split(';')))
        return array
    
    def getLineFromRoot(self, root, X, Y, Z):
        vector = [root[0] + X, root[1] + Y, root[2] + Z]
        line   = [root, vector]
        return line
    
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

        if lineKey == 'v':
            lineValues = self.tempAppendData(lineAsArray[1:])
            self.vertices.append(lineValues)

        elif lineKey == 'f':
            lineValues = self.tempAppendData(lineAsArray[1:])
            self.faces.append(lineValues)

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
        rootPoints = self.generateOuterRootPoints()
        self.setOuterSamplePoints(rootPoints)
        self.generateOuterSupportPillars()

    def generateOuterRootPoints(self):
        rootPoints = []
        xValue = 0
        while xValue <= self.maxPoint[0] / 2:
            yValue = 0
            while yValue <= self.maxPoint[1] / 2:
                rootPoints.append([self.maxPoint[0] / 2 + xValue, self.maxPoint[1] / 2 + yValue])
                rootPoints.append([self.maxPoint[0] / 2 + xValue, self.maxPoint[1] / 2 - yValue])
                rootPoints.append([self.maxPoint[0] / 2 - xValue, self.maxPoint[1] / 2 + yValue])
                rootPoints.append([self.maxPoint[0] / 2 - xValue, self.maxPoint[1] / 2 - yValue])
                yValue += self.outerDensity * 3
            xValue += self.outerDensity * (3**0.5)
        return rootPoints

    def setOuterSamplePoints(self, rootPoints):
        for root in rootPoints:
            samplePoints = self.getHexPoints(root[0], root[1], 0, self.outerDensity)
            self.checkOuterSamplePoints(samplePoints)

    def checkOuterSamplePoints(self, samplePoints):
        for point in samplePoints:
            strPoint = self.listToStr(point[0:2])
            if not strPoint in self.outerSamplePoints.keys():
                result = self.getRayIntersectOuterSamplePoints(point)
                if len(result) > 0:
                    self.outerSamplePoints[strPoint] = result

    def getRayIntersectOuterSamplePoints(self, point):
        heights = []
        for face in self.faces:
            polygon   = self.constructPolygon(face, self.vertices)
            isBeneath = self.pointInPolygon(polygon, point)
            if isBeneath:
                line  = self.getLineFromRoot(point, X=0, Y=0, Z=1)
                inter = self.getPointLineIntersectPlane(line, polygon)
                heights.append(inter[2])
        return heights

    def generateOuterSupportPillars(self):
        for keys in self.outerSamplePoints.keys():
            LIST = sorted(self.outerSamplePoints[keys])
            for index in range(1, len(LIST)-2, 2):
                lowerPoint = self.strToList(keys + f";{LIST[index+0]}", float)
                upperPoint = self.strToList(keys + f";{LIST[index+1]}", float)
                self.generateSupportPillar(lowerPoint, upperPoint)
    
    def generateSupportPillar(self, lowerPoint, upperPoint):
        pillarRadius = self.getPillarRadius(lowerPoint, upperPoint)
        upperRingZ   = upperPoint[2] - self.getPillarRingZ(lowerPoint, upperPoint)
        lowerRingZ   = lowerPoint[2] + self.getPillarRingZ(lowerPoint, upperPoint) * self.lowerRingMult(lowerPoint)

        upperRing = self.getHexPoints(lowerPoint[0], lowerPoint[1], upperRingZ, pillarRadius)
        lowerRing = self.getHexPoints(lowerPoint[0], lowerPoint[1], lowerRingZ, pillarRadius)

        lengthGenVertices = len(self.generatedVertices)
        faces = self.generateSupportPillarFaces(lengthGenVertices)

        self.generatedFaces.extend(faces)

        self.generatedVertices.append(lowerPoint)
        self.generatedVertices.extend(lowerRing)
        self.generatedVertices.extend(upperRing)
        self.generatedVertices.append(upperPoint)
    
    def getPillarRingZ(self, lowerPoint, upperPoint):
        lineIntersect = (upperPoint[2] - lowerPoint[2]) / (self.pillarCompHeight * 2)
        return min(self.pillarCompHeight, lineIntersect)
    
    def getPillarRadius(self, lowerPoint, upperPoint):
        lineIntersect = (upperPoint[2] - lowerPoint[2]) / (self.pillarCompHeight * 2)
        return min(self.pillarRadius, lineIntersect)

    def lowerRingMult(self, lowerPoint):
        if lowerPoint[2] == 0:
            return 0
        return 1

    def generateSupportPillarFaces(self, zero):
        faces  = []
        nIndex = 6
        for index in range(1, 7): 
            faces.append([zero, index + zero, nIndex + zero])
            faces.append([index + zero, nIndex + zero, index + 6 + zero])
            faces.append([index + 6 + zero, nIndex + 6 + zero, nIndex + zero])
            faces.append([zero + 13, index + 6 + zero, nIndex + 6 + zero])
            nIndex = index
        return faces

def main():
    plot    = Plot()
    printer = Printer(1000, 1000, 1000)

    printer.print('./objects/doublehalfcircle.obj', innerDenstiy=3, outerDensity=3)

    plot.plotMesh(printer.vertices, printer.faces)
    plot.plotSurface(printer.generatedVertices, printer.generatedFaces, subplot=0)
    plot.plotSurface(printer.generatedVertices, printer.generatedFaces, subplot=1)
    plot.show()

if __name__ == '__main__':
    main()