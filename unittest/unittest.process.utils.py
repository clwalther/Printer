# default imports
from __test__ import before, test, after
from __test__ import Unittest

# additional libaries
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# imports to test
from process.utils import Utils

class UnittestProcessUtils:
    def __inti__(self):
        pass

    @test
    def GENERATE_PATHWAY_LENGTH_1(self):
        # get
        utils   = Utils()
        VECTORS = [
            [[12.5, 20.0, 12.5], [12.5, 20.0, 0.0]],
            [[12.5, 20.0, 20.0], [12.5, 20.0, 12.5]],
            [[12.5, 0.0, 7.5],   [12.5, 0.0, 0.0]],
            [[12.5, 0.0, 20.0],  [12.5, 0.0, 7.5]],
            [[12.5, 12.5, 20.0], [12.5, 20.0, 20.0]],
            [[12.5, 12.5, 20.0], [12.5, 0.0, 20.0]],
            [[12.5, 7.5, 0.0],   [12.5, 0.0, 0.0]],
            [[12.5, 7.5, 0.0],   [12.5, 20.0, 0.0]],

            [[1, 1, 1], [2, 2, 2]]
        ]
        
        # when
        result = utils.pathalgo.sort(VECTORS)

        # then
        if len(result) == 1:
            return 0
        else:
            return 1

def main():
    processUtils = UnittestProcessUtils()
    unittest     = Unittest(processUtils)
    unittest.run()


if __name__ == '__main__':
    main()