#!/usr/bin/env python

from pyquil import get_qc, Program
from pyquil.api import local_forest_runtime
from pyquil.gates import *

prog = Program(H(0), CNOT(0, 1))

with local_forest_runtime():
    qvm = get_qc("9q-square-qvm")
    results = qvm.run_and_measure(prog, trials=10)
    print(results)
