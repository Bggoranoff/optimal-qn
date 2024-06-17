#ifndef ENV_H
#define ENV_H

typedef struct TwoProtocolSystem {
    float f_thresh;
    float p_1;
    float p_2;
    float alpha;
    float gamma;
} TwoProtocolSystem;

typedef struct LevelInfo {
    int **buffer;
    int next_state;
    int m_links;
} LevelInfo;

typedef struct AdaptiveProtocolSystem {
    int n_links;
    float f_thresh;
    int n_actions;
    float* actions;
    float alpha;
    float gamma;
    float tol;
} AdaptiveProtocolSystem;

typedef struct Environment {
    int n_links;
    float f_thresh;
    float gamma;
    float alpha;
    int n_actions;
    float *actions;
    int max_ttl;
    int *st_per_lev;
    int ***states;
} Environment;

int count_level_states(int m_links, int max_ttl);

void gen_states(int min_ttl, int max_ttl, LevelInfo *info, int *cur_state, int next_link);

Environment *create_env(const AdaptiveProtocolSystem *sys);

int get_ttl_env(const Environment *env, float p_i);

int* transition_fail(int m_links, int *state);

int* transition_succ(Environment *env, int m_links, int *state, float action);

#endif
