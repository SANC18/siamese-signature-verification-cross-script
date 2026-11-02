# Summary of results (mean +/- std over seeds)

Values are fractions (0.05 = 5%). FAR/FRR use the threshold fixed on the training dataset's validation data.


## baseline | contrastive | clean test images

| Train on | Test on | EER | FAR | FRR | AUC | Acc (fixed thr.) | Acc (best thr.) | Seeds |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bengali | bengali | 0.106 +/- 0.006 | 0.079 +/- 0.009 | 0.172 +/- 0.028 | 0.961 +/- 0.002 | 0.874 +/- 0.010 | 0.904 +/- 0.004 | 3 |
| bengali | cedar | 0.196 +/- 0.022 | 0.492 +/- 0.269 | 0.111 +/- 0.157 | 0.893 +/- 0.018 | 0.698 +/- 0.062 | 0.816 +/- 0.021 | 3 |
| bengali | hindi | 0.223 +/- 0.007 | 0.144 +/- 0.030 | 0.318 +/- 0.038 | 0.853 +/- 0.004 | 0.769 +/- 0.004 | 0.780 +/- 0.005 | 3 |
| cedar | bengali | 0.191 +/- 0.001 | 0.977 +/- 0.012 | 0.000 +/- 0.000 | 0.890 +/- 0.001 | 0.511 +/- 0.006 | 0.813 +/- 0.002 | 3 |
| cedar | cedar | 0.053 +/- 0.007 | 0.065 +/- 0.011 | 0.039 +/- 0.019 | 0.988 +/- 0.002 | 0.948 +/- 0.007 | 0.952 +/- 0.005 | 3 |
| cedar | hindi | 0.213 +/- 0.004 | 0.986 +/- 0.010 | 0.000 +/- 0.000 | 0.868 +/- 0.005 | 0.507 +/- 0.005 | 0.791 +/- 0.006 | 3 |
| hindi | bengali | 0.174 +/- 0.009 | 0.129 +/- 0.026 | 0.228 +/- 0.013 | 0.904 +/- 0.008 | 0.821 +/- 0.008 | 0.828 +/- 0.011 | 3 |
| hindi | cedar | 0.160 +/- 0.007 | 0.549 +/- 0.068 | 0.002 +/- 0.001 | 0.923 +/- 0.005 | 0.724 +/- 0.033 | 0.844 +/- 0.006 | 3 |
| hindi | hindi | 0.074 +/- 0.008 | 0.087 +/- 0.015 | 0.065 +/- 0.016 | 0.976 +/- 0.004 | 0.924 +/- 0.007 | 0.928 +/- 0.008 | 3 |

## baseline | triplet | clean test images

| Train on | Test on | EER | FAR | FRR | AUC | Acc (fixed thr.) | Acc (best thr.) | Seeds |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bengali | bengali | 0.112 +/- 0.012 | 0.099 +/- 0.020 | 0.132 +/- 0.011 | 0.953 +/- 0.007 | 0.885 +/- 0.007 | 0.894 +/- 0.012 | 3 |
| bengali | cedar | 0.277 +/- 0.038 | 0.535 +/- 0.123 | 0.048 +/- 0.067 | 0.822 +/- 0.033 | 0.709 +/- 0.037 | 0.760 +/- 0.022 | 3 |
| bengali | hindi | 0.209 +/- 0.004 | 0.301 +/- 0.025 | 0.151 +/- 0.024 | 0.872 +/- 0.005 | 0.774 +/- 0.003 | 0.797 +/- 0.002 | 3 |
| cedar | bengali | 0.180 +/- 0.012 | 0.947 +/- 0.069 | 0.000 +/- 0.000 | 0.904 +/- 0.009 | 0.526 +/- 0.034 | 0.823 +/- 0.012 | 3 |
| cedar | cedar | 0.096 +/- 0.002 | 0.073 +/- 0.009 | 0.132 +/- 0.011 | 0.968 +/- 0.001 | 0.897 +/- 0.002 | 0.909 +/- 0.002 | 3 |
| cedar | hindi | 0.209 +/- 0.010 | 0.964 +/- 0.048 | 0.001 +/- 0.002 | 0.867 +/- 0.010 | 0.518 +/- 0.023 | 0.794 +/- 0.011 | 3 |
| hindi | bengali | 0.143 +/- 0.001 | 0.147 +/- 0.021 | 0.139 +/- 0.019 | 0.931 +/- 0.002 | 0.857 +/- 0.001 | 0.859 +/- 0.002 | 3 |
| hindi | cedar | 0.201 +/- 0.045 | 0.533 +/- 0.103 | 0.022 +/- 0.021 | 0.892 +/- 0.037 | 0.723 +/- 0.044 | 0.808 +/- 0.046 | 3 |
| hindi | hindi | 0.146 +/- 0.007 | 0.168 +/- 0.005 | 0.118 +/- 0.011 | 0.931 +/- 0.004 | 0.857 +/- 0.008 | 0.859 +/- 0.008 | 3 |

