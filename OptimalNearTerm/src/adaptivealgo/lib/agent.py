from typing import List

class Agent:
    def __init__(self, n_states: int, n_actions: int):
        """
        Agent stores all the information about the current policy

        :param list[int] init_state: The state from which the agent starts
        """

        self.cur_value = 0
        self.n_states = n_states
        self.n_actions = n_actions

        self.policy = {}
        self.value = {}
    
    def get_value(self, state: List[int]) -> float:
        """
        Get the value of the state

        :param int state: The state whose value is to be returned
        :returns float: The value of the state
        """

        key = str(state)
        if key not in self.value:
            self.value[key] = 0
        
        return self.value[key]
    
    def set_value(self, state: List[int], value: float):
        """
        Set the value of the state

        :param int state: The state whose value is to be set
        :param float value: The value to set
        """

        key = str(state)
        self.value[key] = value
    
    def get_policy(self, state: List[int]) -> List[float]:
        """
        Get the policy for the state

        :param int state: The state whose policy is to be returned
        :returns list[float]: The policy for the state
        """

        key = str(state)
        if key not in self.policy:
            self.policy[key] = [1 / self.n_actions] * self.n_actions
        
        return self.policy[key]

    def set_policy(self, state: List[int], policy: List[float]):
        """
        Set the policy for the state

        :param int state: The state whose policy is to be set
        :param list[float] policy: The policy to set
        """

        key = str(state)
        self.policy[key] = policy
