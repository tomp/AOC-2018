#!/bin/bash
# Create the directory for a new day's code.
#

usage () {
    echo "Usage: $0 <day>"
    echo "Create the directory for the given day."
    exit 0
}

error () {
    echo "Error: $*"
    exit 1
}

test -n "$1" || usage
DAY=$1

dir="day${DAY}"
prog="day${DAY}.py"

mkdir -p $dir                                        || error "Unable to create $dir"
test -f "$dir/$prog" || cp dayN.py "$dir/$prog"      || error "Unable to install $prog"

echo "Created $dir"