## degrade_aug | contrastive | clean test images

| Train on | Test on | EER | FAR | FRR | AUC | Acc (fixed thr.) | Acc (best thr.) | Seeds |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bengali | bengali | 0.144 +/- 0.000 | 0.086 +/- 0.000 | 0.231 +/- 0.000 | 0.939 +/- 0.000 | 0.842 +/- 0.000 | 0.861 +/- 0.000 | 1 |
| bengali | cedar | 0.215 +/- 0.000 | 0.315 +/- 0.000 | 0.128 +/- 0.000 | 0.866 +/- 0.000 | 0.779 +/- 0.000 | 0.787 +/- 0.000 | 1 |
| bengali | hindi | 0.193 +/- 0.000 | 0.176 +/- 0.000 | 0.213 +/- 0.000 | 0.884 +/- 0.000 | 0.805 +/- 0.000 | 0.808 +/- 0.000 | 1 |
| cedar | bengali | 0.224 +/- 0.000 | 0.252 +/- 0.000 | 0.200 +/- 0.000 | 0.852 +/- 0.000 | 0.774 +/- 0.000 | 0.778 +/- 0.000 | 1 |
| cedar | cedar | 0.051 +/- 0.000 | 0.051 +/- 0.000 | 0.056 +/- 0.000 | 0.987 +/- 0.000 | 0.947 +/- 0.000 | 0.954 +/- 0.000 | 1 |
| cedar | hindi | 0.245 +/- 0.000 | 0.425 +/- 0.000 | 0.126 +/- 0.000 | 0.819 +/- 0.000 | 0.725 +/- 0.000 | 0.761 +/- 0.000 | 1 |
| hindi | bengali | 0.172 +/- 0.000 | 0.179 +/- 0.000 | 0.166 +/- 0.000 | 0.905 +/- 0.000 | 0.828 +/- 0.000 | 0.831 +/- 0.000 | 1 |
| hindi | cedar | 0.243 +/- 0.000 | 0.603 +/- 0.000 | 0.022 +/- 0.000 | 0.840 +/- 0.000 | 0.688 +/- 0.000 | 0.762 +/- 0.000 | 1 |
| hindi | hindi | 0.132 +/- 0.000 | 0.162 +/- 0.000 | 0.101 +/- 0.000 | 0.940 +/- 0.000 | 0.869 +/- 0.000 | 0.872 +/- 0.000 | 1 |

## degrade_aug | triplet | clean test images

