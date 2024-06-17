#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
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
        if (argc < 8) {
            printf("Required number of arguments for policyIter is 9\n");
            return 1;
        }

        int n_links = atoi(argv[2]);
        float f_thresh = atof(argv[3]);

        int n_actions = count_numbers(argv[4]);
        float *actions = (float*) malloc(n_actions * sizeof(float));
        parse_numbers(argv[4], actions, n_actions);
        
        float alpha = atof(argv[5]);
        float gamma = atof(argv[6]);
        float tol = atof(argv[7]);

        AdaptiveProtocolSystem sys = {
            .n_links = n_links,
            .n_actions = n_actions,
            .f_thresh = f_thresh,
            .actions = actions,
            .alpha = alpha,
            .gamma = gamma,
            .tol = tol,
        };

        return policy_iter(sys);
    } else if (strcmp(argv[1], "simulatePolicy") == 0) {
        return simulate_policy();
    } else if (strcmp(argv[1], "solveBasic") == 0) {
        if (argc < 7) {
            printf("Required number of arguments for solveBasic is 5\n");
            return 1;
        }

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
    return 1;
}


void parse_numbers(char *input, float *numbers, int num_count) {
    if (numbers == NULL) {
        return;
    }

    int count = 0;
    char* token = strtok(input, ",");

    while (token != NULL && count < num_count) {
        while (*token == ' ') {
            token += 1;
        }

        numbers[count++] = atof(token);
        token = strtok(NULL, ",");
    }
}

int count_numbers(const char *input) {
    int count = 0;
    bool in_num = false;

    for (const char *p = input; *p != '\0'; p++) {
        if (isdigit(*p)) {
            if (!in_num) {
                count += 1;
                in_num = true;
            }
        } else if (*p == ',' || *p == ' ') {
            in_num = 0;
        }
    }

    return count;
}
