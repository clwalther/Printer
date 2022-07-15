class Utils():
    def __init__(self):
        self.general  = General()
        self.geometry = Geometry()
        self.generate = Generate()
        self.pathalgo = Pathalgo()


class General():
    def __init__(self):
        self.generate = Generate()

    def getMinPoint(self, POINTS):
        minPoint = [POINTS[0][0], POINTS[0][1], POINTS[0][2]]

        for point in POINTS:
            minPoint[0] = min(minPoint[0], point[0])
            minPoint[1] = min(minPoint[1], point[1])
            minPoint[2] = min(minPoint[2], point[2])
        return minPoint

    def getMaxPoint(self, POINTS):
        maxPoint = [POINTS[0][0], POINTS[0][1], POINTS[0][2]]

        for point in POINTS:
            maxPoint[0] = max(maxPoint[0], point[0])
            maxPoint[1] = max(maxPoint[1], point[1])
            maxPoint[2] = max(maxPoint[2], point[2])
        return maxPoint

    def getDistance(self, A, B):
        distance = 0
        for index in range(len(A)):
            distance += (A[index] - B[index])**2
        distance = distance**0.5
        return distance

    def getClosestMultiple(self, A, MUL):
        if MUL > A:
            return 0
 
        A = A + MUL/2
        A = A - (A % MUL)
        return round(A * MUL, 2)

    def getCloseFaces(self, PLABE, ORIENTATION, VERTICES, FACES):
        closeFaces = []
        for face in FACES:
            polygon = self.generate.polygon(face, VERTICES)
            maxPoint = self.getMaxPoint(polygon)
            minPoint = self.getMinPoint(polygon)

            if maxPoint[ORIENTATION] >= PLABE[0][ORIENTATION] and minPoint[ORIENTATION] <= PLABE[0][ORIENTATION]:
                closeFaces.append(polygon)
        return closeFaces


class Geometry:
    def __init__(self):
        self.generate = Generate()

    def pointInPolygon(self, POLYGON, POINT):
        odd = False
        POLYGON.append(POLYGON[0])
        for index in range(len(POLYGON)-1):
            if (POLYGON[index][1] <= POINT[1] and POLYGON[index+1][1] > POINT[1]) or (POLYGON[index][1] > POINT[1] and POLYGON[index+1][1] <= POINT[1]):
                if POINT[0] < POLYGON[index][0] + ((POINT[1] - POLYGON[index][1]) / (POLYGON[index+1][1] - POLYGON[index][1])) * (POLYGON[index+1][0] - POLYGON[index][0]):
                    odd = not odd
        return odd

    def getPlaneEqu(self, POINTS):
        ab = (POINTS[1][0] - POINTS[0][0], POINTS[1][1] - POINTS[0][1], POINTS[1][2] - POINTS[0][2])
        ac = (POINTS[2][0] - POINTS[0][0], POINTS[2][1] - POINTS[0][1], POINTS[2][2] - POINTS[0][2])
    
        a = (ab[1] * ac[2]) - (ac[1] * ab[2])
        b = (ab[2] * ac[0]) - (ac[2] * ab[0])
        c = (ab[0] * ac[1]) - (ac[0] * ab[1])
        d = -(a * POINTS[0][0] + b * POINTS[0][1] + c * POINTS[0][2])
        return a, b, c, d

    def getPointInterLINE_POLYGON(self, LINE, POLYGON):
        a, b, c, d = self.getPlaneEqu(POLYGON)
        point, ___ = self.clacPointInterLINE_PLANE(LINE, a, b, c, d)
        return point

    def getPointInterVECTOR_POLYGON(self, VECTOR, POLYGON):
        a, b, c, d = self.getPlaneEqu(POLYGON)
        point, mul = self.clacPointInterLINE_PLANE(VECTOR, a, b, c, d)
        if not mul == None and mul <= 1 and mul >= 0:
            return point
        else:
            return None

    def getVectorsInterPOLYGONS_PLANE(self, POLYGONS, PLANE):
        vectors = []
        for polygon in POLYGONS:
            intersectVectors = self.getIntersectingVectorsFromPlane(polygon, PLANE)
            vectors = self.appendIntersectVectors(intersectVectors, vectors)
        return vectors
    
    def getIntersectingVectorsFromPlane(self, POLYGON, PLANE):
        intersectVectors = []
        secondaryVector  = POLYGON[-1]
        for primaryVector in POLYGON:
            vector = self.generate.vectorFromPoints(primaryVector, secondaryVector)
            point  = self.getPointInterVECTOR_POLYGON(vector, PLANE)
            
            if not point == None and not point in intersectVectors:
                intersectVectors.append(point)
            secondaryVector = primaryVector
        return intersectVectors
    
    def appendIntersectVectors(self, INTERSECT_VECTORS, VECTORS):
        if len(INTERSECT_VECTORS) >= 2:
            VECTORS.append(INTERSECT_VECTORS)
        return VECTORS
    
    def clacPointInterLINE_PLANE(self, LINE, A, B, C, D):
        sum = (D * (-1)) - ((A * LINE[0][0]) + (B * LINE[0][1]) + (C * LINE[0][2]))
        product = (A * (LINE[1][0] - LINE[0][0])) + (B * (LINE[1][1] - LINE[0][1])) + (C * (LINE[1][2] - LINE[0][2]))
        if not product == 0:
            X = LINE[0][0] + (LINE[1][0] - LINE[0][0]) * sum / product
            Y = LINE[0][1] + (LINE[1][1] - LINE[0][1]) * sum / product
            Z = LINE[0][2] + (LINE[1][2] - LINE[0][2]) * sum / product
            return [X, Y, Z], sum / product
        else:
            return None, None