| Train on | Test on | EER | FAR | FRR | AUC | Acc (fixed thr.) | Acc (best thr.) | Seeds |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bengali | bengali | 0.119 +/- 0.000 | 0.081 +/- 0.000 | 0.182 +/- 0.000 | 0.939 +/- 0.000 | 0.869 +/- 0.000 | 0.884 +/- 0.000 | 1 |
| bengali | cedar | 0.292 +/- 0.000 | 0.675 +/- 0.000 | 0.059 +/- 0.000 | 0.771 +/- 0.000 | 0.633 +/- 0.000 | 0.710 +/- 0.000 | 1 |
| bengali | hindi | 0.243 +/- 0.000 | 0.166 +/- 0.000 | 0.335 +/- 0.000 | 0.830 +/- 0.000 | 0.750 +/- 0.000 | 0.763 +/- 0.000 | 1 |
| cedar | bengali | 0.211 +/- 0.000 | 0.848 +/- 0.000 | 0.007 +/- 0.000 | 0.870 +/- 0.000 | 0.572 +/- 0.000 | 0.793 +/- 0.000 | 1 |
| cedar | cedar | 0.167 +/- 0.000 | 0.099 +/- 0.000 | 0.300 +/- 0.000 | 0.918 +/- 0.000 | 0.800 +/- 0.000 | 0.840 +/- 0.000 | 1 |
| cedar | hindi | 0.229 +/- 0.000 | 0.943 +/- 0.000 | 0.000 +/- 0.000 | 0.860 +/- 0.000 | 0.528 +/- 0.000 | 0.773 +/- 0.000 | 1 |
| hindi | bengali | 0.196 +/- 0.000 | 0.240 +/- 0.000 | 0.143 +/- 0.000 | 0.893 +/- 0.000 | 0.808 +/- 0.000 | 0.810 +/- 0.000 | 1 |
| hindi | cedar | 0.212 +/- 0.000 | 0.056 +/- 0.000 | 0.511 +/- 0.000 | 0.876 +/- 0.000 | 0.716 +/- 0.000 | 0.792 +/- 0.000 | 1 |
| hindi | hindi | 0.180 +/- 0.000 | 0.181 +/- 0.000 | 0.179 +/- 0.000 | 0.898 +/- 0.000 | 0.820 +/- 0.000 | 0.824 +/- 0.000 | 1 |

## baseline | degraded test images (own test writers)

| Train on | Loss | Condition | EER | FAR | FRR |
| --- | --- | --- | --- | --- | --- |
| bengali | contrastive | blur | 0.431 | 0.002 | 0.998 |
| bengali | contrastive | clean | 0.106 | 0.079 | 0.172 |
| bengali | contrastive | lines | 0.408 | 0.003 | 0.990 |
| bengali | contrastive | mix | 0.471 | 0.035 | 0.964 |
| bengali | contrastive | noise | 0.501 | 0.071 | 0.935 |
| bengali | contrastive | stamp | 0.369 | 0.024 | 0.943 |
| bengali | triplet | blur | 0.441 | 0.001 | 1.000 |
| bengali | triplet | clean | 0.112 | 0.099 | 0.132 |
| bengali | triplet | lines | 0.443 | 0.001 | 0.998 |
| bengali | triplet | mix | 0.490 | 0.001 | 0.999 |
| bengali | triplet | noise | 0.493 | 0.000 | 1.000 |
| bengali | triplet | stamp | 0.363 | 0.019 | 0.947 |
| cedar | contrastive | blur | 0.300 | 0.009 | 0.983 |
| cedar | contrastive | clean | 0.053 | 0.065 | 0.039 |
| cedar | contrastive | lines | 0.357 | 0.007 | 0.984 |
| cedar | contrastive | mix | 0.419 | 0.006 | 0.978 |
| cedar | contrastive | noise | 0.478 | 0.000 | 1.000 |
| cedar | contrastive | stamp | 0.302 | 0.006 | 0.935 |
| cedar | triplet | blur | 0.324 | 0.001 | 1.000 |
| cedar | triplet | clean | 0.096 | 0.073 | 0.132 |
| cedar | triplet | lines | 0.314 | 0.007 | 0.988 |
| cedar | triplet | mix | 0.370 | 0.002 | 0.994 |
| cedar | triplet | noise | 0.432 | 0.000 | 1.000 |
| cedar | triplet | stamp | 0.303 | 0.012 | 0.974 |
| hindi | contrastive | blur | 0.465 | 0.168 | 0.786 |
| hindi | contrastive | clean | 0.074 | 0.087 | 0.065 |
| hindi | contrastive | lines | 0.410 | 0.012 | 0.975 |
| hindi | contrastive | mix | 0.474 | 0.020 | 0.965 |
| hindi | contrastive | noise | 0.490 | 0.003 | 0.993 |
| hindi | contrastive | stamp | 0.343 | 0.010 | 0.956 |
| hindi | triplet | blur | 0.453 | 0.047 | 0.941 |
| hindi | triplet | clean | 0.146 | 0.168 | 0.118 |
| hindi | triplet | lines | 0.477 | 0.001 | 0.997 |
| hindi | triplet | mix | 0.493 | 0.003 | 0.997 |
| hindi | triplet | noise | 0.487 | 0.000 | 1.000 |
| hindi | triplet | stamp | 0.422 | 0.006 | 0.981 |

