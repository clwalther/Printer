from process.utils import Utils

class Slice:
    def __init__(self, PRECISION, INNER_SUPPORT_STRUCTURE,OUTER_SUPPORT_STRUCTURE, FACES, VERTICES):
        # imports
        self.utils = Utils()

        # init
        self.PRECISION = PRECISION

        self.INNER_SUPPORT_STRUCTURE = INNER_SUPPORT_STRUCTURE
        self.OUTER_SUPPORT_STRUCTURE = OUTER_SUPPORT_STRUCTURE
        self.FACES    = FACES
        self.VERTICES = VERTICES

        # vals
        self.toolPath = []

        self.parallelFaces = []

        self.maxPoint = self.utils.getMaxPoint(self.VERTICES)

        # direct method_call
        self.cut()
        

    def cut(self):
        self.getParallelFaces()
        self.getSlices()
        print("SLICE SUCCESS", end=', ')
    
    def getParallelFaces(self):
        for face in self.FACES:
            polygon  = self.utils.constructPolygon(face, self.VERTICES)
            minPoint = self.utils.getMinPoint(polygon)
            maxPoint = self.utils.getMaxPoint(polygon)
            self.appendParallelFaces(minPoint, maxPoint, polygon)
    
    def appendParallelFaces(self, minPoint, maxPoint, polygon):
        if not maxPoint[0] - minPoint[0] == 0:
            if (maxPoint[2] - minPoint[2]) / (maxPoint[0] - minPoint[0]) < self.PRECISION:
                self.parallelFaces.append(polygon)
        elif not maxPoint[1] - minPoint[1] == 0:
            if (maxPoint[2] - minPoint[2]) / (maxPoint[1] - minPoint[1]) < self.PRECISION:
                self.parallelFaces.append(polygon)

    def getSlices(self):
        zValue = 0
        while zValue <= self.maxPoint[2]:
            faces = []
            plane = self.utils.getPlaneZ(zValue)
            
            faces.extend(self.utils.getCloseFaces(plane, 2, self.VERTICES, self.FACES))
            faces.extend(self.utils.getCloseFaces(plane, 2, self.INNER_SUPPORT_STRUCTURE.generatedVertices, self.INNER_SUPPORT_STRUCTURE.generatedFaces))
            faces.extend(self.utils.getCloseFaces(plane, 2, self.OUTER_SUPPORT_STRUCTURE.generatedVertices, self.OUTER_SUPPORT_STRUCTURE.generatedFaces))
            
            vectors = self.utils.getIntersectingVectors(faces, plane)
            vectors = self.extendParallelVectors(zValue, vectors)
            
            polygons = self.utils.generatePathway(list(vectors))
            self.toolPath.append(polygons)

            zValue += self.PRECISION

    def extendParallelVectors(self, zValue, vectors):
        parallelVectors = self.getParallelVectors(zValue)
        vectors.extend(parallelVectors)
        return vectors
    
    def getParallelVectors(self, zValue):
        parallelVectors = []
        for polygon in self.parallelFaces:
            if abs(polygon[0][2] - zValue) < self.PRECISION:
                minPoint = self.utils.getMinPoint(polygon)
                maxPoint = self.utils.getMaxPoint(polygon)

                xValue = minPoint[0]
                while xValue < maxPoint[0]:
                    plane = self.utils.getPlaneX(xValue)
                    vectors = self.utils.getIntersectingVectors([polygon], plane)
                    parallelVectors = self.addParallelVectors(vectors, parallelVectors)
                    xValue += self.PRECISION
        return parallelVectors

    def addParallelVectors(self, vectors, parallelVectors):
        if len(vectors) > 0:
            zValue = vectors[0][0][2]
            for vector in vectors:
                if len(vector) > 0:
                    parallelVectors.append(list(vector))
        return parallelVectors