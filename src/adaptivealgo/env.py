from typing import List
import numpy as np

from adaptivealgo.constants import F_MIN
from adaptivealgo.state import State
from adaptivealgo.util import get_ttl

class Environment:
    def __init__(self, n_links: int, ps: list[float], f_thresh: float, alpha: float, gamma: float):
        """
        Environment for the MDP policy iteration

        :param int n_links: The number of links required in the near-term network
        :param list[float] ps: The generation protocol probabilities
        :param float f_thresh: The minimum fidelity threshold
        :param float alpha: Relationship between probability and fidelity F_i = 1 - alpha * p_i
        :param float gamma: Memory decay parameter
        """
        
        self.n_links = n_links
        self.f_thresh = f_thresh
        self.gamma = gamma
        self.alpha = alpha
        self.actions = ps
        self.states = self.gen_states(n_links, self.get_ttl(np.min(ps)))
    
    def gen_states(self, n_links: int, max_ttl: int) -> List[State]:
        """
        Generates all possible states in the MDP

        :param int n_links: The number of links required in the near-term network
        :param int max_ttl: The maximum TTL of a link in memory
        :returns List[State]: The list of states
        """

        states = []
        for m_links in range(n_links + 1):
            sub_states = self._gen_substates(m_links, 1, max_ttl, [], [])
            states.extend(sub_states)
        
        return states
    
    def _gen_substates(self, m_links: int, min_ttl: int, max_ttl: int, cur_state: State, states: list[State]):
        """
        Generates all possible substates in the MDP

        :param int m_links: The number of links in the current state
        :param int max_ttl: The maximum TTL of a link in memory
        :param State cur_state: The current state
        :param list[State] states: The list of states
        :returns list[State]: The list of states
        """

        if len(cur_state) == m_links:
            states.append(cur_state)
            return states

        if min_ttl >= max_ttl:
            return states
        
        for ttl in range(min_ttl, max_ttl + 1):
            new_state = cur_state + [ttl]
            self._gen_substates(m_links, ttl, max_ttl, new_state, states)
        
        return states

    def get_ttl(self, p_i: float) -> int:
        """
        Calculates the TTL of a link in memory with a certain fidelity using
        exponential decay model

        :param float p_i: The success probability of entanglement generation 
        :returns int: TTL of link generated with probability `p_i`
        """

        return get_ttl(p_i, self.alpha, self.f_thresh, self.gamma)

    def is_terminal(self, state: State):
        """
        Checks whether a state is a terminal state, meaning that all links
        have been generated in memory
        """

        return len(state) == self.n_links
    
    def transition(self, state: State, action: float):
        """
        Returns the next possible states given the current state and action

        :param State state: The current state
        :param float action: The action taken
        :returns State, State: The fail state and success state
        """

        fail_state = [ttl - 1 for ttl in state if ttl > 1]
        succ_state = sorted(fail_state + [self.get_ttl(action)])
        
        return fail_state, succ_state
