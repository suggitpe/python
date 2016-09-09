import unittest
import skeleton

class SkeletonTest(unittest.TestCase):
    def testSkeleton(self):
        foo = skeleton.foobar().upper()
        self.assertEqual(foo, 'FOO')

if __name__ == '__main__':
    unittest.main()