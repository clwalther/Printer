from __default__ import *
from __test__ import test, UnitTests

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import Printer

class Test:
    def __init__(self):
        self.default = Default()
    
    @test
    def pointInPolygon(self):
        # get
        printer = Printer(self.default.defaultXSize, self.default.defaultYSize, self.default.defaultZSize)
        # when
        POINT   = [5, 1]
        POLYGON = [[0, 0], [5, 5], [10, 0]]

        result  = printer.pointInPolygon(POLYGON, POINT)
        # then
        if result == False:
            return 1 # ERROR
        return 0
    
    @test
    def pointNotInPolygon(self):
        # get
        printer = Printer(self.default.defaultXSize, self.default.defaultYSize, self.default.defaultZSize)
        # when
        POINT   = [10, 1]
        POLYGON = [[0, 0], [5, 5], [10, 0]]

        result  = printer.pointInPolygon(POLYGON, POINT)
        # then
        if result == True:
            return 1 # ERROR
        return 0

    @test
    def planeLineIntersection(self):
        # get
        printer = Printer(self.default.defaultXSize, self.default.defaultYSize, self.default.defaultZSize)
        # when
        LINE   =  [[0, 0, 0], [0, 0, 1]]
        POLYGON = [[0, 0, 2], [5, 5, 2], [10, 0, 2]]

        result  = printer.getPointLineIntersectPlane(LINE, POLYGON)
        # then
        if isinstance(result, int):
            return 1 # ERROR
        return 0
    
    @test
    def planeLineNoIntersection(self):
        # get
        printer = Printer(self.default.defaultXSize, self.default.defaultYSize, self.default.defaultZSize)
        # when
        LINE   =  [[0, 0, 0], [0, 1, 0]]
        POLYGON = [[0, 0, 2], [5, 5, 2], [10, 0, 2]]

        result  = printer.getPointLineIntersectPlane(LINE, POLYGON)
        # then
        if isinstance(result, list):
            return 1 # ERROR
        return 0

    @test
    def constructPolygon(self):
        # get
        printer = Printer(self.default.defaultXSize, self.default.defaultYSize, self.default.defaultZSize)
        # when
        FACE = [0, 1, 3]
        VERTICES = [[0, 0, 0], [1, 2, 3], [2, 3, 4], [3, 4, 5]]
        result  = printer.constructPolygon(FACE, VERTICES)
        
        # then
        EXPECTED = [[0, 0, 0], [1, 2, 3], [3, 4, 5]]
        if not result == EXPECTED:
            return 1 # ERROR
        return 0

def main():
    test = Test()

    unitTest = UnitTests()
    unitTest.run(test)


if __name__ == '__main__':
    main()