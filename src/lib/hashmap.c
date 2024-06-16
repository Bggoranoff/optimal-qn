#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include "hashmap.h"

unsigned int hash(const char* key) {
    int sum = 0;

    while(*key != '\0') {
        sum += (int) *key;
        key += 1;
    }

    return sum;
}

HashMap* create_hashmap(size_t key_space) {
    HashMap* result = calloc(1, sizeof(HashMap));

    result->size = key_space;
    result->data = calloc(key_space, sizeof(Node*));

    return result;
}

void insert_data(HashMap* hm, const char* key, float data) {
    if(hm == NULL || key == NULL || hm->size == 0) {
        return;
    }

    unsigned int hashed_key = hash(key) % hm->size;

    Node* node = calloc(1,sizeof(Node));
    node->key = calloc(strlen(key) + 1, sizeof(char));
    strcpy(node->key, key);

    node->value = (uint64_t) data;
    node->next = NULL;

    if(hm->data[hashed_key] == NULL) {
        hm->data[hashed_key] = node;
        return;
    }

    Node* current = hm->data[hashed_key];
    Node* prev = NULL;

    while(current != NULL) {
        if(strcmp(current->key, key) == 0) {
            current->value = (uint64_t) data;
            free(node->key);
            free(node);
            return;
        }

        prev = current;
        current = current->next;
    }

    prev->next = node;
}

float get_data(HashMap* hm, const char* key) {
    if(hm == NULL || key == NULL || hm->size == 0) {
        return 0.0f;
    }

    unsigned int hashed_key = hash(key) % hm->size;

    Node* current = hm->data[hashed_key];
    while(current != NULL) {
        if(strcmp(current->key, key) == 0) {
            return current->value;
        }

        current = current->next;
    }

    return 0.0f;
}

void remove_data(HashMap* hm, const char* key) {
    if(hm == NULL || key == NULL || hm->size == 0) {
        return;
    }

    unsigned int hashed_key = hash(key) % hm->size;

    Node* current = hm->data[hashed_key];
    Node* prev = NULL;

    while(current != NULL) {
        if(strcmp(current->key, key) == 0) {
            if(prev == NULL) {
                hm->data[hashed_key] = current->next;
                free(current);
            } else {
                prev->next = current->next;
                free(current);
            }

            return;
        }

        prev = current;
        current = current->next;
    }
}

void delete_hashmap(HashMap* hm) {
    if(hm == NULL) {
        return;
    }

    for(uint64_t i = 0; i < hm->size; i++) {
        if(hm->data[i] == NULL) {
            continue;
        }

        Node* current = hm->data[i];
        while(current != NULL) {
            Node* tmp = current;
            current = current->next;

            free(tmp);
        }
        hm->data[i] = NULL;
    }

    free(hm->data);
    hm->data = NULL;
    free(hm);
}