class Generate:
    def __init__(self):
        pass
    
    def planeX(self, X):
        POINTS = [[X, 0, 0], [X, 1, 0], [X, 0, 1]]
        return POINTS
    
    def planeY(self, Y):
        POINTS = [[0, Y, 0], [1, Y, 0], [0, Y, 1]]
        return POINTS

    def planeZ(self, Z):
        POINTS = [[0, 0, Z], [1, 0, Z], [0, 1, Z]]
        return POINTS

    def polygon(self, FACE, VERTICES):
        polygon = []
        for verticeIndex in FACE:
            polygon.append(VERTICES[verticeIndex])
        return polygon

    def hexagonVertices(self, X, Y, Z, C):
        vertices = [[ 0.0 + X, + (C) + Y, Z],
                    [ (3)**0.5 * (C) / 2 + X,  (C) / 2 + Y, Z],
                    [ (3)**0.5 * (C) / 2 + X, -(C) / 2 + Y, Z],
                    [ 0.0 + X, - (C) + Y, Z],
                    [-(3)**0.5 * (C) / 2 + X, -(C) / 2 + Y, Z],
                    [-(3)**0.5 * (C) / 2 + X,  (C) / 2 + Y, Z]]
        return vertices

    def lineFromRoot(self, ROOT, X, Y, Z):
        vector = [ROOT[0] + X, ROOT[1] + Y, ROOT[2] + Z]
        line   = [ROOT, vector]
        return line

    def vectorFromPoints(self, A, B):
        vector = [A, B]
        return vector


class Pathalgo:
    def __init__(self):
        self.general = General()
        self.THRESHOLD = 10 ** (-4)

    def generatePathway(self, VECTORS):
        support = []

        while len(VECTORS) > 0:
            points = 0
            support.append([VECTORS[points][0]])
            while points < len(VECTORS):
                if len(VECTORS[points]) == 1:
                    VECTORS.pop(points)
                    points = -1
                else:
                    index = 0
                    while index < len(VECTORS[points]):
                        if self.general.getDistance(support[-1][-1], VECTORS[points][index]) < self.THRESHOLD:
                            VECTORS, support = self.updateRootInPath(VECTORS, support, points, index)
                            points = -1
                            break
                        index += 1
                points += 1
        return support

    def updateRootInPath(self, VECTORS, SUPPORT, POINTS, INDEX):
        VECTORS[POINTS].pop(INDEX)
        closest = self.getClosetsVerticeByIndex(SUPPORT[-1][-1], VECTORS[POINTS])
        SUPPORT[-1].append(VECTORS[POINTS][closest])
        VECTORS[POINTS].pop(closest)
        self.checkCredibilityFace(VECTORS, POINTS)
        return VECTORS, SUPPORT

    def getClosetsVerticeByIndex(self, POINT, POINTS):
        closest = 0
        for index in range(len(POINTS)):
            if self.general.getDistance(POINT, POINTS[index]) < self.general.getDistance(POINT, POINTS[closest]):
                closest = index
        return closest

    def checkCredibilityFace(self, VECTORS, POINTS):
        if len(VECTORS[POINTS]) < 1:
            VECTORS.pop(POINTS)
        return VECTORS