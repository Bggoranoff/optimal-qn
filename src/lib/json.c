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
                strcat(json, ", ");
            }

            char buffer[BUF_SIZE];
            snprintf(buffer, sizeof(buffer), "\"%s\": %f", node->key, node->value);
            strcat(json, buffer);

            node = node->next;
            first = false;
        }
    }

    strcat(json, "}");
}

void deserialise_hashmap(const char* json, HashMap* map) {
    char key[BUF_SIZE];
    float value;

    const char* ptr = json;

    while (*ptr != '{' && *ptr != '\0') {
        ptr += 1;
    }

    while (*ptr != '\0' && *ptr != '}') {
        ptr += 1;

        while (*ptr == ' ' || *ptr == '\n' || *ptr == '\t') {
            ptr += 1;
        }
        
        if (*ptr == '\"') {
            ptr += 1;
            char* key_start = (char*) ptr;

            while (*ptr != '\"') {
                ptr += 1;
            }

            strncpy(key, key_start, ptr - key_start);
            key[ptr - key_start] = '\0';
            ptr += 1;
        }

        while (*ptr != ':' && *ptr != '\0') {
            ptr += 1;
        }

        if (*ptr == ':') {
            ptr += 1;
            sscanf(ptr, "%f", &value);
            insert_data(map, key, value);
        }

        while (*ptr != ',' && *ptr != '}' && *ptr != '\0') {
            ptr += 1;
        }
    }
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
