#!/usr/bin/env python

from pyquil import Program
from pyquil.gates import *

p = Program()
ro = p.declare("ro", "BIT", 1)
p += X(0)
p += MEASURE(0, ro[0])

print(p)
