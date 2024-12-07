import unittest

from part2 import to_base


class BaseTest(unittest.TestCase):
    def test_binary(self):
        f = lambda x: to_base(x, 2)
        self.assertEqual(f(0), "0")
        self.assertEqual(f(1), "1")
        self.assertEqual(f(2), "10")
        self.assertEqual(f(3), "11")
        self.assertEqual(f(4), "100")
        self.assertEqual(f(5), "101")
        self.assertEqual(f(6), "110")
        self.assertEqual(f(7), "111")
        self.assertEqual(f(8), "1000")

    def test_ternary(self):
        f = lambda x: to_base(x, 3)
        self.assertEqual(f(0), "0")
        self.assertEqual(f(1), "1")
        self.assertEqual(f(2), "2")
        self.assertEqual(f(3), "10")
        self.assertEqual(f(4), "11")
        self.assertEqual(f(5), "12")
        self.assertEqual(f(6), "20")
        self.assertEqual(f(7), "21")
        self.assertEqual(f(8), "22")
        self.assertEqual(f(9), "100")


if __name__ == "__main__":
    unittest.main(verbosity=2)
