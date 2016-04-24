#!/usr/bin/env python

import sys
import os

adjacencies = None # adjacency matrix representation 
neighbors = None # adjacency list representation
n = None # size


def get_neighbors(i):
    """Find adjacency list of vertex I from adjacency matrix ADJACENCIES."""

    all_neighbors = set()
    for j in range(n):
        if adjacencies[i][j]:
            all_neighbors.add(j)
    return all_neighbors


def all_cycles(i):
    """Find all cycles of length at most 5 starting from vertex I."""

    all_neighbors = set()
    cycles = []

    visited = set()

    def explore(v, cycle):
        visited.add(v)

        if i in neighbors[v]:
            cycles.append(cycle)

        if len(cycle) >= 5:
            return

        for u in neighbors[v]:
            if u not in cycle:
                explore(u, cycle | {u})
    explore(i, {i})

    return cycles


def value(cycle):
    """Returns the value of a cycle (children are worth 2, adults 1
       because that's the cost if they aren't included in any cycle)"""

    val = 0
    for x in cycle:
        if x in children:
            val += 2
        else:
            val += 1
    return val


def most_valuable_cycle(i):
    """Does what it says."""

    return max(all_cycles(i), key = value)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python3 -i code.py [input file]")
        os._exit(1)

    filename = sys.argv[1]

    input_file = None
    try:
        input_file = open(filename, "r")
    except IOError:
        print("Input file '%s' not found." % (filename))
        os._exit(1)

    n = int(input_file.readline())

    # construct set of children
    children = set(int(c) for c in input_file.readline().split())

    # construct list of whether is child
    is_child = []
    for i in range(n):
        is_child.append(i in children)

    # construct adjacency list and adjacency matrix
    adjacencies = []
    neighbors = []
    for i in range(n):
        adjacencies.append([bool(int(x)) for x in input_file.readline().split()])
        neighbors.append(get_neighbors(i))


