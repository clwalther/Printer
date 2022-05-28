from plot import Plot

class Printer:
    def __init__(self, xSize, ySize, zSize):
        # init (printer specific)
        self.xLength = xSize
        self.yLength = ySize
        self.zLength = zSize

        # post-init (file specific)
        self.filePath  = ""

        self.precision = None

        self.innerDenstiy = None
        self.outerDensity = None

        self.pillarCompHeight = None
        self.pillarRadius     = None

        # read
        self.fileLines = []
        self.faces     = []
        self.vertices  = []

        # generate
        self.generatedFaces    = []
        self.generatedVertices = []

        self.outerSamplePoints = {}

        # slice
        self.slice = []

        # execution
        self.position = [0, 0, 0]

    def print(self, filePath, precision, innerDenstiy, outerDensity, pillarCompHeight=0.6, pillarRadius=0.4):
        # init
        self.filePath         = filePath
        self.precision        = precision
        self.innerDenstiy     = innerDenstiy
        self.outerDensity     = outerDensity
        self.pillarCompHeight = pillarCompHeight
        self.pillarRadius     = pillarRadius
        # reading and modifying data
        self.readData()
        self.trimData()
        self.formatFacesValue()
        self.minPoint = self.getMinPoint(self.vertices) # utils
        self.normalizeData()
        self.maxPoint = self.getMaxPoint(self.vertices) # utils
        # generate support structures
        self.generateInnerSupport()
        self.generateOuterSupport()
        # slice
        self.sliceModel()

    # utils
    def getMinPoint(self, points):
        minPoint = [points[0][0], points[0][1], points[0][2]]

        for point in points:
            minPoint[0] = min(minPoint[0], point[0])
            minPoint[1] = min(minPoint[1], point[1])
            minPoint[2] = min(minPoint[2], point[2])
        return minPoint

    def getMaxPoint(self, points):
        maxPoint = [points[0][0], points[0][1], points[0][2]]

        for point in points:
            maxPoint[0] = max(maxPoint[0], point[0])
            maxPoint[1] = max(maxPoint[1], point[1])
            maxPoint[2] = max(maxPoint[2], point[2])
        return maxPoint

    def getDistance(self, A, B):
        distance = ((A[0] - B[0])**2 + (A[1] - B[1])**2 + (A[2] - B[2])**2)**0.5
        return distance

    def getPlaneX(self, X):
        POINTS = [[X, 0, 0], [X, 1, 0], [X, 0, 1]]
        return POINTS

    def getPlaneZ(self, Z):
        POINTS = [[0, 0, Z], [1, 0, Z], [0, 1, Z]]
        return POINTS

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
        RESULT, T  = self.calcIntersectionPlaneLine(LINE, A, B, C, D)
        return RESULT, T

    def getPlaneEqu(self, POINTS):
        AB = (POINTS[1][0] - POINTS[0][0], POINTS[1][1] - POINTS[0][1], POINTS[1][2] - POINTS[0][2])
        AC = (POINTS[2][0] - POINTS[0][0], POINTS[2][1] - POINTS[0][1], POINTS[2][2] - POINTS[0][2])
    
        a = (AB[1] * AC[2]) - (AC[1] * AB[2])
        b = (AB[2] * AC[0]) - (AC[2] * AB[0])
        c = (AB[0] * AC[1]) - (AC[0] * AB[1])
        d = -(a * POINTS[0][0] + b * POINTS[0][1] + c * POINTS[0][2])
        return a, b, c, d

    def calcIntersectionPlaneLine(self, LINE, A, B, C, D):
        SUM = (D * (-1)) - ((A * LINE[0][0]) + (B * LINE[0][1]) + (C * LINE[0][2]))
        PRODUCT = (A * (LINE[1][0] - LINE[0][0])) + (B * (LINE[1][1] - LINE[0][1])) + (C * (LINE[1][2] - LINE[0][2]))
        if not PRODUCT == 0:
            X = LINE[0][0] + (LINE[1][0] - LINE[0][0]) * SUM / PRODUCT
            Y = LINE[0][1] + (LINE[1][1] - LINE[0][1]) * SUM / PRODUCT
            Z = LINE[0][2] + (LINE[1][2] - LINE[0][2]) * SUM / PRODUCT
            return [X, Y, Z], SUM / PRODUCT
        else:
            return -1, -1 # ERROR

    def getCloseFaces(self, plane, orientation, vertices, faces):
        closeFaces = []
        for face in faces:
            polygon = self.constructPolygon(face, vertices)
            maxPoint = self.getMaxPoint(polygon)
            minPoint = self.getMinPoint(polygon)

            if maxPoint[orientation] >= plane[0][orientation] and minPoint[orientation] <= plane[0][orientation]:
                closeFaces.append(polygon)
        return closeFaces
    
    def getIntersectingVectors(self, polygons, plane):
        vectors = []
        for polygon in polygons:
            nIndex = len(polygon)-1
            intersectVector = []
            for index in range(len(polygon)):
                vector = [polygon[index], polygon[nIndex]]
                result, ratio = self.getPointLineIntersectPlane(vector, plane)
                if ratio >= 0 and ratio <= 1 and not result in intersectVector:
                    intersectVector.append(result)
                nIndex = index
            if len(intersectVector) > 1:
                vectors.append(intersectVector)
        return vectors

    def generatePathway(self, vectors):
        MAXDISTANCE = 0.000001
        support = []

        while len(vectors) > 0:
            points = 0
            support.append([vectors[points][0]])
            while points < len(vectors):
                if len(vectors[points]) == 1:
                    vectors.pop(points)
                    points = -1
                else:
                    index = 0
                    while index < len(vectors[points]):
                        if self.getDistance(support[-1][-1], vectors[points][index]) < MAXDISTANCE:
                            vectors, support = self.updateRootInPath(vectors, support, points, index)
                            points = -1
                            break
                        index += 1
                points += 1
        return support

    def updateRootInPath(self, vectors, support, points, index):
        vectors[points].pop(index)
        closest = self.getClosetsVerticeByIndex(support[-1][-1], vectors[points])
        support[-1].append(vectors[points][closest])
        vectors[points].pop(closest)
        self.checkCredibilityFace(vectors, points)
        return vectors, support

    def getClosetsVerticeByIndex(self, point, points):
        closest = 0
        for index in range(len(points)):
            if self.getDistance(point, points[index]) < self.getDistance(point, points[closest]):
                closest = index
        return closest

    def checkCredibilityFace(self, vectors, points):
        if len(vectors[points]) < 1:
            vectors.pop(points)
        return vectors

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
        polygons = []
        polygons.append(self.getPlanesAlgonX())
        polygons.append(self.getPlanesAlgonY())
        supportPolygons = self.getSupportPolygons(polygons)
        self.appendSupportPolygonsToGenerated(supportPolygons)

    def getPlanesAlgonX(self):
        polygons = []
        xValue = self.innerDenstiy / 2
        while xValue <= self.maxPoint[0] / 2:
            polygons.append([[self.maxPoint[0] / 2 + xValue, 0, 0], [self.maxPoint[0] / 2 + xValue, 1, 0], [self.maxPoint[0] / 2 + xValue, 0, 1]])
            polygons.append([[self.maxPoint[0] / 2 - xValue, 0, 0], [self.maxPoint[0] / 2 - xValue, 1, 0], [self.maxPoint[0] / 2 - xValue, 0, 1]])
            xValue += self.innerDenstiy
        return polygons
    
    def getPlanesAlgonY(self):
        polygons = []
        yValue = self.innerDenstiy / 2
        while yValue <= self.maxPoint[1] / 2:
            polygons.append([[0, self.maxPoint[1] / 2 + yValue, 0], [1, self.maxPoint[1] / 2 + yValue, 0], [0, self.maxPoint[1] / 2 + yValue, 1]])
            polygons.append([[0, self.maxPoint[1] / 2 - yValue, 0], [1, self.maxPoint[1] / 2 - yValue, 0], [0, self.maxPoint[1] / 2 - yValue, 1]])
            yValue += self.innerDenstiy
        return polygons

    def getSupportPolygons(self, polygons):
        supportPolygons = []
        for index in range(2):
            for polygon in polygons[index]:
                faces = self.getCloseFaces(polygon, index, self.vertices, self.faces)
                vectors = self.getIntersectingVectors(faces, polygon)
                support = self.generatePathway(vectors)
                supportPolygons.extend(support)
        return supportPolygons
    
    def appendSupportPolygonsToGenerated(self, supportPolygons):
        for polygon in supportPolygons:
            index = len(self.generatedVertices)
            self.generatedFaces.append([i + index for i in range(len(polygon))])
            self.generatedVertices.extend(polygon)

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
                line     = self.getLineFromRoot(point, X=0, Y=0, Z=1)
                inter, _ = self.getPointLineIntersectPlane(line, polygon)
                heights.append(inter[2])
        return heights

    def generateOuterSupportPillars(self):
        for keys in self.outerSamplePoints.keys():
            LIST = self.getSortedSamplePoints(keys)
            for index in range(0, len(LIST)-1, 2):
                lowerPoint = self.strToList(keys + f";{LIST[index+0]}", float)
                upperPoint = self.strToList(keys + f";{LIST[index+1]}", float)
                self.generateSupportPillar(lowerPoint, upperPoint)

    def getSortedSamplePoints(self, key):
        LIST = sorted(self.outerSamplePoints[key])
        LIST.insert(0, 0.0)
        return LIST

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

    # slice
    def sliceModel(self):
        parallelFaces = self.getParallelFaces()
        self.getSlices(parallelFaces)

    def getParallelFaces(self):
        parallelFaces = []
        for face in self.faces:
            polygon = self.constructPolygon(face, self.vertices)
            minPoint = self.getMinPoint(polygon)
            maxPoint = self.getMaxPoint(polygon)
            parallelFaces = self.extendParallelFaces(minPoint, maxPoint, polygon, parallelFaces)
        return parallelFaces
    
    def extendParallelFaces(self, minPoint, maxPoint, polygon, parallelFaces):
        if not maxPoint[0] - minPoint[0] == 0:
            if (maxPoint[2] - minPoint[2]) / (maxPoint[0] - minPoint[0]) < self.precision:
                parallelFaces.append(polygon)
        elif not maxPoint[1] - minPoint[1] == 0:
            if (maxPoint[2] - minPoint[2]) / (maxPoint[1] - minPoint[1]) < self.precision:
                parallelFaces.append(polygon)
        return parallelFaces

    def getSlices(self, parallelFaces):
        zValue = 0
        while zValue <= self.maxPoint[2]:
            faces = []
            plane = self.getPlaneZ(zValue)
            faces.extend(self.getCloseFaces(plane, 2, self.vertices, self.faces))
            faces.extend(self.getCloseFaces(plane, 2, self.generatedVertices, self.generatedFaces))
            vectors = self.getIntersectingVectors(faces, plane)
            vectors = self.extendParallelVectors(zValue, vectors, parallelFaces)
            polygons = self.generatePathway(list(vectors))
            self.slice.append(polygons)

            zValue += self.precision

    def extendParallelVectors(self, zValue, vectors, parallelFaces):
        parallelVectors = self.getParallelVectors(parallelFaces, zValue)
        vectors.extend(parallelVectors)
        return vectors
    
    def getParallelVectors(self, parallelFaces, zValue):
        parallelVectors = []
        for polygon in parallelFaces:
            if abs(polygon[0][2] - zValue) < self.precision:
                minPoint = self.getMinPoint(polygon)
                maxPoint = self.getMaxPoint(polygon)

                xValue = minPoint[0]
                while xValue < maxPoint[0]:
                    plane = self.getPlaneX(xValue)
                    vectors = self.getIntersectingVectors([polygon], plane)
                    parallelVectors = self.addParallelVectors(vectors, parallelVectors)
                    xValue += self.precision
        return parallelVectors

    def addParallelVectors(self, vectors, parallelVectors):
        if len(vectors) > 0:
            zValue = vectors[0][0][2]
            for vector in vectors:
                if len(vector) > 0:
                    parallelVectors.append(list(vector))
        return parallelVectors

def main():
    plot = Plot()

    printer = Printer(1000, 1000, 1000)
    printer.print('./objects/cube.obj', precision=0.1, innerDenstiy=5, outerDensity=2)

    plot.plotSurface(printer.vertices, printer.faces, subplot=0)
    plot.plotMesh(printer.generatedVertices, printer.generatedFaces, subplot=0)

    vertices = []
    faces = []
    for row in printer.slice:
        for elements in row:
            index = len(vertices)
            vertices.extend([[round(value, 6) for value in point] for point in elements])
            faces.append([i + index for i in range(len(elements))])  

    plot.plotMesh(vertices, faces, subplot=1)
    plot.show()

if __name__ == '__main__':
    main()