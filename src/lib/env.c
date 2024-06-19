#include <float.h>
#include <math.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include "utils.h"
#include "env.h"

int count_level_states(int m_links, int max_ttl) {
    int num = tgamma(max_ttl + m_links);
    int denom = tgamma(m_links + 1) * tgamma(max_ttl);

    return num / denom;
}

void gen_states(int min_ttl, int max_ttl, LevelInfo *info, int *cur_state, int next_link) {
    if (next_link == info->m_links) {
        memcpy(info->buffer[info->next_state], cur_state, info->m_links * sizeof(int));
        info->next_state += 1;
        return;
    }

    for (int ttl = min_ttl; ttl <= max_ttl; ttl++) {
        cur_state[next_link] = ttl;
        gen_states(ttl, max_ttl, info, cur_state, next_link + 1);
    }
}

float find_min_action(int n_actions, float *actions) {
    float result = FLT_MAX;

    for (int i = 0; i < n_actions; i++) {
        result = result > actions[i] ? actions[i] : result;
    }

    return result;
}

Environment *create_env(const AdaptiveProtocolSystem *sys) {
    Environment *result = (Environment*) malloc(sizeof(Environment));
    result->n_actions = sys->n_actions;
    result->n_links = sys->n_links;
    result->alpha = sys->alpha;
    result->gamma = sys->gamma;
    result->actions = sys->actions;
    result->f_thresh = sys->f_thresh;
    result->st_per_lev = (int*) malloc((sys->n_links + 1) * sizeof(int));

    float min_action = find_min_action(sys->n_actions, sys->actions);
    result->max_ttl = get_ttl(min_action, sys->alpha, sys->f_thresh, sys->gamma);

    for (int i = 0; i < sys->n_links + 1; i++) {
        result->st_per_lev[i] = count_level_states(i, result->max_ttl);
    }

    result->states = (int***) malloc((sys->n_links + 1) * sizeof(int**));
    for (int i = 0; i < sys->n_links + 1; i++) {
        result->states[i] = (int**) malloc(result->st_per_lev[i] * sizeof(int*));

        for (int j = 0; j < result->st_per_lev[i]; j++) {
            result->states[i][j] = (int*) malloc(i * sizeof(int));
        }

        LevelInfo info = {
            .buffer = result->states[i],
            .next_state = 0,
            .m_links = i
        };

        int *cur_state = (int*) malloc(i * sizeof(int));
        gen_states(1, result->max_ttl, &info, cur_state, 0);
        free(cur_state);
    }

    return result;
}

int get_ttl_env(const Environment *env, float p_i) {
    return get_ttl(p_i, env->alpha, env->f_thresh, env->gamma);
}

int* transition_fail(int m_links, int *state) {
    int *new_state = (int*) calloc(m_links, sizeof(int));
    int ni = 0;

    for (int i = 0; i < m_links; i++) {
        if (state[i] - 1 == 0) {
            continue;
        }

        new_state[ni++] = state[i] - 1;
    }

    return new_state;
}

int* transition_succ(Environment *env, int m_links, int *state, float action) {
    int new_ttl = get_ttl_env(env, action);
    int *new_state = (int*) calloc(m_links + 1, sizeof(int));
    int ni = 0;
    bool included = false;

    for (int i = 0; i < m_links; i++) {
        if (state[i] - 1 == 0) {
            continue;
        }

        if (new_ttl <= state[i] - 1 && !included) {
            new_state[ni++] = new_ttl;
            included = true;
        }

        new_state[ni++] = state[i] - 1;
    }

    if (!included) {
        new_state[ni] = new_ttl;
    }

    return new_state;
}

int count_states(Environment *env) {
    int result = 0;
    for (int i = 0; i < env->n_links + 1; i++) {
        result += env->st_per_lev[i];
    }
    return result;
}
