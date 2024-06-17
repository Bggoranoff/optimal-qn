#ifndef CLI_H
#define CLI_H

#include <string.h>

int cli_main(int argc, char *argv[]);

int count_numbers(const char *input);

void parse_numbers(char *input, float *numbers, int num_count);
#endif
