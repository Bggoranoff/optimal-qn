#include <stdio.h>
#include "cli.h"

int cli_main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Usage: %s <command> [options]\n", argv[0]);
        return 1;
    }

    printf("Executing: %s\n", argv[1]);

    return 0;
}
