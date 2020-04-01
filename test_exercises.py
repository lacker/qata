#!/usr/bin/env python

import unittest

from pyquil.api import local_forest_runtime

from exercises import *


class TestExercises(unittest.TestCase):
    def test_octahedral_die(self):
        outcomes = [throw_octahedral_die() for _ in range(80)]
        for outcome in outcomes:
            self.assertLess(outcome, 9)
            self.assertGreater(outcome, 0)


if __name__ == "__main__":
    with local_forest_runtime():
        unittest.main()
