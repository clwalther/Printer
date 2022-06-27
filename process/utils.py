class Utils():
    def __init__(self):
        pass

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
    
    def getPlaneY(self, Y):
        POINTS = [[0, Y, 0], [1, Y, 0], [0, Y, 1]]
        return POINTS

    def getPlaneZ(self, Z):
        POINTS = [[0, 0, Z], [1, 0, Z], [0, 1, Z]]
        return POINTS
    

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
    
    def constructPolygon(self, face, vertices):
        polygon = []
        for vertice in face:
            polygon.append(vertices[vertice])
        return polygon

    def getLineFromRoot(self, root, X, Y, Z):
        vector = [root[0] + X, root[1] + Y, root[2] + Z]
        line   = [root, vector]
        return line

    def getHexPoints(self, X, Y, Z, C):
        hexPoints= [[ 0.0 + X,  (C) + Y, Z],
                    [ (3)**0.5 * (C) / 2 + X,  (C) / 2 + Y, Z],
                    [ (3)**0.5 * (C) / 2 + X, -(C) / 2 + Y, Z],
                    [ 0.0 + X, -(C) + Y, Z],
                    [-(3)**0.5 * (C) / 2 + X, -(C) / 2 + Y, Z],
                    [-(3)**0.5 * (C) / 2 + X,  (C) / 2 + Y, Z]]
        return hexPoints

    def generatePathway(self, vectors):
        MAXDISTANCE = 0.0001
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