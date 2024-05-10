from argparse import ArgumentParser
import json

from adaptivealgo.cli import cli_main
from adaptivealgo.lib.simulator import Simulator


def build_argument_parser():
    """
    Define the command-line arguments for running policy iteration
    """

    parser = ArgumentParser(
        description="""
        simulate_policy: simulates the Markov decision process optimal policy
        and outputs number of steps.
        """
    )

    parser.add_argument(
        "--process",
        dest="input_path",
        type=str,
        default="./policy.json",
        help="Path to the policy file.",
    )
    parser.add_argument(
        "--iterations",
        dest="iterations",
        type=int,
        default=1000,
        help="Number of iterations to run the simulation.",
    )
    
    return parser

def import_json(input_path: str) -> dict:
    """
    Import the policy file

    :param str input_path: The path to the policy file
    :returns dict: The policy
    """
    
    with open(input_path, "r") as file:
        return json.load(file)

def simulate_policy(policy: dict, n_links: int, actions: list[float], f_thresh: float, alpha: float, gamma: float, iters: int) -> int:
    """
    Simulate the policy

    :param dict policy: The policy
    :param list[float] ps: The generation protocol probabilities
    :param float f_thresh: The minimum fidelity threshold
    :param float alpha: Relationship between probability and fidelity F_i = 1 - alpha * p_i
    :param float gamma: Memory decay parameter
    :returns int: The number of steps
    """

    sim = Simulator(policy, n_links, f_thresh, actions, alpha, gamma)
    result = 0

    for _ in range(iters):
        result += sim.run()
    
    return result // iters

def run(input_path: str, iterations: int):
    """
    Run the policy iteration algorithm

    :param str input_path: The path to the policy file
    """
    
    with open(input_path, "r") as file:
        args = json.load(file)
    
    n_links = args["n_links"]
    ps = args["actions"]
    f_thresh = args["f_thresh"]
    alpha = args["alpha"]
    gamma = args["gamma"]
    policy = args["policy"]

    steps = simulate_policy(policy, n_links, ps, f_thresh, alpha, gamma, iterations)
    print(f"Number of steps: {steps}")

def main():
    cli_main(build_argument_parser, run)