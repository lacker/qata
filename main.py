#!/usr/bin/env python

from pyquil import get_qc, Program
from pyquil.api import local_forest_runtime
from pyquil.gates import *

prog = Program(H(0), CNOT(0, 1))


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


def throw_polyhedral_die(num_sides):
    answer_bits = math.ceil(math.log2(num_sides))
    num_bits = answer_bits + 1
    qvm = get_qc(f"{num_bits}q-qvm")

    # TODO: finish, somehow


def main():
    print(throw_octahedral_die())


if __name__ == "__main__":
    with local_forest_runtime():
        main()
