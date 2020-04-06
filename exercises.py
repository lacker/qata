#!/usr/bin/env python

import math

from pyquil import get_qc, Program
from pyquil.api import local_forest_runtime
from pyquil.gates import *

prog = Program(H(0), CNOT(0, 1))


# TODO: remove
def apply_conditional_hadamard(program, condition, targets):
    """
    In the superimposition where the condition is true, applies Hadamard gates
    on all the target bits.
    """
    for target in targets:
        program += H(target).controlled(condition)


def flip_coin(probability):
    """
    Flips a quantum coin, gets 1 with the given probability.
    """
    qvm = get_qc("1q-qvm")
    program = Program()
    ro = program.declare("ro", "BIT", 1)
    angle = 2 * math.asin(math.sqrt(probability))
    program += RX(angle, 0)
    program += MEASURE(0, ro[0])
    result = qvm.run(program)
    return result[0]


def get_qvm(num_qubits):
    return get_qc(f"{num_qubits}q-qvm")


def throw_die(num_sides):
    qvm = get_qvm(num_sides)
    program = Program()
    ro = program.declare("ro", "BIT", num_sides)
    for i in range(num_sides):
        # A 0 in the ith bit represents choosing this number.
        # We first set it to 1, then if there are no previous 0's,
        # we set it to zero with the appropriate probability.
        program += X(i)
        remaining = num_sides - i
        angle = 2 * math.asin(math.sqrt(1.0 / remaining))
        gate = RX(angle, i)
        for j in range(i):
            gate = gate.controlled(j)
        program += gate
    for i in range(num_sides):
        program += MEASURE(i, ro[i])
    result = qvm.run(program)
    return list(result[0]).index(0)


def throw_octahedral_die():
    qvm = get_qc("3q-qvm")
    program = Program(H(0), H(1), H(2))
    ro = program.declare("ro", "BIT", 3)
    program += MEASURE(0, ro[0])
    program += MEASURE(1, ro[1])
    program += MEASURE(2, ro[2])
    result = qvm.run(program)
    a, b, c = result[0]
    return 1 + 4 * a + 2 * b + c


def main():
    results = [throw_die(5) for _ in range(100)]
    for i in range(5):
        print(i, results.count(i))


if __name__ == "__main__":
    with local_forest_runtime():
        main()
