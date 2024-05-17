from argparse import ArgumentParser

import numpy as np

from adaptivealgo.cli import cli_main
from adaptivealgo.lib.util import get_ttl

def build_argument_parser() -> ArgumentParser:
    """
    Construct argument parser for basic solver

    :return: The argument parser
    """

    parser = ArgumentParser(
        description="""
        solve_basic: solves the optimal resource generation policy problem for
        a near-term quantum network with 2 required links with protocols p1 < p2.
        """
    )
    
    parser.add_argument(
        "--thresh",
        dest="f_thresh",
        type=float,
        help="Minimum fidelity threshold.",
    )
    parser.add_argument(
        "--p1",
        dest="p_1",
        type=float,
        help="Smaller probability of the two actions.",
    )
    parser.add_argument(
        "--p2",
        dest="p_2",
        type=float,
        help="Larger probability of the two actions.",
    )
    parser.add_argument(
        "--alpha",
        dest="alpha",
        type=float,
        help="Specifies relationship between probablity and fidelity.",
    )
    parser.add_argument(
        "--gamma",
        dest="gamma",
        type=float,
        help="Exponential memory decay constant.",
    )

    return parser

def calc_expected_time(first_p: float, second_p: float, ttl: float) -> float:
    """
    Evaluate the policy for a given state

    :param float first_p: The probability of the first action
    :param float second_p: The probability of the second action
    :param float ttl: The time-to-live of the link
    :return: The value of the policy
    """

    assert 0 <= first_p <= 1, f"first_p={first_p}"
    assert 0 <= second_p <= 1, f"second_p={second_p}"

    if first_p == 0 or second_p == 0 or ttl <= 1:
        return np.inf

    return (1 / second_p) + (1 / (first_p * (1 - (1 - second_p) ** (ttl - 1))))

def build_policy(max_ttl: int, et_12: float, et_22: float) -> dict:
    """
    Build the policy for a given state

    :param int max_ttl: The maximum time-to-live of the link
    :param float et_12: The expected time for the first policy
    :param float et_22: The expected time for the second policy
    :return: The policy for the state
    """

    result = {
        "[]": [1.0, 0] if et_12 < et_22 else [0, 1.0],
    }

    for t in range(1, max_ttl + 1):
        result[f"[{t}]"] = [0, 1.0]
    
    return result

def print_policy(policy: dict):
    """
    Print the policy of the agent

    :param dict policy: The policy of the agent
    """

    print("Final policy:")
    for state in policy:
        print(f"State {state}: {policy[state]}")

def run(f_thresh: float, p_1: float, p_2: float, alpha: float, gamma: float):
    """
    Solve the optimal policy problem for s=2 required links in memory

    :param float f_thresh: The minimum fidelity threshold
    :param float p_1: The smaller probability of the two actions
    :param float p_2: The larger probability of the two actions
    :param float alpha: The relationship between probability and fidelity
    :param float gamma: The memory decay constant
    """
    
    assert p_1 < p_2, f"p_1={p_1} >= p_2={p_2}"
    
    t_1 = get_ttl(p_1, alpha, f_thresh, gamma)
    t_2 = get_ttl(p_2, alpha, f_thresh, gamma)

    et_12 = calc_expected_time(p_1, p_2, t_1)
    et_22 = calc_expected_time(p_2, p_2, t_2)

    print(f"Expected time for policy 1, 2: {et_12}")
    print(f"Expected time for policy 2, 2: {et_22}")

    final_policy = build_policy(t_1, et_12, et_22)
    print_policy(final_policy)

def main():
    cli_main(build_argument_parser, run)
