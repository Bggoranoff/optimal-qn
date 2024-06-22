#ifndef AGENT_H
#define AGENT_H

#include "env.h"
#include "hashmap.h"

typedef struct Agent {
    int n_states;
    int n_actions;
    HashMap *policy;
    HashMap *value;
} Agent;

Agent* create_agent(int n_states, int n_actions);

float get_value(Agent *agent, int m_links, int *state);

void set_value(Agent *agent, int m_links, int *state, float value);

float get_policy(Agent *agent, int m_links, int *state);

void set_policy(Agent *agent, int m_links, int *state, float action);

char* to_string(int m_links, int *state);

#endif