## degrade_aug | degraded test images (own test writers)

| Train on | Loss | Condition | EER | FAR | FRR |
| --- | --- | --- | --- | --- | --- |
| bengali | contrastive | blur | 0.208 | 0.117 | 0.406 |
| bengali | contrastive | clean | 0.144 | 0.086 | 0.231 |
| bengali | contrastive | lines | 0.158 | 0.089 | 0.282 |
| bengali | contrastive | mix | 0.245 | 0.085 | 0.590 |
| bengali | contrastive | noise | 0.194 | 0.053 | 0.460 |
| bengali | contrastive | stamp | 0.177 | 0.099 | 0.335 |
| bengali | triplet | blur | 0.205 | 0.089 | 0.610 |
| bengali | triplet | clean | 0.119 | 0.081 | 0.182 |
| bengali | triplet | lines | 0.148 | 0.078 | 0.267 |
| bengali | triplet | mix | 0.246 | 0.100 | 0.573 |
| bengali | triplet | noise | 0.124 | 0.073 | 0.244 |
| bengali | triplet | stamp | 0.165 | 0.082 | 0.357 |
| cedar | contrastive | blur | 0.057 | 0.045 | 0.097 |
| cedar | contrastive | clean | 0.051 | 0.051 | 0.056 |
| cedar | contrastive | lines | 0.057 | 0.045 | 0.102 |
| cedar | contrastive | mix | 0.106 | 0.035 | 0.344 |
| cedar | contrastive | noise | 0.066 | 0.042 | 0.126 |
| cedar | contrastive | stamp | 0.052 | 0.041 | 0.089 |
| cedar | triplet | blur | 0.269 | 0.090 | 0.626 |
| cedar | triplet | clean | 0.167 | 0.099 | 0.300 |
| cedar | triplet | lines | 0.233 | 0.032 | 0.833 |
| cedar | triplet | mix | 0.353 | 0.018 | 0.927 |
| cedar | triplet | noise | 0.587 | 0.000 | 1.000 |
| cedar | triplet | stamp | 0.228 | 0.013 | 0.885 |
| hindi | contrastive | blur | 0.338 | 0.304 | 0.386 |
| hindi | contrastive | clean | 0.132 | 0.162 | 0.101 |
| hindi | contrastive | lines | 0.170 | 0.180 | 0.163 |
| hindi | contrastive | mix | 0.310 | 0.270 | 0.361 |
| hindi | contrastive | noise | 0.172 | 0.183 | 0.159 |
| hindi | contrastive | stamp | 0.201 | 0.221 | 0.174 |
| hindi | triplet | blur | 0.289 | 0.174 | 0.498 |
| hindi | triplet | clean | 0.180 | 0.181 | 0.179 |
| hindi | triplet | lines | 0.211 | 0.154 | 0.288 |
| hindi | triplet | mix | 0.299 | 0.098 | 0.617 |
| hindi | triplet | noise | 0.194 | 0.065 | 0.474 |
| hindi | triplet | stamp | 0.222 | 0.177 | 0.280 |
