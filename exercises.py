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


def throw_die(num_sides):
    answer_bits = math.ceil(math.log2(num_sides))
    num_bits = answer_bits + 1
    qvm = get_qc(f"{num_sides}q-qvm")
    program = Program()

    # TODO: finish, somehow


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
    results = [flip_coin(0.1) for _ in range(1000)]
    for x in range(2):
        print(x, results.count(x))


if __name__ == "__main__":
    with local_forest_runtime():
        main()
