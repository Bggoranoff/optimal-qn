from adaptivealgo.agent import Agent

def test_get_value_no_value():
    agent = Agent(2, 2)
    state = [0]
    assert agent.get_value(state) == 0

def test_set_value():
    agent = Agent(2, 2)
    state = [0]
    agent.set_value(state, 1)
    assert agent.get_value(state) == 1

def test_get_policy_no_policy():
    agent = Agent(2, 2)
    state = [0]
    assert agent.get_policy(state) == [0.5, 0.5]

def test_set_policy():
    agent = Agent(2, 2)
    state = [0]
    agent.set_policy(state, [0.3, 0.7])
    assert agent.get_policy(state) == [0.3, 0.7]