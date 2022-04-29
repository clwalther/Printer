from __default__ import *
from __test__ import test, UnitTests

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import Printer

class Test:
    def __init__(self):
        self.default = Default()

    @test
    def noDublicatesInSamplePoints(self):
        # get
        printer = Printer(self.default.defaultXSize, self.default.defaultYSize, self.default.defaultZSize)
        # when
        printer.print(self.default.defaultObjectFile)
        # then
        for element in printer.samplePoints:
            if printer.samplePoints.count(element) > 1:
                return 1
        return 0

def main():
    test = Test()

    unitTest = UnitTests()
    unitTest.run(test)


if __name__ == '__main__':
    main()