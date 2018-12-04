#!/usr/bin/env python3
#
#  Advent of Code 2018 - Day 4
#
import re
from datetime import datetime
from collections import namedtuple, defaultdict
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

log_re = re.compile(r".(\d\d\d\d-\d\d-\d\d \d\d:\d\d). (.+)")

BEGIN_MSG = 'begins shift'
SLEEP_MSG = 'falls asleep'
AWAKE_MSG = 'wakes up'

Nap = namedtuple('Nap', ['id', 'date', 'asleep', 'awake'])


def parse_logs(lines):
    """Parse a set of log lines into nap records for the guards.
    A list of Nap objects is returned.
    """
    naps = []
    guard_id = 0
    asleep, awake = -1, -1
    for line in sorted(lines):
        m = log_re.match(line)
        ymd_hms, msg = m.groups()
        dt = datetime.strptime(ymd_hms, '%Y-%m-%d %H:%M')
        if BEGIN_MSG in msg:
            guard_id = parse_begins(msg)
        elif SLEEP_MSG in msg:
            if dt.hour == 23:
                asleep = 0
            else:
                asleep = dt.minute
        elif AWAKE_MSG in msg:
            assert dt.hour == 0
            awake = dt.minute
            naps.append(Nap(guard_id, dt.date(), asleep, awake))
        else:
            raise ValueError("unexpected log: '{}'".format(msg))
    return naps

def parse_begins(msg):
    """Parse the guard ID out of the "begins his shift" message."""
    words = msg.split()
    return int(words[1][1:])

def sleeplog():
    """Return an initialized per-minute sleep log."""
    return [0] * 60

def sleep_logs(naps):
    """Compile per-minute sleep logs for each guard.
    A dict mapping the guard id to their sleep log is returned.
    """
    sleeping = defaultdict(sleeplog)
    for nap in naps:
        for m in range(nap.asleep, nap.awake):
            sleeping[nap.id][m] += 1
    return sleeping

def compile_stats(sleeplogs):
    """Calculate stats describing each guards sleep patterns.
    A dict mapping the guard id to a tuple of their stats is returned.
    The tuple contains (guard_id, total_min, max_min, time_of_max_min)
    """
    sleep_stats = dict()
    for guard_id, asleep in sleeplogs.items():
        total_sleep = sum(asleep)
        max_sleep = max(asleep)
        max_time = asleep.index(max_sleep)
        sleep_stats[guard_id] = (guard_id, total_sleep, max_sleep, max_time)
    return sleep_stats

def solve(lines):
    """Solve the problem for Part 1."""
    sleeping = sleep_logs(parse_logs(lines))
    sleep_stats = compile_stats(sleeping)
    guards = sorted(sleep_stats.values(), key=lambda v: v[1], reverse=True)
    guard_id, total_sleep, max_sleep, max_time = guards[0]
    return guard_id * max_time


def solve2(lines):
    """Solve the problem for Part 2."""
    sleeping = sleep_logs(parse_logs(lines))
    sleep_stats = compile_stats(sleeping)
    guards = sorted(sleep_stats.values(), key=lambda v: v[2], reverse=True)
    guard_id, total_sleep, max_sleep, max_time = guards[0]
    return guard_id * max_time


# PART 1

def sample_input():
    """Return the puzzle input and expected result for the part 1
    example problem.
    """
    lines = split_nonblank_lines("""
[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up
""")
    expected = 240
    return lines, expected

def example():
    # single example
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
    expected = 4455
    return lines, expected

def example2():
    lines, expected = sample_input2()
    result = solve2(lines)
    logger.info("got {} (expected {})".format(result, expected))
    logger.info('= ' * 32)

def part2(lines):
    result = solve2(lines)
    logger.info("result is {}".format(result))
    logger.info('= ' * 32)

if __name__ == '__main__':
    example()
    input = load_input(INPUTFILE)
    part1(input)
    example2()
    part2(input)

