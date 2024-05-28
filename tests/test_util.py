import numpy as np
from adaptivealgo.lib.constants import F_MIN
from adaptivealgo.lib.util import get_ttl


def test_get_ttl():
    assert get_ttl(0.1, 0.1, 0.5, 0.1) == 11

def test_get_ttl_fmin():
    assert get_ttl(0.1, 0.1, F_MIN, 0.1) == np.inf