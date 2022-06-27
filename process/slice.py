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
        
        self.leveledVectors = {}
        self.maxPoint = self.utils.general.getMaxPoint(self.VERTICES)

        # direct method_call
        self.run()

    def run(self):
        self.generateLeveledVectors()
        self.getSlices()
        print("SLICE SUCCESS", end=', ')

    def generateLeveledVectors(self):
        for face in self.FACES:
            polygon  = self.utils.generate.polygon(face, self.VERTICES)
            minPoint = self.utils.general.getMinPoint(polygon)
            maxPoint = self.utils.general.getMaxPoint(polygon)
            self.checkPolygonDelta(polygon, minPoint, maxPoint)
        
    def checkPolygonDelta(self, polygon, minPoint, maxPoint):
        if not maxPoint[0] - minPoint[0] == 0:
            if (maxPoint[2] - minPoint[2]) / (maxPoint[0] - minPoint[0]) < self.PRECISION:
                self.extendLeveledVectors(polygon, minPoint, maxPoint)
        elif not maxPoint[1] - minPoint[1] == 0:
            if (maxPoint[2] - minPoint[2]) / (maxPoint[1] - minPoint[1]) < self.PRECISION:
                self.extendLeveledVectors(polygon, minPoint, maxPoint)
    
    def extendLeveledVectors(self, polygon, minPoint, maxPoint):
        xValue = minPoint[0]
        while xValue <= maxPoint[0]:
            plane  = self.utils.generate.planeX(xValue)
            vector = self.utils.geometry.getVectorsInterPOLYGONS_PLANE([polygon], plane)
            
            self.handleLeveledVectors(vector)
            xValue += self.PRECISION
    
    def handleLeveledVectors(self, vector):
        if len(vector) >= 1:
            zKey = self.utils.general.getClosestMultiple(vector[0][0][2], self.PRECISION)
            self.prepareLeveledVectors(zKey)
            self.leveledVectors[zKey].extend(vector)
    
    def prepareLeveledVectors(self, zKey):
        if not zKey in self.leveledVectors.keys():
            self.leveledVectors[zKey] = []

    def getSlices(self):
        zValue = 0
        while zValue <= self.maxPoint[2] + self.PRECISION:
            plane   = self.utils.generate.planeZ(zValue)
            faces   = self.getFaces(plane)
            vectors = self.getVectors(faces, plane, zValue)
            polygon = self.utils.pathalgo.generatePathway(vectors)
            
            self.toolPath.extend(polygon)
            zValue += self.PRECISION        
    
    def getFaces(self, plane):
        faces = []
        faces.extend(self.utils.general.getCloseFaces(plane, 2, self.VERTICES, self.FACES))
        faces.extend(self.utils.general.getCloseFaces(plane, 2, self.INNER_SUPPORT_STRUCTURE.generatedVertices, self.INNER_SUPPORT_STRUCTURE.generatedFaces))
        faces.extend(self.utils.general.getCloseFaces(plane, 2, self.OUTER_SUPPORT_STRUCTURE.generatedVertices, self.OUTER_SUPPORT_STRUCTURE.generatedFaces))
        return faces

    def getVectors(self, faces, plane, zValue):
        vectors = []
        vectors.extend(self.utils.geometry.getVectorsInterPOLYGONS_PLANE(faces, plane))
        vectors.extend(self.getLeveledVectors(zValue))
        return vectors
    
    def getLeveledVectors(self, zValue):
        zKey = self.utils.general.getClosestMultiple(zValue, self.PRECISION)

        if zKey in self.leveledVectors.keys():
            return self.leveledVectors[zKey]
        return []