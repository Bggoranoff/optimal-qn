import argparse

from adaptivealgo import cli_main
from adaptivealgo.agent import Agent
from adaptivealgo.env import Environment

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

def eval_policy(env: Environment, agent: Agent):
    """
    Policy evaluation step
    """

    pass

def improve_policy(env: Environment, agent: Agent):
    """
    Policy improvement step
    """

    pass

def update_bellman(env: Environment, agent: Agent):
    """
    Update the value of a policy using the Bellman equation
    """

    pass

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
    env = Environment(n_links, ps, f_thresh, alpha, gamma)

    print(env.ps)
    print(env.fs)

    pass

def main():
    cli_main(build_argument_parser, run)
