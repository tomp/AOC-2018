#!/usr/bin/env python3
#
#  Advent of Code 2018 - Day 12
#
import re
import json
from datetime import datetime, timedelta
from collections import namedtuple, defaultdict
from itertools import chain
import logging


logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)
logger = logging.getLogger()

INPUTFILE = 'input.txt'


# Utility functions

def strip(line):
    return line.strip()

def load_input(infile):
    with open(infile, 'r') as fp:
        return list(filter(bool, map(strip, fp)))

def split_nonblank_lines(text):
    return list(filter(bool, map(strip, text.splitlines())))


# Solution

def parse_lines(lines):
    assert lines[0].startswith("initial state: ")
    state = lines[0].split()[2]
    rules = defaultdict(lambda: '.')
    for line in lines[1:]:
        if line:
            pattern, sep, result = line.split()
            rules[pattern] = result
    return state, rules

def score_state(state, start=0):
    score = 0
    for idx, pot_state in enumerate(state):
        if pot_state == '#':
            score += idx + start
    return score

def solve(lines, ngen):
    """Solve the problem for Part 1."""
    state, rules = parse_lines(lines)
    for i, rule in enumerate(rules.items()):
        print(i, rule)

    start = -3
    state = "..." + state + "..."

    for gen in range(ngen):
        # print(gen, score_state(state, start), start, state[2:])
        if gen % 1000 == 0:
            print(gen, score_state(state, start), start)
        pots = list(state)
        for idx in range(len(state) - 4):
            pots[idx + 2] = rules[state[idx:idx+5]]
        nextstate = "".join(pots)

        if not nextstate.endswith("..."):
            nextstate = nextstate + "."
        if nextstate.startswith("....."):
            state = nextstate[2:]
            start += 2
        elif nextstate.startswith("..."):
            state = nextstate
        else:
            state = "." + nextstate
            start -= 1
    print(gen+1, score_state(state, start), start, state[2:])
    return score_state(state, start)


def solve2(lines):
    """Solve the problem for Part 2."""
    pass

# PART 1

def sample_input():
    """Return the puzzle input and expected result for the part 1
    example problem.
    """
    lines = split_nonblank_lines("""
initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #""")
    expected = 325
    return lines, expected

def example():
    lines, expected = sample_input()
    result = solve(lines, 20)
    logger.info("got {} (expected {})".format(result, expected))
    assert result == expected
    logger.info('= ' * 32)

def part1(lines):
    result = solve(lines, 20)
    logger.info("result is {}".format(result))
    logger.info('= ' * 32)


# PART 2

def part2(lines):
    result = solve(lines, 100000)
    logger.info("result is {}".format(result))
    logger.info('= ' * 32)

if __name__ == '__main__':
    example()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    part2(input_lines)

