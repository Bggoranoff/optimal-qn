#include <stdio.h>
#include "../lib/env.h"
#include "../lib/agent.h"
#include "policy_iter.h"

int policy_iter(const AdaptiveProtocolSystem *sys) {
    Environment *env = create_env(sys);
    printf(
        "n_links=%d\nf_thresh=%f\nn_actions=%d\nalpha=%f\ngamma=%f\ntol=%f\n",
        env->n_links, env->f_thresh, env->n_actions, env->alpha, env->gamma, sys->tol
    );

    printf("actions=[ ");
    for (int i = 0; i < env->n_actions; i++) {
        printf("%f ", env->actions[i]);
    }
    printf("]\n");

    int n_states = count_states(env);
    Agent *agent = create_agent(n_states, sys->n_actions);

    printf("n_states=%d\nn_actions=%d\n", agent->n_states, agent->n_actions);
    int state[] = {1, 2};
    set_value(agent, 2, state, 0.3);
    printf("V({1, 2}) = %f\n", get_value(agent, 2, state));

    set_policy(agent, 2, state, 0.4);
    printf("P({1, 2}) = %f\n", get_policy(agent, 2, state));

    int another_state[] = {1, 2, 3};
    printf("P({1, 2, 3}) = %f\n", get_policy(agent, 3, another_state));
    return 0;
}
