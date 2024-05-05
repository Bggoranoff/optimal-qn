class Agent:
    def __init__(self, init_state: list[int]):
        """
        Agent stores all the information about the current policy
        """

        self.cur_value = 0
        self.visited_states = [init_state]
        self.cur_state = init_state
