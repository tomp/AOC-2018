#!/usr/bin/env python3

import pytest

from day16 import Device


OPCODE_CASES = [
    (["addr, 0, 1, 2"],
     [3, 5, 7, 11],
     [3, 5, 8, 11]
    ),
    (["addi, 2, 4, 0"],
     [3, 5, 7, 11],
     [11, 5, 7, 11]
    ),

    (["mulr, 1, 2, 3"],
     [3, 5, 7, 11],
     [3, 5, 7, 35]
    ),
    (["muli, 2, 6, 1"],
     [3, 5, 7, 11],
     [3, 42, 7, 11]
    ),

    (["banr, 0, 1, 3"],
     [3, 5, 7, 11],
     [3, 5, 7, 1]
    ),
    (["bani, 3, 5, 0"],
     [3, 5, 7, 11],
     [1, 5, 7, 11]
    ),
    (["bani, 3, 15, 0"],
     [3, 5, 7, 11],
     [11, 5, 7, 11]
    ),

    (["borr, 0, 1, 3"],
     [3, 5, 7, 11],
     [3, 5, 7, 7]
    ),
    (["bori, 3, 5, 1"],
     [3, 5, 7, 11],
     [3, 15, 7, 11]
    ),

    (["setr, 1, 99, 3"],
     [3, 5, 7, 11],
     [3, 5, 7, 5]
    ),
    (["seti, 13, 99, 2"],
     [3, 5, 7, 11],
     [3, 5, 13, 11]
    ),

    (["gtir, 4, 2, 3"],
     [3, 5, 7, 11],
     [3, 5, 7, 0]
    ),
    (["gtir, 4, 1, 3"],
     [3, 5, 7, 11],
     [3, 5, 7, 0]
    ),
    (["gtir, 4, 0, 2"],
     [3, 5, 7, 11],
     [3, 5, 1, 11]
    ),

    (["gtri, 2, 4, 3"],
     [3, 5, 7, 11],
     [3, 5, 7, 1]
    ),
    (["gtri, 0, 4, 3"],
     [3, 5, 7, 11],
     [3, 5, 7, 0]
    ),

    (["gtrr, 3, 2, 0"],
     [3, 5, 7, 11],
     [1, 5, 7, 11]
    ),
    (["gtrr, 2, 3, 1"],
     [3, 5, 7, 11],
     [3, 0, 7, 11]
    ),

    (["eqir, 3, 0, 1"],
     [3, 5, 7, 11],
     [3, 1, 7, 11]
    ),
    (["eqir, 3, 1, 1"],
     [3, 5, 7, 11],
     [3, 0, 7, 11]
    ),

    (["eqri, 3, 7, 1"],
     [3, 5, 7, 11],
     [3, 0, 7, 11]
    ),
    (["eqri, 3, 11, 0"],
     [3, 5, 7, 11],
     [1, 5, 7, 11]
    ),

    (["eqrr, 2, 3, 0"],
     [3, 5, 7, 11],
     [0, 5, 7, 11]
    ),
    (["eqrr, 2, 2, 3"],
     [3, 5, 7, 11],
     [3, 5, 7, 1]
    ),
]

@pytest.mark.parametrize( "prog,reg,expected", OPCODE_CASES)
def test_opcode(prog, reg, expected):
    dev = Device(reg=reg)
    dev.load_prog(prog)
    dev.step()
    assert dev.reg == expected
