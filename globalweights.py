import numpy as np
import math
import scipy.stats as stats
import globals


def calscore(M, cal_power, P, N_min):
    N = np.sum(M)
    S = [float(x) / N for x in M]

    E1 = []
    for i in range(len(S)):
        if S[i] != 0:
            E1.append(S[i] * math.log(S[i] / P[i]))
    MI = np.sum(E1)
    E = 2 * N_min * MI * cal_power
    CS = 1 - stats.chi2.cdf(E, len(S) - 1)

    return CS


def calculate_information():
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
    x = np.zeros((len(globals.CQ_assess) + len(globals.TQ_assess), len(p) + 1))
    info_per_variable = np.zeros((len(globals.CQ_values) + len(globals.TQ_index), len(globals.experts)))
    inf_var = []
    Info_score_real = np.zeros(len(globals.experts))
    Info_score_tot = np.zeros(len(globals.experts))
    Info_score_tot_tq = np.zeros((len(globals.TQ_index), len(globals.experts)))
    Info_score_tot_CQ_asses = np.zeros((len(globals.CQ_values), len(globals.experts)))

    i = 0

    for CQ_value in globals.CQ_values:
        if CQ_value.value > -900 and str(CQ_value.value) != "":
            lowvals[i] = CQ_value.value
            higvals[i] = CQ_value.value

            for CQ_asses in globals.CQ_assess:
                if CQ_value.name == CQ_asses.prod_name:
                    if CQ_asses.vals[0] > -900:
                        for j in range(len(CQ_asses.vals)):
                            if lowvals[i] > CQ_asses.vals[j]:
                                lowvals[i] = CQ_asses.vals[j]
                            if higvals[i] < CQ_asses.vals[j]:
                                higvals[i] = CQ_asses.vals[j]
            nexp = 0
            for expert in globals.experts:
                suma = 0
                if CQ_value.dist.lower() == "uni":
                    x_o[i] = lowvals[i] - globals.k * (higvals[i] - lowvals[i])
                    x_n[i] = higvals[i] + globals.k * (higvals[i] - lowvals[i])
                    for CQ_asses in globals.CQ_assess:
                        if CQ_value.name == CQ_asses.prod_name and CQ_asses.exp_id == expert.id:
                            if CQ_asses.vals[0] > -900:
                                x[i] = np.concatenate(
                                    [[x_o[i]], [CQ_asses.vals[ii] for ii in range(len(globals.quants))], [x_n[i]]],
                                    axis=None)
                            else:
                                x[i] = np.zeros(len(globals.quants) + 2)

                elif CQ_value.dist.lower() == "log_uni" or CQ_value.dist.lower() == "log":
                    x_o[i] = math.log(lowvals[i]) - globals.k * (math.log(higvals[i]) - math.log(lowvals[i]))
                    x_n[i] = math.log(higvals[i]) + globals.k * (math.log(higvals[i]) - math.log(lowvals[i]))
                    for CQ_asses in globals.CQ_assess:
                        if CQ_value.name == CQ_asses.prod_name and CQ_asses.exp_id == expert.id:
                            if CQ_asses.vals[0] > -900:
                                x[i] = np.concatenate(
                                    [[x_o[i]], [math.log(CQ_asses.vals[ii]) for ii in range(len(globals.quants))],
                                     [x_n[i]]],
                                    axis=None)
                            else:
                                x[i] = np.zeros(len(globals.quants) + 2)

                for j in range(len(p)):
                    if (x[i, j + 1] - x[i, j]) != 0:
                        suma = suma + p[j] * math.log(p[j] / (x[i, j + 1] - x[i, j]))

                if suma != 0:
                    info_per_variable[i][nexp] = math.log(x_n[i] - x_o[i]) + suma
                else:
                    info_per_variable[i][nexp] = 0

                nexp = nexp + 1
            inf_var.append(CQ_value.id)

        i = i + 1
    iexp = 0
    for expert in globals.experts:
        iprod = 0
        for CQ_value in globals.CQ_values:
            Info_score_real[iexp] = Info_score_real[iexp] + info_per_variable[iprod][iexp] / (
                    len(globals.CQ_values) - expert.unanswered_cal)
            iprod = iprod + 1
        iexp = iexp + 1

    for TQ_value in globals.TQ_values:
        lowvals[i] = 100000.
        higvals[i] = -100000.
        for TQ_asses in globals.TQ_assess:
            if TQ_value.name == TQ_asses.prod_name:
                for j in range(len(TQ_asses.vals)):
                    if TQ_asses.vals[0] > -900:
                        if lowvals[i] > TQ_asses.vals[j]:
                            lowvals[i] = TQ_asses.vals[j]
                        if higvals[i] < TQ_asses.vals[j]:
                            higvals[i] = TQ_asses.vals[j]
        nexp = 0
        # just loop over the globals.experts now!
        for expert in globals.experts:

            sumb = 0
            if TQ_value.dist.lower() == "uni":

                x_o[i] = lowvals[i] - globals.k * (higvals[i] - lowvals[i])
                x_n[i] = higvals[i] + globals.k * (higvals[i] - lowvals[i])
                for TQ_asses in globals.TQ_assess:
                    if TQ_value.name == TQ_asses.prod_name and TQ_asses.exp_id == expert.id:
                        if TQ_asses.vals[0] > -900:
                            x[i] = np.concatenate(
                                [[x_o[i]], [TQ_asses.vals[ii] for ii in range(len(globals.quants))], [x_n[i]]],
                                axis=None)
                        else:
                            x[i] = np.zeros(len(globals.quants) + 2)
                        # x[i] = [x_o[i], TQ_asses.vals[0], TQ_asses.vals[1], TQ_asses.vals[2], x_n[i]]
            elif TQ_value.dist.lower() == "log_uni" or TQ_value.dist.lower() == "log":
                x_o[i] = math.log(lowvals[i]) - globals.k * (math.log(higvals[i]) - math.log(lowvals[i]))
                x_n[i] = math.log(higvals[i]) + globals.k * (math.log(higvals[i]) - math.log(lowvals[i]))
                for TQ_asses in globals.TQ_assess:
                    if TQ_value.name == TQ_asses.prod_name and TQ_asses.exp_id == expert.id:
                        if TQ_asses.vals[0] > -900:
                            x[i] = np.concatenate(
                                [[x_o[i]], [math.log(TQ_asses.vals[ii]) for ii in range(len(globals.quants))], [x_n[i]]],
                                axis=None)
                        else:
                            x[i] = np.zeros(len(globals.quants) + 2)

            for j in range(len(p)):
                if (x[i, j + 1] - x[i, j]) != 0:
                    sumb = sumb + p[j] * math.log(p[j] / (x[i, j + 1] - x[i, j]))

            if sumb != 0:
                info_per_variable[i][nexp] = math.log(x_n[i] - x_o[i]) + sumb
            else:
                info_per_variable[i][nexp] = 0

            inf_var.append(TQ_value.id)
            nexp = nexp + 1
        i = i + 1

    iexp = 0
    for expert in globals.experts:
        for j in range(len(globals.CQ_values) + len(globals.TQ_index)):
            Info_score_tot[iexp] = Info_score_tot[iexp] + info_per_variable[j][iexp] / (
                    len(globals.CQ_values) + len(globals.TQ_index) - expert.unanswered_cal - expert.unanswered_tq)
        for j in range(len(globals.CQ_values)):
            Info_score_tot_CQ_asses[j][iexp] = info_per_variable[j][iexp]
        for j in range(len(globals.TQ_index)):
            Info_score_tot_tq[j][iexp] = info_per_variable[j + len(globals.CQ_values)][iexp]
        iexp = iexp + 1

    return Info_score_real, Info_score_tot, Info_score_tot_tq, Info_score_tot_CQ_asses, p


