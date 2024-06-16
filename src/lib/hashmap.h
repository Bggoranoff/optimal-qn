#ifndef HASHMAP_H
#define HASHMAP_H

#include <stdlib.h>

typedef struct Node {
    struct Node* next;
    char* key;
    float value;
} Node;

typedef struct HashMap {
    size_t size;
    Node** data;
} HashMap;

HashMap* create_hashmap(size_t key_space);

unsigned int hash(const char* key);

void insert_data(HashMap* hm, const char* key, float data);

float get_data(HashMap* hm, const char* key);

void remove_data(HashMap* hm, const char* key);

void delete_hashmap(HashMap* hm);

#endif
