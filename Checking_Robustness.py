from itertools import combinations

import numpy as np

import globals
import revert
from DM_optimization import DM_optimization
from calculate_DM_global import calculate_DM_global
from calculate_DM_item import calculate_DM_item
from globalweights import global_weights


#     Robustness_table = Checglobals.king_Robustness_items(Cal_var, TQ_assess, realization,...
#         globals.k ,globals.alpha, bacglobals.k_measure, N_max_it, weight_type, optimization, incl_cal_pwr);
#
# global_weights(CQ_values, CQ_assess, TQ_assess, experts, globals.TQ_index, globals.k, globals.alpha, 0)
#         calculate_DM_global(CQ_values, CQ_assess, TQ_assess, experts, globals.alpha, globals.k, globals.TQ_index, TQ_values, 0)
# Cal_var(i,j,globals.k)
# i = aantal expert
# j = aantal quantielen
# globals.k = aantal calibratie vragen

def Checking_Robustness_items(incl_cal_pwr, cal_power):
    prodlist = []
    robustness_table = []
    cal_power_l = cal_power
    for CQ_value in globals.CQ_values:
        prodlist.append(CQ_value.id)
    for i in range(0, globals.N_max_it):
        Remove_CQ_values = []
        m = list(combinations(prodlist, i + 1))

        for kn in range(len(m)):
            Remove_CQ_values.append([m[kn][l] for l in range(len(m[kn]))])

        if incl_cal_pwr == "yes":
            cal_power_l = (len(globals.CQ_values) - float(i)) / len(globals.CQ_values)

        for remove_CQ_value in Remove_CQ_values:
            string1 = ('Excluded questions: ' + str(remove_CQ_value)[1:-1])
            revert.revert()
            rem_lin = []
            i = 0

            for CQ_value in globals.CQ_values:
                if CQ_value.id in remove_CQ_value:
                    rem_lin.append(i)
                i = i + 1

            for j in reversed(rem_lin):
                globals.CQ_values.remove(globals.CQ_values[j])

            rem_lin = []
            i = 0
            for CQ_asses in globals.CQ_assess:
                if CQ_asses.prod_id in remove_CQ_value:
                    rem_lin.append(i)
                i = i + 1

            for j in reversed(rem_lin):
                globals.CQ_assess.remove(globals.CQ_assess[j])

            if not globals.optimization:
                if globals.weight_type == 'global':
                    global_weights(0)

                    exp_ar = []
                    for expert in globals.experts:
                        exp_ar.append(expert.W[0][3])

                    if np.array_equal(exp_ar, np.zeros(len(globals.experts))):
                        string2 = 'Not possible to calculate the DM. All weights are zero'
                        robustness_table.append([string1, string2, "", ""])
                    else:
                        calculate_DM_global(0)

                elif globals.weight_type == 'item':
                    global_weights(0)

                    exp_ar = []
                    for expert in globals.experts:
                        exp_ar.append([expert.w_CQ_asses[i] for i in range(len(globals.CQ_values))])

                    if np.array_equal(exp_ar, np.zeros((len(globals.experts), len(globals.CQ_values)))):
                        string2 = 'Not possible to calculate the DM. All weights are zero'
                        robustness_table.append([string1, string2, "", ""])
                    else:
                        calculate_DM_item(0)
                else:
                    print("Robustness only for item and global")
            else:
                DM_optimization()

            robustness_table.append(
                [string1, globals.experts[-1].W[1][2], globals.experts[-1].W[1][1], globals.experts[-1].W[1][0]])

    return robustness_table
