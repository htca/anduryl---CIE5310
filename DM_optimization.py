import numpy as np

import globals
import revert
from calculate_DM_global import calculate_DM_global
from calculate_DM_item import calculate_DM_item
from globalweights import global_weights


def DM_optimization():
    if globals.weight_type == "global":

        global_weights(0)
        calculate_DM_global(0)

        initial_alpha = 0
        alphas = [initial_alpha]
        for expert in globals.experts:
            alphas.append(expert.W[0][0])

        alphas = np.sort(np.unique(alphas))
        alpha_select = initial_alpha

        W_max = globals.experts[-1].W[1][3]

        for alpha in alphas:
            revert.revert()
            globals.alpha = alpha
            global_weights(0)
            calculate_DM_global(0)
            if W_max <= globals.experts[-1].W[1][3]:
                W_max = globals.experts[-1].W[1][3]
                alpha_select = alpha

        globals.alpha = alpha_select
        revert.revert()

        global_weights(0)
        calculate_DM_global(0)

    elif globals.weight_type == "item":

        initial_alpha = 0
        global_weights(0)
        calculate_DM_item(0)

        alphas = [initial_alpha]
        for expert in globals.experts:
            alphas.append(expert.W[0][0])

        W_max = globals.experts[-1].W[1][3]
        globals.alpha = initial_alpha
        alpha_select = initial_alpha
        for alpha in alphas:
            revert.revert()
            globals.alpha = alpha
            global_weights(0)
            calculate_DM_item(0)

            if W_max <= globals.experts[-1].W[1][3]:
                W_max = globals.experts[-1].W[1][3]
                alpha_select = alpha

        revert.revert()
        globals.alpha = alpha_select

        global_weights(0)
        calculate_DM_item(0)

    else:
        print("wrong weight_type! only global or item are allowed")

    return
