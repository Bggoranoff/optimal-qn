#ifndef SOLVE_BASIC
#define SOLVE_BASIC

typedef struct TwoProtocolSystem {
    float f_thresh;
    float p_1;
    float p_2;
    float alpha;
    float gamma;
} TwoProtocolSystem;

int solve_basic(TwoProtocolSystem sys);

#endif

