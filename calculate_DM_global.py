import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy.integrate import quad, quadrature, fixed_quad
import math
from importascii import CQ_assesing, exp
from globalweights import global_weights
import globals


def unif_dnes_v1(x, q, p):
    if x <= q[1]:
        val = (p[0] * (1 / (q[1] - q[0])))
    elif x > q[-2]:
        val = (p[-1] * (1 / (q[-1] - q[-2])))
    else:
        for i in range(1, len(p)):
            if (x <= q[i + 1]) & (x > q[i]):
                val = (p[i] * (1 / (q[i + 1] - q[i])))

    return val


def calculate_DM_global(W_index):
    p = []
    temp = [0.]
    for i in range(len(globals.quants)):
        temp.append(globals.quants[i])
    temp.append(1.0)
    for i in range(1, len(temp)):
        p.append(temp[i] - temp[i - 1])

    lowvals = np.zeros([len(globals.CQ_assess) + len(globals.TQ_assess)])
    higvals = np.zeros([len(globals.CQ_assess) + len(globals.TQ_assess)])
    x_o = np.zeros([len(globals.CQ_assess) + len(globals.TQ_assess)])
    x_n = np.zeros([len(globals.CQ_assess) + len(globals.TQ_assess)])
    strs = ["" for x in range(len(globals.experts))]
    fin_str = ["" for x in range(len(globals.experts))]
    i = 0
    for CQ_value in globals.CQ_values:
        lowvals[i] = CQ_value.value
        higvals[i] = CQ_value.value
        quant = []
        for CQ_asses in globals.CQ_assess:
            if CQ_value.name == CQ_asses.prod_name:
                for j in range(len(CQ_asses.vals)):
                    # quant.append(CQ_asses.vals[j])
                    if CQ_asses.vals[0] > -900:
                        if lowvals[i] > CQ_asses.vals[j]:
                            lowvals[i] = CQ_asses.vals[j]
                        if higvals[i] < CQ_asses.vals[j]:
                            higvals[i] = CQ_asses.vals[j]

        if CQ_value.dist.lower() == "uni":
            x_o[i] = lowvals[i] - globals.k * (higvals[i] - lowvals[i])
            x_n[i] = higvals[i] + globals.k * (higvals[i] - lowvals[i])
            quant.append(x_o[i])
            quant.append(x_n[i])

            W_tot = 1.0
            for expert in globals.experts:
                for CQ_asses in globals.CQ_assess:
                    if CQ_value.name == CQ_asses.prod_name and CQ_asses.exp_id == expert.id:
                        if expert.W[W_index][4] == 0 or CQ_asses.vals[0] <= -900:
                            W_tot = W_tot - expert.W[W_index][4]

            nexp = 0
            for expert in globals.experts:
                for CQ_asses in globals.CQ_assess:
                    if CQ_value.name == CQ_asses.prod_name and CQ_asses.exp_id == expert.id:
                        if expert.W[W_index][4] == 0 or CQ_asses.vals[0] <= -900:
                            strs[nexp] = ' 0'
                        else:
                            string1 = "[ " + str(x_o[i])
                            for ii in range(len(CQ_asses.vals)):
                                string1 = string1 + "," + str(CQ_asses.vals[ii])
                            string1 = string1 + "," + str(x_n[i]) + " ]"
                            strs[nexp] = ' {:}*unif_dnes_v1(x, {:}, {:})'.format(expert.W[W_index][4] / W_tot, string1,
                                                                                 str(p))
                            for j in range(len(CQ_asses.vals)):
                                quant.append(CQ_asses.vals[j])
                nexp = nexp + 1

            fin_str[0] = strs[0]

            for j in range(1, len(strs)):
                fin_str[j] = fin_str[j - 1] + " + " + strs[j]

            X = np.sort(np.unique(quant))

            CQ_value.X_DM.append(X[0])
            CQ_value.F_DM.append(0)
            integral = 0
            for j in range(1, len(X)):
                x = X[j]
                CQ_value.X_DM.append(X[j])
                CQ_value.f_DM.append(eval(fin_str[len(strs) - 1]))
                dintegral = quad(eval("lambda x: " + fin_str[len(strs) - 1]), X[j - 1], X[j])
                integral = integral + dintegral[0]
                CQ_value.F_DM.append(integral)

            DM_vals = np.interp(globals.quants, CQ_value.F_DM, CQ_value.X_DM)

            CQ_value.DM.append(x_o[i])
            CQ_value.DM.extend(DM_vals)
            CQ_value.DM.append(x_n[i])

        elif CQ_value.dist.lower() == "log_uni" or CQ_value.dist.lower() == "log":
            x_o[i] = math.log(lowvals[i]) - globals.k * (math.log(higvals[i]) - math.log(lowvals[i]))
            x_n[i] = math.log(higvals[i]) + globals.k * (math.log(higvals[i]) - math.log(lowvals[i]))
            quant.append(x_o[i])
            quant.append(x_n[i])
            W_tot = 1.0
            for expert in globals.experts:
                for CQ_asses in globals.CQ_assess:
                    if CQ_value.name == CQ_asses.prod_name and CQ_asses.exp_id == expert.id:
                        if expert.W[W_index][4] == 0 or CQ_asses.vals[0] <= -900:
                            W_tot = W_tot - expert.W[W_index][4]

            nexp = 0
            for expert in globals.experts:
                for CQ_asses in globals.CQ_assess:
                    if CQ_value.name == CQ_asses.prod_name and CQ_asses.exp_id == expert.id:
                        if expert.W[W_index][4] == 0 or CQ_asses.vals[0] <= -900:
                            strs[nexp] = ' 0'
                        else:
                            string1 = "[ " + str(x_o[i])
                            for ii in range(len(CQ_asses.vals)):
                                string1 = string1 + "," + str(math.log(CQ_asses.vals[ii]))
                            string1 = string1 + "," + str(x_n[i]) + " ]"
                            strs[nexp] = ' {:}*unif_dnes_v1(x, {:}, {:})'.format(expert.W[W_index][4] / W_tot, string1,
                                                                                 str(p))

                            for j in range(len(CQ_asses.vals)):
                                quant.append(math.log(CQ_asses.vals[j]))

                nexp = nexp + 1

            fin_str[0] = strs[0]

            for j in range(1, len(strs)):
                fin_str[j] = fin_str[j - 1] + " + " + strs[j]

            X = np.sort(np.unique(quant))

            F_DM = [0]
            CQ_value.X_DM.append(X[0])
            CQ_value.F_DM.append(0)
            integral = 0
            for j in range(1, len(X)):
                x = X[j]
                CQ_value.X_DM.append(X[j])
                CQ_value.f_DM.append(eval(fin_str[len(strs) - 1]))
                dintegral = quad(eval("lambda x: " + fin_str[len(strs) - 1]), X[j - 1], X[j])
                integral = integral + dintegral[0]
                CQ_value.F_DM.append(integral)

            DM_vals = np.interp(globals.quants, CQ_value.F_DM, CQ_value.X_DM)
            CQ_value.DM.append(math.exp(x_o[i]))
            CQ_value.DM.extend([math.exp(DM_vals[ii]) for ii in range(len(globals.quants))])
            CQ_value.DM.append(math.exp(x_n[i]))


        else:
            print('Wrong background measure of item ' + CQ_value.name)

    for TQ_value in globals.TQ_values:
        lowvals[i] = 1e6
        higvals[i] = -1e6
        quant = []
        for TQ_asses in globals.TQ_assess:
            if TQ_value.name == TQ_asses.prod_name:
                for j in range(len(TQ_asses.vals)):
                    # quant.append(TQ_asses.vals[j])
                    if TQ_asses.vals[0] > -900:
                        if lowvals[i] > TQ_asses.vals[j]:
                            lowvals[i] = TQ_asses.vals[j]
                        if higvals[i] < TQ_asses.vals[j]:
                            higvals[i] = TQ_asses.vals[j]

        if TQ_value.dist.lower() == "uni":
            x_o[i] = lowvals[i] - globals.k * (higvals[i] - lowvals[i])
            x_n[i] = higvals[i] + globals.k * (higvals[i] - lowvals[i])
            quant.append(x_o[i])
            quant.append(x_n[i])
            nexp = 0
            for expert in globals.experts:
                for TQ_asses in globals.TQ_assess:
                    if TQ_value.name == TQ_asses.prod_name and TQ_asses.exp_id == expert.id:
                        if expert.W[W_index][4] == 0 or TQ_asses.vals[0] < -900:
                            strs[nexp] = ' 0'
                        else:
                            string1 = "[ " + str(x_o[i])
                            for ii in range(len(TQ_asses.vals)):
                                string1 = string1 + "," + str(TQ_asses.vals[ii])
                            string1 = string1 + "," + str(x_n[i]) + " ]"
                            strs[nexp] = ' {:}*unif_dnes_v1(x, {:}, {:})'.format(expert.W[W_index][4], string1, str(p))
                            for j in range(len(TQ_asses.vals)):
                                quant.append(TQ_asses.vals[j])
                nexp = nexp + 1

            fin_str[0] = strs[0]

            for j in range(1, len(strs)):
                fin_str[j] = fin_str[j - 1] + " + " + strs[j]

            X = np.sort(np.unique(quant))

            F_DM = [0]
            TQ_value.X_DM.append(X[0])
            TQ_value.F_DM.append(0)
            integral = 0
            for j in range(1, len(X)):
                x = X[j]
                TQ_value.X_DM.append(X[j])
                TQ_value.f_DM.append(eval(fin_str[len(strs) - 1]))
                dintegral = quad(eval("lambda x: " + fin_str[len(strs) - 1]), X[j - 1], X[j])
                integral = integral + dintegral[0]
                TQ_value.F_DM.append(integral)

            vals = globals.quants  # get p here?
            DM_vals = np.interp(vals, TQ_value.F_DM, TQ_value.X_DM)

            TQ_value.DM.append(x_o[i])
            TQ_value.DM.extend(DM_vals)
            TQ_value.DM.append(x_n[i])

        elif TQ_value.dist.lower() == "log_uni" or TQ_value.dist.lower() == "log":
            x_o[i] = math.log(lowvals[i]) - globals.k * (math.log(higvals[i]) - math.log(lowvals[i]))
            x_n[i] = math.log(higvals[i]) + globals.k * (math.log(higvals[i]) - math.log(lowvals[i]))

            nexp = 0
            for expert in globals.experts:
                for TQ_asses in globals.TQ_assess:
                    if TQ_value.name == TQ_asses.prod_name and TQ_asses.exp_id == expert.id:
                        if expert.W[W_index][4] == 0 or TQ_asses.vals[0] <= -900:
                            strs[nexp] = ' 0'
                        else:
                            string1 = "[ " + str(x_o[i])
                            for ii in range(len(TQ_asses.vals)):
                                string1 = string1 + "," + str(math.log(TQ_asses.vals[ii]))
                            string1 = string1 + "," + str(x_n[i]) + " ]"
                            strs[nexp] = ' {:}*unif_dnes_v1(x, {:}, {:})'.format(expert.W[W_index][4], string1,
                                                                                 str(p))
                            for j in range(len(TQ_asses.vals)):
                                quant.append(math.log(TQ_asses.vals[j]))
                nexp = nexp + 1

            fin_str[0] = strs[0]

            for j in range(1, len(strs)):
                fin_str[j] = fin_str[j - 1] + " + " + strs[j]

            X = np.sort(np.unique(quant))
            integral = 0
            for j in range(1, len(X)):
                x = X[j]
                TQ_value.X_DM.append(X[i])
                TQ_value.f_DM.append(eval(fin_str[len(strs) - 1]))
                dintegral = quad(eval("lambda x: " + fin_str[len(strs) - 1]), X[j - 1], X[j])
                integral = integral + dintegral[0]
                TQ_value.F_DM.append(integral)

            vals = globals.quants  # get p here?
            DM_vals = np.interp(vals, TQ_value.F_DM, TQ_value.X_DM)
            TQ_value.DM.append(math.exp(x_o[i]))
            TQ_value.DM.extend([math.exp(DM_vals[ii]) for ii in range(len(globals.quants))])
            TQ_value.DM.append(math.exp(x_n[i]))
        else:
            print('Wrong background measure of item ' + TQ_value.name)

    # now add to CQ_assesing and to globals.TQ_assess
    id_DM = len(globals.experts) + 1
    globals.experts.append(
        exp(id_DM, "DM", np.zeros(len(globals.TQ_index)), np.zeros(len(globals.CQ_values)), len(globals.quants)))

    for TQ_value in globals.TQ_values:
        globals.TQ_assess.append(CQ_assesing(id_DM, "DM", TQ_value.id, TQ_value.name, TQ_value.dist,
                                             [TQ_value.DM[ii + 1] for ii in range(len(globals.quants))]))

    for CQ_value in globals.CQ_values:
        if CQ_value.value > -900 and str(CQ_value.value) != "":
            globals.CQ_assess.append(CQ_assesing(id_DM, "DM", CQ_value.id, CQ_value.name, CQ_value.dist,
                                                 [CQ_value.DM[ii + 1] for ii in range(len(globals.quants))]))

    global_weights(W_index + 1)

    return
