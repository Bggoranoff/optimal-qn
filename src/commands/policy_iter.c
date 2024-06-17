#include <stdio.h>
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
    return 0;
}
