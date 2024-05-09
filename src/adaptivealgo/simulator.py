import numpy as np

from adaptivealgo.state import State
from adaptivealgo.util import get_ttl


class Simulator:
    def __init__(self, policy: dict, n_links: int, f_thresh: float, actions: list[float], alpha: float, gamma: float):
        """
        Simulator for the MDP policy iteration

        :param dict policy: The policy of the agent
        :param int n_links: The number of links required in the near-term network
        :param float f_thresh: The minimum fidelity threshold
        :param list[float] actions: The generation protocol probabilities
        :param float alpha: Relationship between probability and fidelity F_i = 1 - alpha * p_i
        :param float gamma: Memory decay parameter
        """
        
        self.policy = policy
        self.n_links = n_links
        self.f_thresh = f_thresh
        self.actions = actions
        self.alpha = alpha
        self.gamma = gamma
    
    def get_next_state(self, state: State, action: float) -> State:
        """
        Get the next state given the current state and action

        :param State state: The current state
        :param float action: The action
        :returns State: The next state
        """
        
        rnd = np.random.rand()

        state = [ttl - 1 for ttl in state if ttl > 1]
        if rnd < action:
            ttl = get_ttl(action, self.alpha, self.f_thresh, self.gamma)
            state = sorted(state + [ttl])
        
        return state

    def run(self) -> int:
        """
        Run the simulation

        :returns int: The number of steps
        """
        
        state = []
        steps = 0
        while len(state) < self.n_links:
            action_idx = self.policy[str(state)]
            action = self.actions[action_idx]
            state = self.get_next_state(state, action)
            steps += 1
        
        return steps