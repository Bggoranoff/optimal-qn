#include <time.h>
#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include <float.h>
#include "../lib/env.h"
#include "../lib/agent.h"
#include "../lib/json.h"
#include "policy_iter.h"

int calc_m_links(int *state, int max_links) {
    int result = 0;
    for (int i = 0; i < max_links; i++) {
        if (state[i] == 0) {
            break;
        }

        result += 1;
    }

    return result;
}

float calc_value(Environment *env, Agent *agent, int m_links, int *state, float action) {
    if (action == 0) {
        return DEFAULT_VALUE;
    }

    int *fail_state = transition_fail(m_links, state);
    int *succ_state = transition_succ(env, m_links, state, action);

    int m_links_fail = calc_m_links(fail_state, m_links);
    int m_links_succ = calc_m_links(succ_state, m_links + 1);


    float val_fail = get_value(agent, m_links_fail, fail_state);
    float val_succ = get_value(agent, m_links_succ, succ_state);

    return -1.0f + (1 - action) * val_fail + action * val_succ;
}

void update_bellman(Environment *env, Agent *agent, int m_links, int s_idx) {
    int *state = env->states[m_links][s_idx];
    float action = get_policy(agent, m_links, state);

    float value = calc_value(env, agent, m_links, state, action);
    set_value(agent, m_links, state, value);
}

void eval_policy(Environment *env, Agent *agent, float tol) {
    float delta = FLT_MAX;
    int its = 0;
    
    while (delta >= tol) {
        delta = -1;

        for (int m_links = env->n_links - 1; m_links >= 0; m_links--) {
            for (int i = 0; i < env->st_per_lev[m_links]; i++) {
                float old_val = get_value(agent, m_links, env->states[m_links][i]);
                update_bellman(env, agent, m_links, i);
                float new_val = get_value(agent, m_links, env->states[m_links][i]);

                delta = fmax(delta, fabs(old_val - new_val));
            }
        }
    }
}

void update_policy(Environment *env, Agent *agent, int m_links, int s_idx) {
    int *state = env->states[m_links][s_idx];
    float best_action = get_policy(agent, m_links, state);
    float best_value = get_value(agent, m_links, state);

    for (int i = 0; i < env->n_actions; i++) {
        float action = env->actions[i];
        if (get_ttl_env(env, action) < env->n_links - m_links) {
            continue;
        }

        float value = calc_value(env, agent, m_links, state, action);

        best_action = value > best_value ? action : best_action;
        best_value = value > best_value ? value : best_value;
    }

    set_policy(agent, m_links, state, best_action);
}

bool improve_policy(Environment *env, Agent *agent) {
    bool policy_stable = true;

    for (int m_links = env->n_links - 1; m_links >= 0; m_links--) {
        for (int i = 0; i < env->st_per_lev[m_links]; i++) {
            int *state = env->states[m_links][i];
            float old_action = get_policy(agent, m_links, state);
            update_policy(env, agent, m_links, i);
            float new_action = get_policy(agent, m_links, state);

            if (old_action != new_action) {
                policy_stable = false;
            }
        }
    }

    return policy_stable;
}

void output_policy(Environment *env, Agent *agent, const char *output_path) {
    int json_size = (env->n_links + 20) * agent->n_states;
    char *policy_json = (char*) malloc(json_size * sizeof(char));
    serialise_hashmap(agent->policy, policy_json);

    char *value_json = (char*) malloc(json_size * sizeof(char));
    serialise_hashmap(agent->value, value_json);

    HashMap *params = create_hashmap(PARAMS_SIZE);
    insert_data(params, "n_links", (float) env->n_links);
    insert_data(params, "n_actions", (float) env->n_actions);
    insert_data(params, "alpha", env->alpha);
    insert_data(params, "gamma", env->gamma);
    insert_data(params, "f_thresh", env->f_thresh);

    char *params_json = (char*) malloc(PARAMS_SIZE * 20 * sizeof(char));
    serialise_hashmap(params, params_json);

    char *output_json = (char*) malloc((2 * json_size + PARAMS_SIZE * 20) * sizeof(char));
    serialise_system(policy_json, value_json, params_json, output_json);

    if (output_path == NULL) {
        printf("%s\n", output_json);
    } else {
        adx_store_data(output_path, output_json);
    }

    free(value_json);
    free(policy_json);
    free(params_json);
}

void adx_store_data(const char *filepath, const char *data) {
    FILE *fp = fopen(filepath, "w");
    if (fp != NULL) {
        fputs(data, fp);
        fclose(fp);
    }
}

int policy_iter(const AdaptiveProtocolSystem *sys) {
    Environment *env = create_env(sys);
    int n_states = count_states(env);
    Agent *agent = create_agent(n_states, sys->n_actions);

    bool policy_stable = false;
    int iter = 0;
    clock_t start = clock();

    while (!policy_stable) {
        iter += 1;
        eval_policy(env, agent, sys->tol);
        policy_stable = improve_policy(env, agent);
    }

    clock_t end = clock();
    printf("Policy iteration complete within %d iterations!\n", iter);
    printf("Policy iteration took %.5f seconds!\n", ((float) end - start) / CLOCKS_PER_SEC);
    output_policy(env, agent, "./output.json");
    return 0;
}
