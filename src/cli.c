#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "cli.h"
#include "commands/policy_iter.h"
#include "commands/simulate_policy.h"
#include "commands/solve_basic.h"

int cli_main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Usage: %s <command> [options]\n", argv[0]);
        return 1;
    }

    if (strcmp(argv[1], "policyIter") == 0) {
        return policy_iter();
    } else if (strcmp(argv[1], "simulatePolicy") == 0) {
        return simulate_policy();
    } else if (strcmp(argv[1], "solveBasic") == 0) {
        TwoProtocolSystem sys = {
            .f_thresh = atof(argv[2]),
            .p_1 = atof(argv[3]),
            .p_2 = atof(argv[4]),
            .alpha = atof(argv[5]),
            .gamma = atof(argv[6]),
        };

        return solve_basic(sys);
    }

    printf("Unknown command: %s\n", argv[1]);
    return 0;
}
