import math
import numpy as np

class Agent:
    def __init__(self, n_links: int, n_actions: int, max_ttl: int):
        """
        Agent stores all the information about the current policy

        :param list[int] init_state: The state from which the agent starts
        """

        self.cur_value = 0
        self.n_states = self.calc_num_states(n_links, max_ttl)
        self.n_actions = n_actions

        self.policy = self.gen_init_policy()

    def calc_num_states(self, n_links: int, max_ttl: int) -> int:
        """
        Given a number of links that need to be generated and the maximum
        possible TTL of a link, calculate the number of states in the MDP

        :param int n_links: Required number of links in the network
        :param int max_ttl: Maximum possible TTL of a generated link
        :returns int: Number of states in the MDP
        """

        return math.factorial(max_ttl + n_links) // (math.factorial(max_ttl) * math.factorial(n_links))

    def gen_init_policy(self):
        """
        Generate equiprobable policy for each state in the MDP

        :returns list[list[float]]: List of probabilities for each state
        """

        return (1 / self.n_actions) * np.ones((self.n_states, self.n_actions))
