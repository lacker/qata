#!/usr/bin/env python3

import math

import numpy as np

from pyquil import get_qc, Program
from pyquil.api import local_forest_runtime, WavefunctionSimulator
from pyquil.gates import *
from pyquil.quil import DefGate

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
    num_sides_log = []
    while num_sides > 1:
        num_sides_log.append(num_sides)
        if num_sides % 2 == 0:
            probabilities.append(0.5)
            num_sides /= 2
        else:
            probabilities.append(1.0 / num_sides)
            num_sides -= 1
    flips = flip_coins(probabilities)
    answer = 1
    for flip, maximum in reversed(list(zip(flips, num_sides_log))):
        if not flip:
            continue
        if maximum % 2 == 0:
            answer += maximum / 2
        else:
            answer = maximum
    return answer


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


def controlled(submatrix):
    """
    Create a matrix that applies submatrix to the second qubit based on the first qubit.
    """
    upper_left = np.identity(2)
    off_diagonal = np.zeros((2, 2))
    upper = np.concatenate([upper_left, off_diagonal], axis=0)
    lower = np.concatenate([off_diagonal, submatrix], axis=0)
    return np.concatenate([upper, lower], axis=1)


def simulate_controlled_y():
    y = np.array([[0, -1j], [1j, 0]])
    controlled_y_definition = DefGate("CONTROLLED-Y", controlled(y))
    CONTROLLED_Y = controlled_y_definition.get_constructor()

    p = Program(controlled_y_definition)
    p += NOT(0)
    p += CONTROLLED_Y(0, 1)
    print(WavefunctionSimulator().wavefunction(p))
    # TODO: see if this can find wavefunction starting with 1,0


def diffusion(n):
    """
    Return a n x n Grover's diffusion operator matrix.
    """
    ones = np.ones((n, n))
    identity = np.identity(n)
    return 2.0 / n * ones - identity


def single_shot_grovers(input_bits):
    n = round(math.log2(len(input_bits)))
    if 2 ** n != len(input_bits):
        raise Exception(f"could not logify ${input_bits}")

    # Construct gates for operating our function, and Grover diffusion
    bit_picker_matrix = np.diag([1 - 2 * bit for bit in input_bits])
    bit_picker_definition = DefGate("BIT-PICKER", bit_picker_matrix)
    BIT_PICKER = bit_picker_definition.get_constructor()

    diffusion_matrix = diffusion(len(input_bits))
    diffusion_definition = DefGate("DIFFUSION", diffusion_matrix)
    DIFFUSION = diffusion_definition.get_constructor()

    # Wire up the program
    qvm = get_qvm(n)
    p = Program()
    p += bit_picker_definition
    p += diffusion_definition
    p += BIT_PICKER(*range(n))
    p += DIFFUSION(*range(n))

    print(WavefunctionSimulator().wavefunction(p))


# TODO: run and see if this does something
def main():
    single_shot_grovers([0, 0, 1, 0])


if __name__ == "__main__":
    with local_forest_runtime():
        main()
