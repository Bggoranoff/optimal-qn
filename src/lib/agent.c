#include "agent.h"
#include "hashmap.h"
#include <stdio.h>
#include <stdlib.h>

Agent* create_agent(int n_states, int n_actions) {
    Agent *agent = (Agent*) malloc(sizeof(Agent));

    agent->n_states = n_states;
    agent->n_actions = n_actions;

    agent->policy = create_hashmap(n_states);
    agent->value = create_hashmap(n_states);

    return agent;
}

char* to_string(int m_links, int *state) {
    int key_size = 2 + m_links + 2 * (m_links - 1);
    char *result = (char*) malloc(key_size + 1);

    if (result == NULL) {
        return NULL;
    }

    char *ptr = result;
    *ptr++ = '[';
    for (int i = 0; i < m_links; i++) {
        if (i > 0) {
            *ptr++ = ',';
            *ptr++ = ' ';
        }
        ptr += sprintf(ptr, "%d", state[i]);
    }
    *ptr++ = ']';
    *ptr = '\0';

    return result;
}

float get_value(Agent *agent, int m_links, int *state) {
    char *key = to_string(m_links, state);
    float result = get_data(agent->value, key);

    free(key);
    return result;
}

void set_value(Agent *agent, int m_links, int *state, float value) {
    char *key = to_string(m_links, state);
    insert_data(agent->value, key, value);
    free(key);
}

float get_policy(Agent *agent, int m_links, int *state) {
    char *key = to_string(m_links, state);
    float result = get_data(agent->policy, key);

    free(key);
    return result;
}

void set_policy(Agent *agent, int m_links, int *state, float value) {
    char *key = to_string(m_links, state);
    insert_data(agent->policy, key, value);
    free(key);
}
