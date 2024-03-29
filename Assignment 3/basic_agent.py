#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : 2021 Mar 30, 10:13:15
@last modified : 2021 Apr 01, 07:46:07
"""


from core.player import Player, Color
from seega.seega_rules import SeegaRules
from copy import deepcopy


class AI(Player):

    in_hand = 12
    score = 0
    name = "Basic Agent"

    def __init__(self, color):
        super(AI, self).__init__(color)
        self.position = color.value

    def play(self, state, remain_time):
        print("")
        print(f"Player {self.position} is playing.")
        print("time remain is ", remain_time, " seconds")
        return minimax_search(state, self)

    def successors(self, state):
        """successors.
        The successors function must return (or yield) a list of pairs (a, s) in which a is the action played to reach the state s.

        :param state: the state for which we want the successors
        """
        for action in SeegaRules.get_player_actions(state, self.position):
            next_state = deepcopy(state)
            SeegaRules.act(next_state, action, self.position)
            yield action, next_state

    def cutoff(self, state, depth):
        """cutoff.
        The cutoff function returns true if the alpha-beta/minimax search has to stop and false otherwise.

        :param state: the state for which we want to know if we have to apply the cutoff
        :param depth: the depth of the cutoff
        """
        return SeegaRules.is_end_game(state) or depth > 0

    def evaluate(self, state):
        """evaluate.
        The evaluate function must return an integer value representing the utility function of the board.

        :param state: the state for which we want the evaluation scalar
        """
        return state.score[self.position]

    def set_score(self, new_score):
        self.score = new_score

    def update_player_infos(self, infos):
        self.in_hand = infos["in_hand"]
        self.score = infos["score"]

    def reset_player_informations(self):
        self.in_hand = 12
        self.score = 0


"""
MiniMax and AlphaBeta algorithms.
Adapted from:
    Author: Cyrille Dejemeppe <cyrille.dejemeppe@uclouvain.be>
    Copyright (C) 2014, Universite catholique de Louvain
    GNU General Public License <http://www.gnu.org/licenses/>
"""

inf = float("inf")


def minimax_search(state, player, prune=True):
    """Perform a MiniMax/AlphaBeta search and return the best action.

    Arguments:
    state -- initial state
    player -- a concrete instance of class AI implementing an Alpha-Beta player
    prune -- whether to use AlphaBeta pruning

    """

    def max_value(state, alpha, beta, depth):
        if player.cutoff(state, depth):
            return player.evaluate(state), None
        val = -inf
        action = None
        for a, s in player.successors(state):
            if (
                s.get_latest_player() == s.get_next_player()
            ):  # next turn is for the same player
                v, _ = max_value(s, alpha, beta, depth + 1)
            else:  # next turn is for the other one
                v, _ = min_value(s, alpha, beta, depth + 1)
            if v > val:
                val = v
                action = a
                if prune:
                    if v >= beta:
                        return v, a
                    alpha = max(alpha, v)
        return val, action

    def min_value(state, alpha, beta, depth):
        if player.cutoff(state, depth):
            return player.evaluate(state), None
        val = inf
        action = None
        for a, s in player.successors(state):
            if (
                s.get_latest_player() == s.get_next_player()
            ):  # next turn is for the same player
                v, _ = min_value(s, alpha, beta, depth + 1)
            else:  # next turn is for the other one
                v, _ = max_value(s, alpha, beta, depth + 1)
            if v < val:
                val = v
                action = a
                if prune:
                    if v <= alpha:
                        return v, a
                    beta = min(beta, v)
        return val, action

    _, action = max_value(state, -inf, inf, 0)
    return action