def global_weights(W_index):
    N_quants = len(globals.quants)
    for CQ_value in globals.CQ_values:
        if CQ_value.value > -900 and str(CQ_value.value) != "":
            for CQ_asses in globals.CQ_assess:
                if CQ_asses.vals[0] > -900:
                    if CQ_value.name == CQ_asses.prod_name:
                        for expert in globals.experts:
                            if expert.id == CQ_asses.exp_id:
                                if CQ_value.value <= CQ_asses.vals[0]:
                                    expert.M[W_index][0] = expert.M[W_index][0] + 1
                                elif CQ_value.value > CQ_asses.vals[len(globals.quants) - 1]:
                                    expert.M[W_index][len(globals.quants)] = expert.M[W_index][len(globals.quants)] + 1
                                else:
                                    for i in range(1, len(globals.quants)):
                                        if CQ_asses.vals[i - 1] < CQ_value.value <= CQ_asses.vals[i]:
                                            expert.M[W_index][i] = expert.M[W_index][i] + 1

    Info_score_real, Info_score_tot, Info_score_tot_tq, Info_score_tot_CQ_asses, p = calculate_information()

    w = 0
    w_tq = np.zeros((len(globals.experts), len(globals.TQ_index)))
    w_CQ_asses = np.zeros((len(globals.experts), len(globals.CQ_values)))

    iexp = 0
    N_min = np.sum(globals.experts[0].M[W_index])
    for expert in globals.experts:
        N_min = min([np.sum(expert.M[W_index]), N_min])
    for expert in globals.experts:
        expert.W[W_index][0] = calscore(expert.M[W_index], 1, p, N_min)
        expert.W[W_index][1] = Info_score_tot[iexp]
        expert.W[W_index][2] = Info_score_real[iexp]

        if expert.W[W_index][0] < globals.alpha:
            ind = 0
        else:
            ind = 1

        expert.W[W_index][3] = ind * expert.W[W_index][0] * expert.W[W_index][2]
        w = w + expert.W[W_index][3]

        for iTQ_asses in range(len(globals.TQ_index)):
            w_tq[iexp][iTQ_asses] = Info_score_tot_tq[iTQ_asses][iexp] * ind * expert.W[W_index][0]
            expert.w_tq[iTQ_asses] = w_tq[iexp][iTQ_asses]

        for iCQ_value in range(len(globals.CQ_values)):
            w_CQ_asses[iexp][iCQ_value] = Info_score_tot_CQ_asses[iCQ_value][iexp] * ind * expert.W[W_index][0]
            expert.w_CQ_asses[iCQ_value] = w_CQ_asses[iexp][iCQ_value]
        iexp = iexp + 1

    w_tq_norm = (w_tq / np.sum(w_tq, axis=0))
    w_CQ_asses_norm = (w_CQ_asses / np.sum(w_CQ_asses, axis=0))

    iexp = 0
    for expert in globals.experts:
        expert.W[W_index][4] = expert.W[W_index][3] / w
        expert.w_tq_norm = w_tq_norm[iexp]
        expert.w_CQ_asses_norm = w_CQ_asses_norm[iexp]
        iexp = iexp + 1
    return
