import random

import numpy as np

import globals
import revert
from DM_optimization import DM_optimization
from calculate_DM_global import calculate_DM_global
from calculate_DM_item import calculate_DM_item
from globalweights import global_weights


def randomise():
    revert.revert()
    exparray = np.array([expert.id for expert in globals.experts])
    expnames = np.array([expert.name for expert in globals.experts])
    globals.alpha = 0.05
    distribution = []
    N_iter = 100
    zero = 0
    for i in range(N_iter):
        revert.revert()
        exp_shuffle2 = []
        for j in range(len(globals.CQ_values)):
            exp_shuffle1 = random.sample(exparray, len(exparray))
            exp_shuffle2.append(exp_shuffle1)

        iprod = 0
        for CQ_value in globals.CQ_values:
            iCQ_asses = 0
            for CQ_asses in globals.CQ_assess:
                if CQ_value.name == CQ_asses.prod_name:
                    CQ_asses.exp_id = exp_shuffle2[iprod][iCQ_asses]
                    iCQ_asses = iCQ_asses + 1
            iprod = iprod + 1

        if not globals.optimization:
            if globals.weight_type == 'global':
                global_weights(0)
                exp_ar = []
                for expert in globals.experts:
                    exp_ar.append(expert.W[0][3])
                if np.array_equal(exp_ar, np.zeros(len(globals.experts))):
                    print('Not possible to calculate the DM. All weights are zero')
                    zero = zero + 1
                else:
                    calculate_DM_global(0)
                    distribution.append(globals.experts[-1].W[1])
            elif globals.weight_type == 'item':
                global_weights(0)
                calculate_DM_item(0)
                distribution.append(globals.experts[-1].W[1])
        else:
            DM_optimization()
            distribution.append(globals.experts[-1].W[1])

    return distribution
