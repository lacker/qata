#!/usr/bin/env python

import math

from pyquil import get_qc, Program
from pyquil.api import local_forest_runtime
from pyquil.gates import *

prog = Program(H(0), CNOT(0, 1))


def get_qvm(num_qubits):
    return get_qc(f"{num_qubits}q-qvm")


def rotation(probability, index):
    """
    Return a gate that rotates a particular index with the given probability.
    So if it starts as a 0, with probability it goes to a 1.
    """
    angle = 2 * math.asin(math.sqrt(probability))
    return RX(angle, index)


def flip_coin(probability):
    """
    Flips a quantum coin, gets 1 with the given probability.
    """
    qvm = get_qvm(1)
    program = Program()
    ro = program.declare("ro", "BIT", 1)
    program += rotation(probability, 0)
    program += MEASURE(0, ro[0])
    result = qvm.run(program)
    return result[0]


def flip_coins(probabilities):
    """
    Flips a quantum coin for each probability.
    The probabilities are the odds of getting 1 in that spot.
    """
    qvm = get_qvm(len(probabilities))
    program = Program()
    ro = program.declare("ro", "BIT", len(probabilities))
    for i, prob in enumerate(probabilities):
        program += rotation(prob, i)
        program += MEASURE(i, ro[i])
    result = qvm.run(program)
    return list(result[0])


def throw_die_inefficiently(num_sides):
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


def throw_die(num_sides):
    probabilities = []
    while num_sides > 1:
        if num_sides % 2 == 0:
            probabilities.append(0.5)
            num_sides /= 2
        else:
            probabilities.append(1.0 / num_sides)
            num_sides -= 1
    # TODO: more


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
    results = [flip_coins([0.5, 0.3, 0.1]) for _ in range(100)]
    first = [a for a, _, _ in results]
    second = [b for _, b, _ in results]
    third = [c for _, _, c in results]
    print("first:")
    for i in range(2):
        print(i, first.count(i))
    print("second:")
    for i in range(2):
        print(i, second.count(i))
    print("third:")
    for i in range(2):
        print(i, third.count(i))


if __name__ == "__main__":
    with local_forest_runtime():
        main()
