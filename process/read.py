from process.utils import Utils

class Read:
    def __init__(self, FILE_PATH):
        # imports
        self.utils = Utils()
        
        # init
        self.FILE_PATH = FILE_PATH
        
        # vals
        self.fileLines = []
        
        self.FACES    = []
        self.VERTICES = []

        # direct method_call
        self.run()

    def run(self):
        self.readData()
        self.trimData()
        self.formatFaces()
        self.normalizeVertices()
        print("READ SUCCESS", end=',  ')

    
    def readData(self):
        with open(self.FILE_PATH, 'r') as context:
            self.fileLines = context.readlines()

    def trimData(self):
        WHITE_SPACE = ' '
        
        for line in self.fileLines:
            trimedLine = line.split(WHITE_SPACE)
            self.formatData(trimedLine)

    def formatData(self, trimedLine):
        lineKey = trimedLine[0]
        self.appendData(lineKey, trimedLine[1:])
    
    def appendData(self, lineKey, trimedLine):
        if lineKey == 'v':
            lineValues = list(map(float, trimedLine))
            self.VERTICES.append(lineValues)
        elif lineKey == 'f':
            lineValues = list(map(float, trimedLine))
            self.FACES.append(lineValues)

    def formatFaces(self):
        self.FACES = [[int(verticeIndex - 1) for verticeIndex in faces] for faces in self.FACES]

    def normalizeVertices(self):
        minPoint = self.utils.general.getMinPoint(self.VERTICES)

        for verticeIndex in range(len(self.VERTICES)):
            self.VERTICES[verticeIndex][0] -= minPoint[0]
            self.VERTICES[verticeIndex][1] -= minPoint[1]
            self.VERTICES[verticeIndex][2] -= minPoint[2]  