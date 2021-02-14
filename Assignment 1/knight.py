#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : 2021 Feb 13, 12:10:58
@last modified : 2021 Feb 14, 17:49:36
"""
"""NAMES OF THE AUTHOR(S): Gael Aglin <gael.aglin@uclouvain.be>
                           Vincent Buccilli <vincent.buccilli@student.uclouvain.be>
                           Romain Graux <romain.graux@student.uclouvain.be>"""

import time
import sys
import copy as copylib
from search import *

KNIGHT = "♘"  # u"\u2658"
VISITED_TILE = "♞"  # u"\u265E"
NOT_VISITED_TILE = " "

#################
#   Key class   #
#################

class Key:
    @classmethod
    def naive(cls, position):
        """Return 0 whatever the position

        :param position: current position (y, x)
        """
        return 0

    @classmethod
    def border(cls, position, nRows, nCols):
        """Give the distance between the current position and the closest
        border

        :param position: current position (y, x)
        :param nRows: number of rows of the grid
        :param nCols: number of columns of the grid
        """
        return min(
            position[0] ** 2 + position[1] ** 2,
            position[0] ** 2 + (state.nCols - position[1] - 1) ** 2,
            (state.nRows - position[0] - 1) ** 2 + position[1] ** 2,
            (state.nCols - position[1] - 1) ** 2 + (state.nRows - position[0] - 1) ** 2,
        )


#################
# Problem class #
#################
class Knight(Problem):
    """Knight."""

    AVAILABLE_MOVES = [
        (-2, -1),
        (-1, -2),
        (2, -1),
        (-1, 2),
        (2, 1),
        (1, 2),
        (-2, 1),
        (1, -2),
    ]  # List all possible moves for a knight (L shape)

    def successor(self, state):
        """Yield all possible next states in ascending order (order given by
        `_border`)

        :param state: the current state
        """

        def _valid_pos(y, x):
            """Return True if the position is within the borders and
            the position is not yet visited, else False

            :param y: y coordinate of the position
            :param x: x coordinate of the position
            """
            return (
                0 <= x < state.nCols
                and 0 <= y < state.nRows
                and state.grid[y][x] == NOT_VISITED_TILE
            )

        positions = []
        for mov_y, mov_x in Knight.AVAILABLE_MOVES:
            new_x, new_y = state.x + mov_x, state.y + mov_y
            if _valid_pos(new_y, new_x):
                # print(f"Valid pos :: ({new_y} , {new_x})")
                positions.append((new_y, new_x))

        positions = sorted(positions, key=Key.naive, reverse=True)
        for pos in positions:
            new_state = state.next_state(pos)
            yield (0, new_state)

    def goal_test(self, state):
        """Return True is the state is the goal state i.e. we have visited all
        tiles (nRows * nCols)

        :param state: the current state
        """
        return state.n_visited == state.nRows * state.nCols


###############
# State class #
###############


class State:
    """State."""

    def __init__(self, shape, init_pos, grid=None, n_visited=1):
        """__init__.

        :param shape:
        :param init_pos:
        """
        self.shape = self.nRows, self.nCols = shape
        self.n_visited = n_visited
        self.grid = []
        for i in range(self.nRows):
            self.grid.append([" "] * self.nCols)

        if grid is not None:
            for i in range(self.nRows):
                for j in range(self.nCols):
                    self.grid[i][j] = grid[i][j]

        self.init_pos = self.y, self.x = init_pos
        self.grid[self.y][self.x] = KNIGHT

    def next_state(self, position):
        """Return the next state corresponding to the same state as self with
        new position

        :param position: the new position (y, x)
        """
        prev_y, prev_x = self.y, self.x
        st = State(self.shape, position, grid=self.grid, n_visited=self.n_visited)
        st.grid[prev_y][prev_x] = VISITED_TILE
        return st

    def __str__(self):
        """__str__."""
        print(f"nRows {self.nRows} :: nCols {self.nCols}")
        n_sharp = 2 * self.nCols + 1
        s = ("#" * n_sharp) + "\n"
        for i in range(self.nRows):
            s += "#"
            for j in range(self.nCols):
                s = s + str(self.grid[i][j]) + " "
            s = s[:-1]
            s += "#"
            if i < self.nRows - 1:
                s += "\n"
        s += "\n"
        s += "#" * n_sharp
        return s


INGINIOUS = False

if __name__ == "__main__":
    if not INGINIOUS:
        ##############################
        # Launch the search in local #
        ##############################
        # Use this block to test your code in local
        # Comment it and uncomment the next one if you want to submit your code on INGInious
        with open("instances.txt") as f:
            instances = f.read().splitlines()

        for instance in instances:
            elts = instance.split(" ")
            shape = (int(elts[0]), int(elts[1]))
            init_pos = (int(elts[2]), int(elts[3]))
            init_state = State(shape, init_pos)

            problem = Knight(init_state)

            # example of bfs tree search
            startTime = time.perf_counter()
            node, nb_explored, remaining_nodes = breadth_first_graph_search(problem)
            endTime = time.perf_counter()

            # example of print
            path = node.path()
            path.reverse()

            print("Number of moves: " + str(node.depth))
            for n in path:
                print(
                    n.state
                )  # assuming that the __str__ function of state outputs the correct format
                print()
            print("* Execution time:\t", str(endTime - startTime))
            print("* Path cost to goal:\t", node.depth, "moves")
            print("* #Nodes explored:\t", nb_explored)
            print("* Queue size at goal:\t", remaining_nodes)
    else:
        ####################################
        # Launch the search for INGInious  #
        ####################################
        # Use this block to test your code on INGInious
        shape = (int(sys.argv[1]), int(sys.argv[2]))
        init_pos = (int(sys.argv[3]), int(sys.argv[4]))
        init_state = State(shape, init_pos)

        problem = Knight(init_state)

        # example of bfs tree search
        startTime = time.perf_counter()
        node, nb_explored, remaining_nodes = breadth_first_graph_search(problem)
        endTime = time.perf_counter()

        # example of print
        path = node.path()
        path.reverse()

        print("Number of moves: " + str(node.depth))
        for n in path:
            print(
                n.state
            )  # assuming that the __str__ function of state outputs the correct format
            print()
        print("* Execution time:\t", str(endTime - startTime))
        print("* Path cost to goal:\t", node.depth, "moves")
        print("* #Nodes explored:\t", nb_explored)
        print("* Queue size at goal:\t", remaining_nodes)
