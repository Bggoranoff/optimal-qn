#ifndef POLICY_ITER
#define POLICY_ITER

#include "../lib/env.h"
#include "../lib/agent.h"
#include <float.h>
#include <stdbool.h>

static const float DEFAULT_VALUE = -FLT_MAX + 1;

static const int PARAMS_SIZE = 5;

int policy_iter(const AdaptiveProtocolSystem *sys);

int calc_m_links(int *state, int max_links);

float calc_value(Environment *env, Agent *agent, int m_links, int *state, float action);

void update_bellman(Environment *env, Agent *agent, int m_links, int s_idx);

void eval_policy(Environment *env, Agent *agent, float tol);

void update_policy(Environment *env, Agent *agent, int m_links, int s_idx);

bool improve_policy(Environment *env, Agent *agent);

void output_policy(Environment *env, Agent *agent, const char *output_path);

#endif

