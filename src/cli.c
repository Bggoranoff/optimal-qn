#include <stdio.h>
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
        return solve_basic();
    }

    printf("Unknown command: %s\n", argv[1]);
    return 0;
}
