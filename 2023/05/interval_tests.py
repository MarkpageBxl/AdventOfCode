import unittest

from part2 import compute_interval_overlap, rel_to_abs as r2a, abs_to_rel as a2r


class RelAbsTests(unittest.TestCase):
    def testRelToAbs(self):
        d = (0, 5)
        self.assertEqual(r2a(d), (0, 4))
        d = (3, 10)
        self.assertEqual(r2a(d), (3, 12))

    def testAbsToRel(self):
        d = (0, 5)
        self.assertEqual(a2r(d), (0, 6))
        d = (3, 10)
        self.assertEqual(a2r(d), (3, 8))


class IntervalTests(unittest.TestCase):
    def test_full_disjunction_left(self):
        d1 = a2r((0, 4))
        d2 = a2r((5, 14))
        o, no = compute_interval_overlap(d1, d2)
        self.assertIsNone(o)
        self.assertEqual(no, [d1])

    def test_full_disjunction_right(self):
        d1 = a2r((20, 22))
        d2 = a2r((5, 14))
        o, no = compute_interval_overlap(d1, d2)
        self.assertIsNone(o)
        self.assertEqual(no, [d1])

    def test_partial_left_right_edge(self):
        d1 = a2r((0, 9))
        d2 = a2r((3, 9))
        o, no = compute_interval_overlap(d1, d2)
        self.assertEqual(o, a2r((3, 9)))
        self.assertEqual(len(no), 1)
        self.assertEqual(no[0], a2r((0, 2)))

    def test_partial_left_mid(self):
        d1 = a2r((0, 5))
        d2 = a2r((3, 9))
        o, no = compute_interval_overlap(d1, d2)
        self.assertEqual(o, a2r((3, 5)))
        self.assertEqual(len(no), 1)
        self.assertEqual(no[0], a2r((0, 2)))

    def test_partial_left_left_edge(self):
        d1 = a2r((0, 5))
        d2 = a2r((5, 10))
        o, no = compute_interval_overlap(d1, d2)
        self.assertEqual(o, a2r((5, 5)))
        self.assertEqual(len(no), 1)
        self.assertEqual(no[0], a2r((0, 4)))

    def test_partial_right_left_edge(self):
        d1 = a2r((5, 15))
        d2 = a2r((5, 10))
        o, no = compute_interval_overlap(d1, d2)
        self.assertEqual(o, a2r((5, 10)))
        self.assertEqual(len(no), 1)
        self.assertEqual(no[0], a2r((11, 15)))

    def test_partial_right_right_edge(self):
        d1 = a2r((81, 94))
        d2 = a2r((25, 94))
        o, no = compute_interval_overlap(d1, d2)
        self.assertEqual(o, a2r((81, 94)))
        self.assertEqual(len(no), 0)

    def test_partial_right_mid(self):
        d1 = a2r((8, 15))
        d2 = a2r((5, 10))
        o, no = compute_interval_overlap(d1, d2)
        self.assertEqual(o, a2r((8, 10)))
        self.assertEqual(len(no), 1)
        self.assertEqual(no[0], a2r((11, 15)))

    def test_subset_of(self):
        d1 = a2r((8, 10))
        d2 = a2r((6, 15))
        o, no = compute_interval_overlap(d1, d2)
        self.assertEqual(o, a2r((8, 10)))
        self.assertEqual(len(no), 0)

    def test_strictly_includes(self):
        d1 = a2r((3, 15))
        d2 = a2r((6, 12))
        o, no = compute_interval_overlap(d1, d2)
        self.assertEqual(o, a2r((6, 12)))
        self.assertEqual(len(no), 2)
        self.assertIn(a2r((3, 5)), no)
        self.assertIn(a2r((13, 15)), no)


if __name__ == "__main__":
    unittest.main(verbosity=2)
