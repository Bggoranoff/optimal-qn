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
        self.ps = ps
        self.fs = [1 - alpha * p_i for p_i in self.ps]
        self.ttls = [self.get_ttl(f_i) for f_i in self.fs]
        self.max_ttl = np.max(self.ttls)

    def get_ttl(self, f_i: float):
        """
        Calculates the TTL of a link in memory with a certain fidelity using
        exponential decay model

        :param float f_i: The initial fidelity of the link
        :param float f_thresh: The minimum fidelity threshold
        :param float gamma: The memory decay rate constant
        :returns int: TTL of link with initial fidelity `f_i`
        """

        return np.floor(np.log((f_i - F_MIN) / (self.f_thresh - F_MIN)) / self.gamma)
