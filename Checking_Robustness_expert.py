from itertools import combinations
import numpy as np
import copy
from globalweights import global_weights
from calculate_DM_global import calculate_DM_global
from calculate_DM_item import calculate_DM_item
from DM_optimization import DM_optimization


#     Robustness_table = Checking_Robustness_items(Cal_var, TQ_assess, realization,...
#         k ,alpha, back_measure, N_max_it, weight_type, optimization, incl_cal_pwr);
#
# global_weights(CQ_values, CQ_assess, TQ_assess, experts, TQ_index, k, alpha, 0)
#         calculate_DM_global(CQ_values, CQ_assess, TQ_assess, experts, alpha, k, TQ_index, TQ_values, 0)
# Cal_var(i,j,k)
# i = aantal expert
# j = aantal quantielen
# k = aantal calibratie vragen

def Checking_Robustness_expert(CQ_values, CQ_assess, TQ_assess, experts, TQ_index, TQ_values, k, alpha, w_index,
                               N_max,
                               weight_type, optimization, incl_cal_pwr, cal_power):
    explist = []
    robustness_table = []
    cal_power_l = cal_power
    for expert in experts:
        explist.append(expert.id)

    robust_row = 0
    for i in range(0, N_max):
        Remove_experts = []
        m = list(combinations(explist, i + 1))
        for k in range(len(m)):
            Remove_experts.append([m[k][l] for l in range(len(m[k]))])

        if incl_cal_pwr == "yes":
            cal_power_l = (len(CQ_values) - float(i)) / len(CQ_values)

        for remove_expert in Remove_experts:
            string1 = ('Excluded questions: ' + str(remove_expert)[1:-1])
            CQ_values_temp = copy.deepcopy(CQ_values)
            CQ_assess_temp = copy.deepcopy(CQ_assess)
            TQ_assess_temp = copy.deepcopy(TQ_assess)
            TQ_values_temp = copy.deepcopy(TQ_values)
            experts_temp = copy.deepcopy(experts)
            TQ_index_temp = copy.deepcopy(TQ_index)
            rem_lin = []
            i = 0

            for expert in experts_temp:
                if expert.id in remove_expert:
                    rem_lin.append(i)
                i = i + 1

            for j in reversed(rem_lin):
                experts_temp.remove(experts_temp[j])

            rem_lin = []
            i = 0
            for CQ_asses in CQ_assess_temp:
                if CQ_asses.exp_id in remove_expert:
                    rem_lin.append(i)
                i = i + 1

            for j in reversed(rem_lin):
                CQ_assess_temp.remove(CQ_assess_temp[j])

            rem_lin = []
            i = 0
            for TQ_asses in TQ_assess_temp:
                if TQ_asses.exp_id in remove_expert:
                    rem_lin.append(i)
                i = i + 1

            for j in reversed(rem_lin):
                TQ_assess_temp.remove(TQ_assess_temp[j])

            if not optimization:
                if weight_type == 'global':
                    global_weights(CQ_values_temp)

                    exp_ar = []
                    # print(len(experts_temp))
                    for expert in experts_temp:
                        exp_ar.append(expert.W[0][3])

                    if np.array_equal(exp_ar, np.zeros(len(experts_temp))):
                        string2 = 'Not possible to calculate the DM. All weights are zero'
                        robustness_table.append([string1, string2, "", ""])
                    else:
                        calculate_DM_global(CQ_values_temp)


                elif weight_type == 'item':
                    global_weights(CQ_values_temp)

                    exp_ar = []
                    # print(len(experts_temp))
                    for expert in experts_temp:
                        exp_ar.append([expert.w_CQ_asses[i] for i in range(len(CQ_values_temp))])

                    if np.array_equal(exp_ar, np.zeros((len(experts_temp), len(CQ_values_temp)))):
                        string2 = 'Not possible to calculate the DM. All weights are zero'
                        robustness_table.append([string1, string2, "", ""])
                    else:
                        calculate_DM_item(CQ_values_temp)
                else:
                    print("Robustness only for item and global")
            else:
                DM_optimization()

            robustness_table.append(
                [string1, experts_temp[-1].W[1][1], experts_temp[-1].W[1][2], experts_temp[-1].W[1][0]])

    return robustness_table
