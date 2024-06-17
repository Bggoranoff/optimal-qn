#ifndef POLICY_ITER
#define POLICY_ITER

typedef struct AdaptiveProtocolSystem {
    int n_links;
    float f_thresh;
    int n_actions;
    float* actions;
    float alpha;
    float gamma;
    float tol;
} AdaptiveProtocolSystem;

int policy_iter(AdaptiveProtocolSystem sys);

#endif

