#include "json.h"
#include "hashmap.h"
#include <stdbool.h>
#include <stdio.h>
#include <string.h>

const size_t BUF_SIZE = 256;

void serialise_hashmap(HashMap* map, char* json) {
    strcpy(json, "{");
    bool first = true;

    for (int i = 0; i < map->size; i++) {
        Node* node = map->data[i]; 
        
        while (node != NULL) {
            if (!first) {
                strcat(json, ",\n");
            }

            char buffer[BUF_SIZE];
            snprintf(buffer, sizeof(buffer), "\t\"%s\": %f", node->key, node->value);
            strcat(json, buffer);

            node = node->next;
            first = false;
        }
    }

    strcat(json, " }");
}

void serialise_system(const char *policy, const char *values, const char *params, char *json) {
    strcpy(json, "{\n");

    strcat(json, "    \"params\": ");
    strcat(json, params);
    strcat(json, ",\n");

    strcat(json, "    \"values\": ");
    strcat(json, values);
    strcat(json, ",\n");

    strcat(json, "    \"policy\": ");
    strcat(json, policy);

    strcat(json, "\n}");
}
