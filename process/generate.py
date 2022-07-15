from process.utils import *

class Inner_Support_Structure():
    def __init__(self, INNER_DENSITY, FACES, VERTICES):
        # imports
        self.utils = Utils()

        # init
        self.INNER_DENSITY = INNER_DENSITY

        self.FACES    = FACES
        self.VERTICES = VERTICES

        # vals
        self.generatedFaces    = []
        self.generatedVertices = []

        self.planes   = [[], []]
        self.polygons = []

        self.maxPoint = self.utils.general.getMaxPoint(self.VERTICES)

        # direct method_call
        self.generate()
    
    def generate(self):
        self.getPlanesAlgonX()
        self.getPlanesAlgonY()
        self.getPolygons()
        self.includePolygonInGenerated()
        print("INNER SUCCESS", end=', ')
    
    def getPlanesAlgonX(self):
        xValue = self.INNER_DENSITY / 2

        while xValue <= self.maxPoint[0] / 2:
            self.planes[0].append(self.utils.generate.planeX(self.maxPoint[0] / 2 + xValue))
            self.planes[0].append(self.utils.generate.planeX(self.maxPoint[0] / 2 - xValue))
            xValue += self.INNER_DENSITY
        
    def getPlanesAlgonY(self):
        yValue = self.INNER_DENSITY / 2

        while yValue <= self.maxPoint[1] / 2:
            self.planes[1].append(self.utils.generate.planeY(self.maxPoint[1] / 2 + yValue))
            self.planes[1].append(self.utils.generate.planeY(self.maxPoint[1] / 2 - yValue))
            yValue += self.INNER_DENSITY

    def getPolygons(self):
        for orientation in range(2):
            for plane in self.planes[orientation]:
                faces   = self.utils.general.getCloseFaces(plane, orientation, self.VERTICES, self.FACES)
                vectors = self.utils.geometry.getVectorsInterPOLYGONS_PLANE(faces, plane)
                polygon = self.utils.pathalgo.generatePathway(vectors)
                self.polygons.extend(polygon)     
    
    def includePolygonInGenerated(self):
        for polygon in self.polygons:
            index = len(self.generatedVertices)
            self.generatedFaces.append([length + index for length in range(len(polygon))])
            self.generatedVertices.extend(polygon)


