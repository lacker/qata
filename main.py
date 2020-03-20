#!/usr/bin/env python

from pyquil import Program
from pyquil.gates import *

p = Program()
p += X(0)
print(p)
