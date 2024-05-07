from argparse import ArgumentParser
from typing import List

import numpy as np

from adaptivealgo import cli_main
from adaptivealgo.util import get_ttl

def build_argument_parser() -> ArgumentParser:
    """
    Construct argument parser for basic solver

    :return: The argument parser
    """

    parser = ArgumentParser(
        description="""
        solve_basic: solves the optimal resource generation policy problem for
        a near-term quantum network with 2 required links.
        """
    )
    
    parser.add_argument(
        "--thresh",
        dest="f_thresh",
        type=float,
        help="Minimum fidelity threshold.",
    )
    parser.add_argument(
        "--actions",
        dest="actions",
        type=str,
        help="Comma-separated list of probabilities.",
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

    return (1 / first_p) + (1 / (second_p * (1 - (1 - second_p) ** (ttl - 1))))

def build_policy(max_ttl: int, expected_times: list[float]) -> dict:
    """
    Build the policy for a given state

    :param int max_ttl: The maximum time-to-live of the link
    :param list[float] expected_times: The expected times for each action
    :return: The policy for the state
    """

    result = {
        "[]": [1.0, 0] if expected_times[0] < expected_times[1] else [0, 1.0],
    }

    for t in range(1, max_ttl + 1):
        result[f"[{t}]"] = [0, 1.0] if expected_times[0] < expected_times[1] else [1.0, 0]
    
    return result

def print_policy(policy: dict):
    """
    Print the policy of the agent

    :param dict policy: The policy of the agent
    """

    print("Final policy:")
    for state in policy:
        print(f"State {state}: {policy[state]}")

def run(f_thresh: float, actions: str, alpha: float, gamma: float):
    """
    Solve the optimal policy problem for s=2 required links in memory

    :param float f_thresh: The minimum fidelity threshold
    :param str actions: The list of probabilities
    :param float alpha: The relationship between probability and fidelity
    :param float gamma: The memory decay constant
    """

    ps = [float(p) for p in actions.replace(" ", "").split(",")]
    assert len(ps) == 2, "Only two actions are supported"

    ts = [get_ttl(p, alpha, f_thresh, gamma) for p in ps]

    expected_times = [
        calc_expected_time(ps[0], ps[1], ts[0]),
        calc_expected_time(ps[1], ps[0], ts[1]),
    ]

    final_policy = build_policy(np.max(ts), expected_times)
    print_policy(final_policy)

def main():
    cli_main(build_argument_parser, run)
