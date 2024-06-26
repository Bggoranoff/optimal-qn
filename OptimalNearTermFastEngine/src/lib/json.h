#ifndef JSON_H
#define JSON_H

#include "hashmap.h"

void serialise_hashmap(HashMap* map, char* json);

void serialise_system(const char *policy, const char *values, const char *params, char *json);

#endif

