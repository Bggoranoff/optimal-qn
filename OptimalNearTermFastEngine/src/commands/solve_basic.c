#include <assert.h>
#include <float.h>
#include <math.h>
#include <stdio.h>
#include "solve_basic.h"
#include "../lib/utils.h"

float calc_et(float p_1, float p_2, float t_1) {
    assert(p_1 >= 0 && p_1 <= 1);
    assert(p_2 >= 0 && p_2 <= 1);

    if (p_1 == 0 || p_2 == 0 || t_1 <= 1) {
        return FLT_MAX;
    }

    float p_fail = 1.0f - powf(1.0f - p_2, t_1 - 1.0f);
    return 1.0f / p_2 + 1.0f / (p_1 * p_fail);
}

int solve_basic(const TwoProtocolSystem *sys) {
    printf("Calling solve_basic...\n");

    assert(sys->p_1 < sys->p_2);
    assert(1 - sys->alpha * sys->p_1 >= sys->f_thresh);
    assert(1 - sys->alpha * sys->p_2 >= sys->f_thresh);

    int t_1 = get_ttl(sys->p_1, sys->alpha, sys->f_thresh, sys->gamma);
    int t_2 = get_ttl(sys->p_2, sys->alpha, sys->f_thresh, sys->gamma);

    float et_12 = calc_et(sys->p_1, sys->p_2, t_1);
    float et_22 = calc_et(sys->p_2, sys->p_2, t_2);

    printf("Protocol: (%d, %d)\n", et_12 < et_22 ? 1 : 2, 2);
    return 0;
}
