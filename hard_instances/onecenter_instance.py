#!/usr/bin/env python

import sys
import random


def make_cycle(starting):
    """Return children and adjacencies for a cycle, beginning at vertex
    number STARTING.
    """

    children = set()
    adjacencies = set()

    adjacencies.add((0, starting))
    adjacencies.add((starting, 0))

    adjacencies.add((starting, starting + 1))
    adjacencies.add((starting + 1, starting + 2))
    adjacencies.add((starting + 2, starting))

    children.add(starting + 1)
    children.add(starting + 2)

    return children, adjacencies


def generate_onecenter_instance(n):
    """Generate a N-vertex one-center instance"""

    filename = "onecenter_instance_%d.in" % (n)
    output_file = open(filename, "w")

    output_file.write("%d\n" % (n)) # number of vertices

    children = set()
    adjacencies = set()

    for i in range((n - 1) // 3):
        new_children, new_adjacencies = make_cycle(1 + 3 * i)
        children |= new_children # union in (extend)
        adjacencies |= new_adjacencies

    if (n-1) % 3 == 2:
        adjacencies.add((n-2, n-1))
        adjacencies.add((n-1, n-2))
        children.add(n-2)
        children.add(n-1)

    # print children
    for i in range(n):
        if i in children:
            output_file.write(str(i) + " ") # ...this vertex is a child
    output_file.write("\n")

    # print adjacencies
    for i in range(n):
        for j in range(n):
            if (i, j) in adjacencies:
                output_file.write("1 ") # edge exists
            else:
                output_file.write("0 ") # no edge
        output_file.write("\n")

    output_file.close()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        generate_onecenter_instance(int(sys.argv[1]))
