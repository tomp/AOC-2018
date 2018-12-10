#!/usr/bin/env python3
#
#  Advent of Code 2018 - Day 10
#
import re
import json
from datetime import datetime, timedelta
from collections import namedtuple, defaultdict
from itertools import chain
from functools import reduce, total_ordering
from operator import attrgetter
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

INT_RE = r"\s*(-?\d+)"

line_re = re.compile(r"position=<{},{}> velocity=<{},{}>$".format(
    INT_RE, INT_RE, INT_RE, INT_RE))

class Point():
    def __init__(self, x0, y0, dx, dy):
        self.x0 = x0
        self.y0 = y0
        self.dx = dx
        self.dy = dy

    def __repr__(self):
        return "<Point x=({},{}), v=({},{})>".format(
                self.x0, self.y0, self.dx, self.dy)

    def at_time(self, t):
        return (self.x0 + t * self.dx, self.y0 + t * self.dy)


def parse_point(line):
    m = line_re.match(line)
    values = list(map(int, m.groups()))
    return Point(*values)

def points_at(points, t):
    return [p.at_time(t) for p in points]

def solve(lines, tmax=100000):
    """Solve the problem for Part 1."""
    points = list(map(parse_point, lines))

    tmin = -1
    area_min = -1
    for t in range(tmax):
        pt = points_at(points, t)
        xmax = max([p[0] for p in pt])
        xmin = min([p[0] for p in pt])
        ymax = max([p[1] for p in pt])
        ymin = min([p[1] for p in pt])
        area = (xmax-xmin)*(ymax - ymin)
        if area < area_min or tmin < 0:
            tmin = t
            area_min = area
        if area > area_min:
            break

    pt = points_at(points, tmin)
    xmax = max([p[0] for p in pt])
    xmin = min([p[0] for p in pt])
    ymax = max([p[1] for p in pt])
    ymin = min([p[1] for p in pt])

    result = []
    for _ in range(ymax - ymin + 1):
        result.append([' '] * (xmax - xmin + 1))
    for x, y in pt:
        result[y-ymin][x-xmin] = '#'

    sky = "\n".join(["".join(line) for line in result])
    return sky, tmin

def solve2(lines):
    """Solve the problem for Part 2."""
    pass

# PART 1

def sample_input():
    """Return the puzzle input and expected result for the part 1
    example problem.
    """
    lines = split_nonblank_lines("""
position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>""")
    sky_lines = split_nonblank_lines("""
......................
......................
......................
......................
......#...#..###......
......#...#...#.......
......#...#...#.......
......#####...#.......
......#...#...#.......
......#...#...#.......
......#...#...#.......
......#...#..###......
......................
......................
......................
......................""")
    expected = trim_sky(sky_lines)
    return lines, expected

def trim_sky(lines):
    coords = []
    for lineno, line in enumerate(lines):
        coords.extend([(idx, lineno) for idx, ch in enumerate(line) if ch == '#'])

    xmax = max([p[0] for p in coords])
    xmin = min([p[0] for p in coords])
    ymax = max([p[1] for p in coords])
    ymin = min([p[1] for p in coords])

    result = []
    for _ in range(ymax - ymin + 1):
        result.append([' '] * (xmax - xmin + 1))
    for x, y in coords:
        result[y-ymin][x-xmin] = '#'

    return "\n".join(["".join(line) for line in result])


def example():
    lines, expected = sample_input()
    result, elapsed = solve(lines)
    logger.info("got\n{}\n(expected\n{}\n".format(result, expected))
    logger.info("time of message: {}".format(elapsed))
    assert result == expected
    logger.info('= ' * 32)

def part1(lines):
    result, elapsed = solve(lines)
    logger.info("result is\n{}\n".format(result))
    logger.info("time of message: {}".format(elapsed))
    logger.info('= ' * 32)


if __name__ == '__main__':
    example()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)

