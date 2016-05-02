#!/usr/bin/env python

import sys
import os

adjacencies = None # adjacency matrix representation 
neighbors = None # adjacency list representation
n = None # size
SCCs = None # list of sets of vertices, representing the SCC decomposition


def is_complete():
    """Return whether the graph represented by the adjacency list in
    adjacencies is complete."""
    return all([all(lst) for lst in adjacencies])


def dfs_post_ordering(adjacencies):
    """Return a list of the DFS post-number ordering of the graph
    represented by ADJACENCIES."""
    def neighbors(v):
        neighbors = set()
        for u in range(n):
            if adjacencies[v][u]:
                neighbors.add(u)
        return neighbors

    ordering = []

    visited = set()

    def explore(v):
        visited.add(v)
        for u in neighbors(v):
            if u not in visited:
                explore(u)
        ordering.append(v) # count up post number

    while len(visited) < n:
        explore(min([i for i in range(n) if i not in visited]))

    return ordering


def get_SCCs():
    """Return a list of sets, representing the SCC decomposition of the graph."""
    SCCs = []

    reversed_adjacencies = [[0 for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            reversed_adjacencies[i][j] = adjacencies[j][i]

    reversed_post_ordering = dfs_post_ordering(reversed_adjacencies) # all vertices, in the order we'll use for the DFS (sink-first)
    processed = [] # which vertices have been put in components yet?

    current_component = [] # an SCC we're currently constructing

    visited = set()

    def explore(v):
        visited.add(v)
        current_component.append(v)
        processed.append(v)

        for u in neighbors[v]:
            if u not in visited:
                explore(u)

    while len(processed) < n:
        explore([x for x in reversed_post_ordering if x not in processed][-1]) # explore vertex that comes last in ordering, which hasn't been processed yet
        SCCs.append(current_component) # this component is finished
        current_component = [] # start new component

    return SCCs


def remove(i):
    """Completely remove vertex I, as if it had never been.
    Shifts numbers of all later vertices down by 1."""

    # update adjacencies
    
    del adjacencies[i] # remove all adjacencies FROM vertex i (shifting down all farther indices)

    for j in range(len(adjacencies)):
        del adjacencies[j][i] # remove all adjacencies TO vertex i
    
    # update neighbors

    del neighbors[i] # remove set of vertex i's neighbors

    for j in range(n - 1):
        if i in neighbors[j]: # i is no longer anyone's neighbor
            neighbors[j].remove(i) 
        for x in range(i + 1, n): # renumber neighbors who are vertices that come after i
            if x in neighbors[j]:
                neighbors[j].remove(x)
                neighbors[j].add(x - 1)

    # update n
    n -= 1 # graph is one smaller duh


def remove_all(s):
    """Completely remove all vertices in the set S."""
    for i in sorted(s)[::-1]: # remove in reverse order, so that the removal of one
                              # vertex does not change the names of other vertices
        remove(i)


def in_a_cycle(i):
    """Returns whether or not vertex I is in a cycle of size <= 5.
    (Does not consider SCCs.)"""
    visited = set()
    in_cycle = [False]

    def explore(v, d):
        if d >= 5:
            return 
        if i in neighbors[v]:
            in_cycle[0] = True

        visited.add(v)

        for n in neighbors[v]:
            if n not in visited:
                explore(n, d + 1)

    explore(i, 0)
    return in_cycle[0]


def gonna_die():
    """Returns all people (vertices) who are definitely going to die."""
    dooomed = set()
    for i in range(n):
        if not in_a_cycle(i):
            dooomed.add(i)
    return dooomed


def remove_not_in_a_cycle():
    """Remove from adjacencies and neighbors all vertices not in a cycle.
    (Does not take SCCs into account.)"""
    remove_all(gonna_die())


def get_neighbors(i):
    """Find adjacency list of vertex I from adjacency matrix (adjacencies)."""
    all_neighbors = set()
    for j in range(n):
        if adjacencies[i][j]:
            all_neighbors.add(j)
    return all_neighbors


def all_cycles(i):
    """Find all cycles of length at most 5 starting from vertex I."""

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
    output_file = open("complete.txt", "w")

    for filename in [x for x in os.listdir(".") if x[-3:] == ".in"]:
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

        output_file.write(filename + ": " + ("complete" if is_complete() else "not complete") + "\n")

    output_file.close()
