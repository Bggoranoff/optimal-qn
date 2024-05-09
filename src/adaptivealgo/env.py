import numpy as np

from adaptivealgo.constants import F_MIN

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

    def get_ttl(self, p_i: float):
        """
        Calculates the TTL of a link in memory with a certain fidelity using
        exponential decay model

        :param float p_i: The success probability of entanglement generation 
        :returns int: TTL of link generated with probability `p_i`
        """

        return np.floor(np.log((1 - self.alpha * p_i - F_MIN) / (self.f_thresh - F_MIN)) / self.gamma)

    def is_terminal(self, state: list[int]):
        """
        Checks whether a state is a terminal state, meaning that all links
        have been generated in memory
        """

        return len(state) == self.n_links
