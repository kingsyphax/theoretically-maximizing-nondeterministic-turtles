#!/usr/bin/env python

import sys
import random

def make_nasty(starting):
    """Return children and adjacencies for a nasty, beginning at vertex
    number STARTING.
    """

    children = set()
    adjacencies = set()

    for i in range(3):
        new_starting = starting + i * 5 + 1
        adjacencies.add((starting, new_starting)) # beginning of cycle

        for x in range(4):
            children.add(new_starting + x) # cycle is children
            adjacencies.add((new_starting + x, new_starting + x + 1)) # cycle edges 
        children.add(new_starting + 4)
        adjacencies.add((new_starting + 4, starting)) # end of cycle

    return children, adjacencies


def generate_nasty_instance(n):
    """Generate a N-vertex nasty instance"""

    filename = "nasty_instance_%d.in" % (n)
    output_file = open(filename, "w")

    output_file.write("%d\n" % (n)) # number of vertices

    children = set()
    adjacencies = set()

    for i in range(n // 16):
        new_children, new_adjacencies = make_nasty(16 * i)
        children |= new_children # union in (extend)
        adjacencies |= new_adjacencies

    if n % 16 > 5:
        starting = 16 * (n // 16)
        for x in range(starting, n - 1):
            children.add(x)
            adjacencies.add((x, x + 1))
        children.add(n-1)
        adjacencies.add((n - 1, starting))

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
        generate_nasty_instance(int(sys.argv[1]))
