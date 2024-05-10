import numpy as np
from adaptivealgo.cli.solve_basic import build_policy, calc_expected_time

def test_calc_expected_time():
    expected = calc_expected_time(0.1, 0.2, 5)
    assert np.isclose(expected, 18.47, atol=1e-2)

def test_calc_expected_time_first_zero():
    expected = calc_expected_time(0, 0.2, 5)
    assert expected == np.inf

def test_calc_expected_time_second_zero():
    expected = calc_expected_time(0.1, 0, 5)
    assert expected == np.inf

def test_calc_expected_time_ttl_one():
    expected = calc_expected_time(0.1, 0.2, 1)
    assert expected == np.inf

def test_build_policy():
    expected = build_policy(5, [5.47, 13.11])
    assert expected == {
        "[]": [1.0, 0],
        "[1]": [0, 1.0],
        "[2]": [0, 1.0],
        "[3]": [0, 1.0],
        "[4]": [0, 1.0],
        "[5]": [0, 1.0],
    }