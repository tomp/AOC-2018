#!/usr/bin/env python3
#
#  Advent of Code 2018 - Day 9
#
from collections import defaultdict
import logging

from llist import dllist, dllistnode


logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)
logger = logging.getLogger()

INPUT = (464, 70918)


# Solution

def solve(nplayer, nmarble):
    """Solve the problem for Part 1."""
    score = defaultdict(int)
    circle = dllist([0, 2, 1, 3])
    cur = circle.nodeat(3)
    for marble in range(circle.size, nmarble+1):
        node = cur
        if marble % 23:
            for _ in range(2):
                node = node.next or circle.first
            cur = circle.insert(marble, node)
        else:
            for _ in range(7):
                node = node.prev or circle.last
            cur = node.next or circle.first
            value = circle.remove(node)
            player = (marble - 1) % nplayer + 1
            score[player] += marble + value
    return max(score.values())


def solve2(nplayer, nmarble):
    """Solve the problem for Part 2."""
    pass

# PART 1

def sample_cases():
    """Return the example inputs and expected results for the part 1.
    (Used if there are multiple example cases.)
    """
    return [( 9,   25,     32),
            (10, 1618,   8317),
            (13, 7999, 146373),
            (17, 1104,   2764),
            (21, 6111,  54718),
            (30, 5807,  37305)]

def example():
    cases = sample_cases()
    for nplayer, nmarble, expected in cases:
        result = solve(nplayer, nmarble)
        logger.info("({}, {}) -> {} (expected {})".format(nplayer,
            nmarble, result, expected))
        assert result == expected

    logger.info('= ' * 32)

def part1(nplayer, nmarble):
    result = solve(nplayer, nmarble)
    logger.info("result is {}".format(result))
    logger.info('= ' * 32)


# PART 2

def part2(nplayer, nmarble):
    result = solve(nplayer, 100 * nmarble)
    logger.info("result is {}".format(result))
    logger.info('= ' * 32)

if __name__ == '__main__':
    example()
    input_values = INPUT
    part1(*input_values)
    part2(*input_values)

