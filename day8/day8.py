#!/usr/bin/env python3
#
#  Advent of Code 2018 - Day 8
#
import re
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

class Node():
    def __init__(self, children, metadata, size):
        self.metadata = metadata
        self.children = children
        self.size = size

    def value(self):
        if not self.children:
            return sum(self.metadata)
        return sum([(self.children[i-1]).value() for i in self.metadata
            if i < len(self.children) + 1])

def next_child(license):
    """Return the node defined at the top of the given license.
    A node object is returned.
    """
    nchild, nmeta = license[:2]
    if nchild == 0:
        return Node([], license[2:2+nmeta], 2+nmeta)

    children = []
    index = 2
    for _ in range(nchild):
        child = next_child(license[index:])
        children.append(child)
        index += child.size
    return Node(children, license[index:index+nmeta], index + nmeta)

def all_metadata(top):
    result = list(top.metadata)
    for child in top.children:
        result.extend(all_metadata(child))
    return result

def solve(lines):
    """Solve the problem for Part 1."""
    license = list(map(int, lines[0].split()))
    top = next_child(license)
    metadata = all_metadata(top)
    return sum(metadata)


def solve2(lines):
    """Solve the problem for Part 2."""
    license = list(map(int, lines[0].split()))
    top = next_child(license)
    return top.value()

# PART 1

def sample_input():
    """Return the puzzle input and expected result for the part 1
    example problem.
    """
    lines = ['2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2']
    expected = 138
    return lines, expected

def example():
    lines, expected = sample_input()
    result = solve(lines)
    logger.info("got {} (expected {})".format(result, expected))
    assert result == expected
    logger.info('= ' * 32)

def part1(lines):
    result = solve(lines)
    logger.info("result is {}".format(result))
    logger.info('= ' * 32)


# PART 2

def sample_input2():
    """Return the puzzle input and expected result for the part 2
    example problem.
    """
    lines, _ = sample_input()
    expected = 66
    return lines, expected

def example2():
    lines, expected = sample_input2()
    result = solve2(lines)
    logger.info("got {} (expected {})".format(result, expected))
    assert result == expected
    logger.info('= ' * 32)

def part2(lines):
    result = solve2(lines)
    logger.info("result is {}".format(result))
    logger.info('= ' * 32)

if __name__ == '__main__':
    example()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)

