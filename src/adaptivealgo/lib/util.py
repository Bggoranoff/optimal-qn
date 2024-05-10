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
    assert 1 - alpha * p_i >= F_MIN, f"p_i={p_i}, alpha={alpha}, F_MIN={F_MIN}"
    assert f_thresh >= F_MIN, f"f_thresh={f_thresh}, F_MIN={F_MIN}"

    if f_thresh == F_MIN:
        return np.inf

    return int(np.floor(np.log((1 - alpha * p_i - F_MIN) / (f_thresh - F_MIN)) / gamma))