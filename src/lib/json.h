#ifndef JSON_H
#define JSON_H

#include "hashmap.h"

void serialise_hashmap(HashMap* map, char* json);

void deserialise_hashmap(const char* json, HashMap* map);

#endif
