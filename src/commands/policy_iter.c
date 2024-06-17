#include <stdio.h>
#include "policy_iter.h"

int policy_iter(AdaptiveProtocolSystem sys) {
    printf(
        "n_links=%d\nf_thresh=%f\nn_actions=%d\nalpha=%f\ngamma=%f\ntol=%f\n",
        sys.n_links, sys.f_thresh, sys.n_actions, sys.alpha, sys.gamma, sys.tol
    );
    printf("actions=[ ");
    for (int i = 0; i < sys.n_actions; i++) {
        printf("%f ", sys.actions[i]);
    }
    printf("]\n");
    return 0;
}
