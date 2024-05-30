from adaptivealgo.lib.constants import F_MIN

import numpy as np

def get_ttl(p_i: float, alpha: float, f_thresh: float, gamma: float) -> int:
    """
    Calculates the TTL of a link in memory with a certain fidelity using
    exponential decay model

    :param float p_i: The success probability of entanglement generation
    :param float alpha: The relationship between probability and fidelity
    :param float f_thresh: The minimum fidelity threshold
    :param float gamma: The memory decay parameter
    :returns int: TTL of link generated with probability `p_i`
    """

    assert 0 <= p_i <= 1, f"p_i={p_i}"
    # assert 1 - alpha * p_i >= F_MIN, f"p_i={p_i}, alpha={alpha}, F_MIN={F_MIN}"
    assert f_thresh >= F_MIN, f"f_thresh={f_thresh}, F_MIN={F_MIN}"

    if f_thresh == F_MIN:
        return np.inf
    
    if 1 - alpha * p_i < F_MIN:
        return 0

    return int(np.floor(np.log((1 - alpha * p_i - F_MIN) / (f_thresh - F_MIN)) / gamma))

def trim_state(state: list[int], n_links: int) -> list[int]:
    """
    Remove the links that will never survive for the given number of links
    required in memory

    :param list[int] state: The state
    :param int n_links: The number of links required
    :returns list[int]: The trimmed state
    """

    prev_state = state
    state = [ttl for ttl in state if ttl >= n_links - len(state)]

    while len(prev_state) != len(state):
        prev_state = state
        state = [ttl for ttl in state if ttl >= n_links - len(state)]

    return state