class Printer:
    def __init__(self, xSize, ySize, zSize):
        self.fileLines = []
        self.filePath  = ""

        self.faces     = []
        self.vertecies = []
        
        self.xLength = xSize
        self.yLength = ySize
        self.zLength = zSize

        self.position = [0, 0, 0]
    
    def print(self, filePath):
        self.read(filePath)
        self.trimData()

    def read(self, filePath):
        with open(filePath, 'r') as context:
            self.fileLines = context.readlines()
    
    def trimData(self):
        whiteSpace = ' '
        for line in self.fileLines:
            lineAsArray = line.split(whiteSpace)
            self.formatData(lineAsArray)
            
    def formatData(self, lineAsArray):
        prefixVerteceis = 'v'
        prefixFaces     = 'f'

        if lineAsArray[0] == prefixVerteceis:
            for values in lineAsArray[1:]:
                print(int(values))
        elif lineAsArray[0] == prefixFaces:
            for values in lineAsArray[1:]:
                print(int(values))

def main():
    xSize = 1000
    ySize = 1000
    zSize = 1000

    printer = Printer(xSize, ySize, zSize)
    printer.print('./objects/cube.obj')

if __name__ == '__main__':
    main()