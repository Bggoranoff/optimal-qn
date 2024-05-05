import argparse
import numpy as np

from adaptivealgo import cli_main

F_MIN = 0.25
"""Minimal theoretical fidelity of two-state entanglement generation"""

def build_argument_parser():
    """
    Define the command-line arguments for running policy iteration
    """

    parser = argparse.ArgumentParser(
        description="""
        policy_iter: solves a Markov decision process to generate a required number of links
        in a near-term quantum network using an adaptive generation protocol.
        """
    )
    parser.add_argument(
        "--links",
        dest="n_links",
        type=int,
        default="2",
        help="Number of required links in the network.",
    )
    parser.add_argument(
        "--thresh",
        dest="f_thresh",
        type=float,
        default="0.4",
        help="Minimum fidelity threshold (F_thresh).",
    )
    parser.add_argument(
        "--actions",
        dest="actions",
        type=str,
        default="0.3, 0.5",
        help="Comma-separated list of protocol probabilities of success (e.g. 0.25, 0.5, 0.75).",
    )
    parser.add_argument(
        "--alpha",
        dest="alpha",
        type=float,
        default="1.0",
        help="Defines mapping between probability and fidelity F_i = 1 - alpha * p_i",
    )
    parser.add_argument(
        "--gamma",
        dest="gamma",
        type=float,
        default="0.2",
        help="Fixed parameter specifying exponential memory decay.",
    )
    return parser

def get_ttl(f_i: float, f_thresh: float, gamma: float):
    """
    Calculates the TTL of a link in memory with a certain fidelity using
    exponential decay model

    :param float f_i: The initial fidelity of the link
    :param float f_thresh: The minimum fidelity threshold
    :param float gamma: The memory decay rate constant
    :returns int: TTL of link with initial fidelity `f_i`
    """

    return np.floor(np.log((f_i - F_MIN) / (f_thresh - F_MIN)) / gamma)

def run(n_links: int, f_thresh: float, actions: str, alpha: float, gamma: float):
    """
    Perform policy iteration given the command-line arguments

    :param int n_links: Target required number of links in the network
    :param float f_thresh: Minimum fidelity threshold
    :param str actions: Comma-separated list of probabilities
    :param float alpha: Specifies relationship between probablity and fidelity
    :param float gamma: Exponential memory decay constant
    """

    ps = [float(p) for p in actions.replace(" ", "").split(",")]
    fs = [1 - alpha * p_i for p_i in ps]
    ttls = [get_ttl(f_i, f_thresh, gamma) for f_i in fs]
    max_ttl = np.max(ttls)

    print(f"Performing policy iteration for {n_links} links")
    print(ps)
    print(fs)
    print(ttls)
    print(max_ttl)

    pass

def main():
    cli_main(build_argument_parser, run)
