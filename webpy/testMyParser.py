__author__ = 'marty'

import unittest
import testRandomGenerator
from myparser2 import *
# Here's our "unit".


# Here's our "unit tests".
class parserTests(unittest.TestCase):

    def testsShouldWork(self):
        arrays={'values':5}
        constants=['C']
        self.assertEqual(extractLeftParameter('T[arrays[values[2]]]',arrays=arrays),-1)
        self.assertEqual(extractLeftParameter('T[arrays[values[C]]]',arrays=arrays,constants=constants),-1)
        self.assertEqual(extractLeftParameter('T[0]'),-1)
        self.assertEqual(extractLeftParameter('T[i]'),'i')
        self.assertEqual(extractLeftParameter('T[C]',constants=constants),-1)
        self.assertEqual(extractLeftParameter('answer'),-1)
        self.assertEqual(extractFunctionAndArgument('min(T[j]+1)'),('min','T[j]+1'))
        self.assertEqual(massSplitOneDFor('T[i-1]+1 for i in 1:N','T[i]'),'for i in range(1,N):\n\tT[i]=T[i-1]+1')
        self.assertEqual(extractLeftParameterTwoD("answer"),(-1,-1))
        self.assertEqual(extractLeftParameterTwoD("T[0][0]"),(-1,-1))
        self.assertRaises(Exception,"T[[0]=1")
        self.assertRaises(Exception,"T[i]=1 for j in 1:N")



def main():
    unittest.main()


if __name__ == '__main__':
    main()