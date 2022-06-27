from __init__ import *

class Printer:
    def __init__(self):
        # DEV
        self.plot  = Plot()
        self.timer = Timer()

    def print(self, FILE_PATH, PRECISION, INNER_DENSITY, OUTER_DENSITY, PILLAR_COMP_HEIGHT=0.6, PILLAR_RADIUS=0.4):
        # init
        self.FILE_PATH          = FILE_PATH
        self.PRECISION          = PRECISION
        self.INNER_DENSITY      = INNER_DENSITY
        self.OUTER_DENSITY      = OUTER_DENSITY
        self.PILLAR_COMP_HEIGHT = PILLAR_COMP_HEIGHT
        self.PILLAR_RADIUS      = PILLAR_RADIUS

        self.timer.start()
        self.READ = Read(
            self.FILE_PATH
        )
        self.timer.checkpoint()
        # self.plot.vertices(self.READ.VERTICES, 0)
        # self.plot.surface(self.READ.VERTICES, self.READ.FACES, 1)
        # self.plot.show()

        self.INNER_SUPPORT_STRUCTURE = Inner_Support_Structure(
            self.INNER_DENSITY, 
            self.READ.FACES,
            self.READ.VERTICES
        )
        self.timer.checkpoint()
        # self.plot.vertices(self.INNER_SUPPORT_STRUCTURE.generatedVertices, 0)
        # self.plot.mesh(self.INNER_SUPPORT_STRUCTURE.generatedVertices, self.INNER_SUPPORT_STRUCTURE.generatedFaces, 0)
        # self.plot.show()

        self.OUTER_SUPPORT_STRUCTURE = Outer_Support_Structure(
            self.OUTER_DENSITY,
            self.PILLAR_COMP_HEIGHT,
            self.PILLAR_RADIUS,
            self.READ.FACES,
            self.READ.VERTICES
        )
        self.timer.checkpoint()
        # self.plot.vertices(self.OUTER_SUPPORT_STRUCTURE.generatedVertices, 0)
        # self.plot.surface(self.OUTER_SUPPORT_STRUCTURE.generatedVertices, self.OUTER_SUPPORT_STRUCTURE.generatedFaces, 1)
        # self.plot.show()

        self.SLICE = Slice(
            self.PRECISION,
            self.INNER_SUPPORT_STRUCTURE,
            self.OUTER_SUPPORT_STRUCTURE,
            self.READ.FACES,
            self.READ.VERTICES
        )
        self.timer.checkpoint()
        # self.plot.vertices(self.SLICE.toolPath[0], 0)
        # self.plot.show()
        
        self.timer.printTimestamps()

def main():
    printer = Printer()

    FILE_PATH     = './objects/halfball.obj'
    PRECISION     = 0.1
    INNER_DENSITY = 5.0
    OUTER_DENSITY = 2.0

    printer.print(
        FILE_PATH=FILE_PATH,
        PRECISION=PRECISION,
        INNER_DENSITY=INNER_DENSITY,
        OUTER_DENSITY=OUTER_DENSITY
    )

if __name__ == '__main__':
    main()