class Outer_Support_Structure():
    def __init__(self, OUTER_DENSITY, PILLAR_COMP_HEIGHT, PILLAR_RADIUS, FACES, VERTICES):
        # imports
        self.utils = Utils()

        # init
        self.OUTER_DENSITY      = OUTER_DENSITY
        self.PILLAR_COMP_HEIGHT = PILLAR_COMP_HEIGHT
        self.PILLAR_RADIUS      = PILLAR_RADIUS

        self.FACES    = FACES
        self.VERTICES = VERTICES

        # vals
        self.generatedFaces    = []
        self.generatedVertices = []

        self.rootPoints   = []
        self.samplePoints = []
        self.blackPoints  = []

        self.maxPoint = self.utils.general.getMaxPoint(self.VERTICES)

        # direct method_call
        self.generate()
    
    def generate(self):
        self.generateRootPoints()
        self.setOuterSamplePoints()
        self.generateSupportPillars()
        print("OUTER SUCCESS", end=', ')
    
    def generateRootPoints(self):
        xValue = 0
        while xValue <= self.maxPoint[0] / 2:
            yValue = 0
            while yValue <= self.maxPoint[1] / 2:
                self.rootPoints.append([self.maxPoint[0] / 2 + xValue, self.maxPoint[1] / 2 + yValue])
                self.rootPoints.append([self.maxPoint[0] / 2 + xValue, self.maxPoint[1] / 2 - yValue])
                self.rootPoints.append([self.maxPoint[0] / 2 - xValue, self.maxPoint[1] / 2 + yValue])
                self.rootPoints.append([self.maxPoint[0] / 2 - xValue, self.maxPoint[1] / 2 - yValue])
                yValue += self.OUTER_DENSITY * 3
            xValue += self.OUTER_DENSITY * (3**0.5)

    def setOuterSamplePoints(self):
        for root in self.rootPoints:
            samplePoints = self.utils.generate.hexagonVertices(root[0], root[1], 0, self.OUTER_DENSITY)
            self.appendValidPoints(samplePoints)

    def appendValidPoints(self, samplePoints):
        for point in samplePoints:
            if not point in self.blackPoints and not point in self.samplePoints:
                if self.isBeneathObj(point):
                    self.samplePoints.append(point)
                else:
                    self.blackPoints.append(point)

    def isBeneathObj(self, point):
        for face in self.FACES:
            polygon  = self.utils.generate.polygon(face, self.VERTICES)
            isInside = self.utils.geometry.pointInPolygon(polygon, point)
            if isInside:
                return True
        return False

    def generateSupportPillars(self):
        pairs = self.getPillarPairs()
        for pair in pairs:
            self.generateSupportPillar(pair[0], pair[1])
    
    def getPillarPairs(self):
        pairs = []
        for point in self.samplePoints:
            heights = self.getHeights(point)
            for index in range(1, len(heights), 2):
                pairs.append([heights[index - 1], heights[index]])
        return pairs

    def getHeights(self, point):
        heights = [point]
        for face in self.FACES:
            polygon   = self.utils.generate.polygon(face, self.VERTICES)
            isBeneath = self.utils.geometry.pointInPolygon(polygon, point)
            if isBeneath:
                line  = self.utils.generate.lineFromRoot(point, X=0, Y=0, Z=1)
                inter = self.utils.geometry.getPointInterLINE_POLYGON(line, polygon)
                heights.append(inter)
        return sorted(heights, key = lambda x: x[2])

    def generateSupportPillar(self, lowerPoint, upperPoint):
        pillarRadius = self.getPillarRadius(lowerPoint, upperPoint)

        upperRingZ   = upperPoint[2] - self.getPillarRingZ(lowerPoint, upperPoint)
        lowerRingZ   = lowerPoint[2] + self.getPillarRingZ(lowerPoint, upperPoint) * self.lowerRingMult(lowerPoint)

        upperRing = self.utils.generate.hexagonVertices(lowerPoint[0], lowerPoint[1], upperRingZ, pillarRadius)
        lowerRing = self.utils.generate.hexagonVertices(lowerPoint[0], lowerPoint[1], lowerRingZ, pillarRadius)

        self.includePillarInFaces(len(self.generatedVertices))
        self.includePillarInVertices(lowerPoint, lowerRing, upperRing, upperPoint)

    def getPillarRingZ(self, lowerPoint, upperPoint):
        lineIntersect = (upperPoint[2] - lowerPoint[2]) / (self.PILLAR_COMP_HEIGHT * 2)
        return min(self.PILLAR_COMP_HEIGHT, lineIntersect)

    def getPillarRadius(self, lowerPoint, upperPoint):
        lineIntersect = (upperPoint[2] - lowerPoint[2]) / (self.PILLAR_COMP_HEIGHT * 2)
        return min(self.PILLAR_RADIUS, lineIntersect)

    def lowerRingMult(self, lowerPoint):
        if lowerPoint[2] == 0:
            return 0
        return 1

    def includePillarInVertices(self, lowerPoint, lowerRing, upperRing, upperPoint):
        self.generatedVertices.append(lowerPoint)
        self.generatedVertices.extend(lowerRing)
        self.generatedVertices.extend(upperRing)
        self.generatedVertices.append(upperPoint)

    def includePillarInFaces(self, zero):
        faces  = []
        nIndex = 6
        for index in range(1, 7): 
            faces.append([zero, index + zero, nIndex + zero])
            faces.append([index + zero, nIndex + zero, index + 6 + zero])
            faces.append([index + 6 + zero, nIndex + 6 + zero, nIndex + zero])
            faces.append([zero + 13, index + 6 + zero, nIndex + 6 + zero])
            nIndex = index
        self.generatedFaces.extend(faces)