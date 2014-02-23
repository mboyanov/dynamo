__author__ = 'marty'

import unittest
from myparser2 import *
# Here's our "unit".


# Here's our "unit tests".
class parserTests(unittest.TestCase):

    def testsShouldWork(self):
        arrays={'values':5}
        constants=['C']
        self.assertEqual(extractLeftParameter('T[arrays[values[2]]]',arrays=arrays),-1)
        assert(extractLeftParameter('T[arrays[values[C]]]',arrays=arrays,constants=constants)==-1)

        assert(extractLeftParameter('T[0]')==-1)
        assert(extractLeftParameter('T[i]')=='i')
        assert(extractLeftParameter('T[C]',constants=constants)==-1)
        assert(extractLeftParameter('answer')==-1)
        assert(extractFunctionAndArgument('min(T[j]+1)')==('min','T[j]+1'))
        assert(massSplitOneDFor('T[i-1]+1 for i in 1:N','T[i]')=='for i in range(1,N):\n\tT[i]=T[i-1]+1')
        assert(extractLeftParameterTwoD("answer")==(-1,-1))
        assert(extractLeftParameterTwoD("T[0][0]")==(-1,-1))




def main():
    unittest.main()

if __name__ == '__main__':
    main()