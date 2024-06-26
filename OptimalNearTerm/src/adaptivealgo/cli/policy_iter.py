import argparse
import json
from typing import List
import numpy as np
import time
import wandb

from adaptivealgo.cli import cli_main
from adaptivealgo.lib.agent import Agent
from adaptivealgo.lib.env import Environment
from adaptivealgo.lib.state import State

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
        default="0.3",
        help="Minimum fidelity threshold (F_thresh).",
    )
    parser.add_argument(
        "--actions",
        dest="actions",
        type=str,
        default="0.1, 0.7",
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
        default="0.1",
        help="Fixed parameter specifying exponential memory decay.",
    )
    parser.add_argument(
        "--tol",
        dest="tol",
        type=float,
        default="1e-20",
        help="Tolerance at which the policy is considered stable.",
    )
    parser.add_argument(
        "--output",
        dest="output_path",
        type=str,
        default=None,
        help="Path to save the policy.",
    )
    return parser

def eval_policy(env: Environment, agent: Agent, tol: float):
    """
    Policy evaluation step

    :param Environment env: The environment object
    :param Agent agent: The agent object
    :param float tol: The tolerance at which the policy is considered stable
    """

    delta = np.inf

    while delta >= tol:
        delta = -np.inf
        for s_idx in range(agent.n_states):
            if env.is_terminal(env.states[s_idx]):
                continue

            old_value = agent.get_value(env.states[s_idx])
            update_bellman(env, agent, s_idx)
            delta = max(delta, np.abs(agent.get_value(env.states[s_idx]) - old_value))

def update_policy(env: Environment, agent: Agent, s_idx: int):
    """
    Update the policy of a state

    :param Environment env: The environment object
    :param Agent agent: The agent object
    :param int s_idx: The index of the state in the list of states
    """

    state = env.states[s_idx]
    best_action = None
    best_value = -np.inf

    for a_idx in range(agent.n_actions):
        action = env.actions[a_idx]
        if env.get_ttl(action) < env.n_links - len(state):
            continue

        value = calc_value(env, agent, state, action)

        best_action = a_idx if value > best_value else best_action
        best_value = value if value > best_value else best_value

    new_policy = [0 for _ in range(agent.n_actions)]
    new_policy[best_action] = 1
    agent.set_policy(state, new_policy)

def improve_policy(env: Environment, agent: Agent) -> bool:
    """
    Policy improvement step

    :param Environment env: The environment object
    :param Agent agent: The agent object
    :returns bool: Whether the policy is stable
    """

    policy_stable = True

    for s_idx in range(agent.n_states):
        if env.is_terminal(env.states[s_idx]):
            continue

        old_policy = agent.get_policy(env.states[s_idx])
        update_policy(env, agent, s_idx)
        new_policy = agent.get_policy(env.states[s_idx])

        if not np.array_equal(old_policy, new_policy):
            policy_stable = False

    return policy_stable

def calc_value(env: Environment, agent: Agent, state: State, action: float) -> float:
    """
    Calculate the value of a state-action pair

    :param Environment env: The environment object
    :param State state: The state
    :param float action: The action
    """

    fail_state, succ_state = env.transition(state, action)
    return -1 + (1 - action) * agent.get_value(fail_state) + action * agent.get_value(succ_state)

def update_bellman(env: Environment, agent: Agent, s_idx: int):
    """
    Update the value of a policy using the Bellman equation

    :param Environment env: The environment object
    :param Agent agent: The agent object
    :param int s_idx: The index of the state in the list of states
    """

    state = env.states[s_idx]
    value = 0

    for a_idx in range(agent.n_actions):
        action = env.actions[a_idx]
        if env.get_ttl(action) < env.n_links - len(state):
            continue

        prob = agent.get_policy(state)[a_idx]
        value += prob * calc_value(env, agent, state, action)

    agent.set_value(state, value)

def print_policy(agent: Agent, env: Environment):
    """
    Print the policy of the agent

    :param Agent agent: The agent object
    :param Environment env: The environment object
    """

    print("Final policy:")
    for state in env.states:
        if env.is_terminal(state):
            continue

        print(f"State {state}: {agent.get_policy(state)}")

def build_policy_dict(agent: Agent, env: Environment) -> dict:
    """
    Build a dictionary representation of the policy

    :param Agent agent: The agent object
    :param Environment env: The environment object
    :returns dict: The policy dictionary
    """

    policy = {}
    for state in env.states:
        if env.is_terminal(state):
            continue

        policy[str(state)] = int(np.argmax(agent.get_policy(state)))
    
    return policy

def find_policy(n_links: int, f_thresh: float, ps: List[float], alpha: float, gamma: float, tol: float, to_print: bool=False) -> dict:
    env = Environment(n_links, ps, f_thresh, alpha, gamma)
    agent = Agent(n_states=len(env.states), n_actions=len(ps))

    policy_stable = False
    i = 0

    while not policy_stable:
        i += 1
        eval_policy(env, agent, tol)
        policy_stable = improve_policy(env, agent)

    policy = build_policy_dict(agent, env)
    result = {
        "n_links": env.n_links,
        "f_thresh": env.f_thresh,
        "actions": env.actions,
        "alpha": env.alpha,
        "gamma": env.gamma,
        "policy": policy,
    }

    if to_print:
        print("Final values:")
        for state in env.states:
            print(f"State {state}: E[t] = {-agent.get_value(state)}")
        print_policy(agent, env)

    return result, i

def run(n_links: int, f_thresh: float, actions: str, alpha: float, gamma: float, tol: float, output_path: str):
    """
    Perform policy iteration given the command-line arguments

    :param int n_links: Target required number of links in the network
    :param float f_thresh: Minimum fidelity threshold
    :param str actions: Comma-separated list of probabilities
    :param float alpha: Specifies relationship between probablity and fidelity
    :param float gamma: Exponential memory decay constant
    """

    ps = [float(p) for p in actions.replace(" ", "").split(",")]

    wandb.init(
        project="adaptive-algorithms",
        config={
            "n_links": n_links,
            "f_thresh": f_thresh,
            "actions": ps,
            "alpha": alpha,
            "gamma": gamma,
            "tol": tol,
        }
    )
    
    start_time = time.process_time()
    policy, i = find_policy(n_links, f_thresh, ps, alpha, gamma, tol, to_print=not output_path)
    end_time = time.process_time()

    wandb.log({"policy_iterations": i, "time": end_time - start_time})
    wandb.finish()

    print(f"Policy iteration converged after {i} steps for {end_time - start_time} seconds")
    if output_path:
        with open(output_path, "w") as file:
            json.dump(policy, file)
    else:
        print(json.dumps(policy, indent=4))

def main():
    cli_main(build_argument_parser, run)
