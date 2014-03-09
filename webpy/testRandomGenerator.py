__author__ = 'marty'

import unittest
import randomgenerator

class MyTestCase(unittest.TestCase):
    def test_randomConstants(self):
        t= "[['C',1,2]]"
        constants=randomgenerator.getRandomConstants(t)
        self.assertIn('C',constants)
        self.assertTrue(constants['C']==1 or constants['C']==2 )
        self.assertNotIn('B',constants)

    def test_randomArrays(self):
        t= "[('weights',10,1,10),('values',10,1,10)]"
        arrays=randomgenerator.getRandomArrays(t)
        self.assertIn('weights',arrays)
        self.assertTrue(len(arrays['values'])==10 )
        self.assertNotIn('B',arrays)

    def test_randomSpecialArrays(self):
        t="[('values',5,1,10,'addone')]"
        arrays=randomgenerator.getRandomArrays(t)
        self.assertIn('values',arrays)
        self.assertIn(1,arrays['values'])


if __name__ == '__main__':
    unittest.main()
