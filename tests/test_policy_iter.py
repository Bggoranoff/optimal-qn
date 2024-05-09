from adaptivealgo.policy_iter import calc_value, update_bellman
from adaptivealgo.env import Environment
from adaptivealgo.agent import Agent

def test_calc_value():
    env = Environment(n_links=2, ps=[0.1, 0.2], f_thresh=0.5, alpha=0.1, gamma=0.1)
    agent = Agent(2, 2)

    agent.set_value([], 1)
    agent.set_value([10], 3)

    state = [1]
    action = 0.1
    assert calc_value(env, agent, state, action) == -1 + (1 - action) * 1 + action * 3

def test_update_bellman():
    env = Environment(n_links=2, ps=[0.1, 0.2], f_thresh=0.5, alpha=0.1, gamma=0.1)
    agent = Agent(2, 2)

    agent.set_value([], 1)
    agent.set_value([10], 3)

    s_idx = 1
    update_bellman(env, agent, s_idx)

    expected = 0.5 * (-1 + (1 - 0.1) * 1 + 0.1 * 3) + 0.5 * (-1 + (1 - 0.2) * 1 + 0.2 * 3)
    assert agent.get_value([1]) == expected