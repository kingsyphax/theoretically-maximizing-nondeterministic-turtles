#!/usr/bin/env python

import sys
import random

def make_turtle(starting):
    """Return children and adjacencies for a turtle, beginning at vertex
    number STARTING.
    """

    children = set()
    adjacencies = set()

    for i in range(5):
        children.add(starting + i) # node in central cycle
        adjacencies.add((starting + i, starting + ((i + 1) % 5))) # central cycle edges 

        new_starting = starting + (i + 1) * 4 + 1
        adjacencies.add((starting + i, new_starting))
        for x in range(3):
            adjacencies.add((new_starting + x, new_starting + x + 1)) # outer cycle edges 
        adjacencies.add((new_starting + 3, starting + i))

    return children, adjacencies


def generate_turtle_instance(n):
    """Generate a N-vertex turtle instance"""

    filename = "turtle_instance_%d.in" % (n)
    output_file = open(filename, "w")

    output_file.write("%d\n" % (n)) # number of vertices

    children = set()
    adjacencies = set()

    for i in range(n // 25):
        new_children, new_adjacencies = make_turtle(25 * i)
        children |= new_children # union in (extend)
        adjacencies |= new_adjacencies

    if n % 25 > 5:
        starting = 25 * (n // 25)
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
        generate_turtle_instance(int(sys.argv[1]))
