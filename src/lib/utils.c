#include "utils.h"
#include <assert.h>
#include <limits.h>
#include <math.h>

int get_ttl(float p_i, float alpha, float f_thresh, float gamma) {
    assert(p_i >= 0 && p_i <= 1);
    assert(f_thresh >= F_MIN);

    if (f_thresh == F_MIN) {
        return INT_MAX;
    }

    float f_i = 1 - alpha * p_i;
    if (f_i < F_MIN) {
        return 0;
    }

    return floorf(logf((f_i - F_MIN) / (f_thresh - F_MIN)) / gamma);
}

long factorial(int n) {
    long result = 1;

    for (int i = 1; i <= n; i++) {
        result *= i;
    }

    return result;
}
