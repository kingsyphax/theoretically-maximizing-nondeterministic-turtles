#!/usr/bin/env python

import random

def generate_big_instance():
    """Generate a randomized 500-vertex instance"""

    filename = "big_instance.in"
    output_file = open(filename, "w")

    output_file.write("500\n") # number of vertices = 500

    # print children
    for i in range(500):
        if random.random() < 0.5: # with probability 1/2...
            output_file.write(str(i) + " ") # ...this vertex is a child
    output_file.write("\n")

    # print adjacencies
    for i in range(500):
        for j in range(500):
            if i == j:
                output_file.write("0 ") # no vertex is connected to itself
            else:
                output_file.write(str(int(random.random() < 0.5)) + " ") # vertex i is connected to vertex j with probability 1/2
        output_file.write("\n")

    output_file.close()


if __name__ == "__main__":
    generate_big_instance()
