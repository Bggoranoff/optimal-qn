from adaptivealgo.lib.env import Environment
import math

def test_get_states():
    env = Environment(n_links=2, ps=[0.1, 0.2], f_thresh=0.5, alpha=0.1, gamma=0.1)
    states = env.gen_states(n_links=4, max_ttl=5)
    expected = math.factorial(9) / (math.factorial(4) * math.factorial(5))
    assert len(states) == expected

def test_get_states_empty():
    env = Environment(n_links=2, ps=[0.1, 0.2], f_thresh=0.5, alpha=0.1, gamma=0.1)
    states = env.gen_states(n_links=0, max_ttl=0)
    assert len(states) == 1

def test_get_states_single():
    env = Environment(n_links=2, ps=[0.1, 0.2], f_thresh=0.5, alpha=0.1, gamma=0.1)
    states = env.gen_states(n_links=1, max_ttl=1)
    print(states)
    assert len(states) == 2

def test_get_ttl():
    env = Environment(n_links=2, ps=[0.1, 0.2], f_thresh=0.5, alpha=0.1, gamma=0.1)
    assert env.get_ttl(0.1) == 10

def test_is_terminal_true():
    env = Environment(n_links=2, ps=[0.1, 0.2], f_thresh=0.5, alpha=0.1, gamma=0.1)
    assert env.is_terminal([1, 2]) == True

def test_is_terminal_false():
    env = Environment(n_links=2, ps=[0.1, 0.2], f_thresh=0.5, alpha=0.1, gamma=0.1)
    assert env.is_terminal([1]) == False

def test_transition():
    env = Environment(n_links=2, ps=[0.1, 0.2], f_thresh=0.5, alpha=0.1, gamma=0.1)
    assert env.transition([1], 0.1) == ([], [10])