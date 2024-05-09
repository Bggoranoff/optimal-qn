from adaptivealgo.util import get_ttl
from src.adaptivealgo.simulator import Simulator

policy = {
    "[]": [1.0, 0],
    "[1]": [0, 1.0],
    "[2]": [0, 1.0],
    "[3]": [0, 1.0],
    "[4]": [0, 1.0],
    "[5]": [0, 1.0],
}

def test_get_next_state():
    simulator = Simulator(policy, 4, 0.3, [0.1, 0.2], 1.0, 0.2)
    state = [2]
    action = 0.2
    next_state = simulator.get_next_state(state, action)
    assert next_state == [1] or next_state == [1, 11]