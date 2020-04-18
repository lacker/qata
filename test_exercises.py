#!/usr/bin/env python

import unittest

import numpy as np

from pyquil.api import local_forest_runtime

from exercises import *


class TestExercises(unittest.TestCase):
    def test_octahedral_die(self):
        for _ in range(10):
            outcome = throw_octahedral_die()
            self.assertLess(outcome, 9)
            self.assertGreater(outcome, 0)

    def test_controlled(self):
        c = controlled(np.zeros((2, 2)))
        self.assertEqual(np.trace(c), 2)
        c = controlled(np.identity(2))
        self.assertEqual(np.trace(c), 4)


if __name__ == "__main__":
    with local_forest_runtime():
        unittest.main(warnings="ignore")
