#!/usr/bin/env python

import unittest
from part1 import next_coeffs, alternate


class Tests(unittest.TestCase):
    def test_binomial(self):
        coeffs = next_coeffs([])
        self.assertEqual(coeffs, [1])
        coeffs = next_coeffs(coeffs)
        self.assertEqual(coeffs, [1, 1])
        coeffs = next_coeffs(coeffs)
        self.assertEqual(coeffs, [1, 2, 1])
        coeffs = next_coeffs(coeffs)
        self.assertEqual(coeffs, [1, 3, 3, 1])
        coeffs = next_coeffs(coeffs)
        self.assertEqual(coeffs, [1, 4, 6, 4, 1])

    def test_alternate(self):
        l = alternate([1, 4, 6, 4, 1])
        self.assertEqual(l, [1, -4, 6, -4, 1])
        l = alternate([])
        self.assertEqual(l, [])
        l = alternate([1])
        self.assertEqual(l, [1])


if __name__ == "__main__":
    unittest.main(verbosity=2)
