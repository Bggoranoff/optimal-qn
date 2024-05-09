import numpy as np
from adaptivealgo.constants import F_MIN
from adaptivealgo.util import get_ttl


def test_get_ttl():
    assert get_ttl(0.1, 0.1, 0.5, 0.1) == 10

def test_get_ttl_fmin():
    assert get_ttl(0.1, 0.1, F_MIN, 0.1) == np.inf