import numpy as np
import globals


class CQ_values_class:
    def __init__(self, id, name, value, dist):
        self.id = id
        self.name = name
        self.value = value
        self.dist = dist
        self.DM = []
        self.X_DM = []
        self.f_DM = []
        self.F_DM = []


class TQ_values_class:
    def __init__(self, id, name, value, dist):
        self.id = id
        self.name = name
        self.value = value
        self.dist = dist
        self.DM = []
        self.X_DM = []
        self.f_DM = []
        self.F_DM = []


class CQ_assesing:
    def __init__(self, exp_id, exp_name, prod_id, prod_name, prod_dist, vals):
        self.exp_id = exp_id
        self.exp_name = exp_name
        self.prod_id = prod_id
        self.prod_name = prod_name
        self.prod_dist = prod_dist
        self.vals = vals


class TQ_assess:
    def __init__(self, exp_id, exp_name, prod_id, prod_name, prod_dist, vals):
        self.exp_id = exp_id
        self.exp_name = exp_name
        self.prod_id = prod_id
        self.prod_name = prod_name
        self.prod_dist = prod_dist
        self.vals = vals


class exp:
    def __init__(self, id, name, w_item_tq, w_CQ_asses, N_quant):
        self.id = id
        self.name = name
        self.M = np.zeros((2, N_quant + 1))
        self.W = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
        self.x = [0, 0, 0]
        self.w_CQ_asses = w_CQ_asses
        self.w_CQ_asses_norm = w_CQ_asses
        self.w_tq = w_item_tq
        self.w_tq_norm = w_item_tq
        self.unanswered_cal = 0
        self.unanswered_tq = 0


def importfiles(assessments, realisations, quants):
    CQ_values = []
    CQ_assess = []
    TQ_index = []
    TQ_assess = []
    TQ_values = []
    CQ_index = []
    experts = []
    N_quant = len(quants)
    precision = 1E-15

    # realisations
    for i in range(len(realisations)):
        if float(realisations[i][2]) > -9.900E+0002:
            CQ_index.append(realisations[i][1])
            CQ_values.append(CQ_values_class(int(realisations[i][0]), (realisations[i][1]), float(realisations[i][2]), (realisations[i][3])))
            globals.CQ_values.append(CQ_values_class(int(realisations[i][0]), (realisations[i][1]), float(realisations[i][2]), (realisations[i][3])))
        else:
            TQ_index.append(realisations[i][1])
            TQ_values.append(TQ_values_class(int(realisations[i][0]), (realisations[i][1]), float(realisations[i][2]), (realisations[i][3])))
            globals.TQ_index.append((realisations[i][1]))
            globals.TQ_values.append(
                TQ_values_class(int(realisations[i][0]), (realisations[i][1]), float(realisations[i][2]), (realisations[i][3])))

    # CQ_assesing
    for i in range(len(assessments)):
        if (assessments[i][3]) in TQ_index:
            TQ_assess.append(CQ_assesing(int(assessments[i][0]), (assessments[i][1]), int(assessments[i][2]), (assessments[i][3]), (assessments[i][4]),
                               [float(assessments[i][j]) for j in range(5, 5 + N_quant)]))
            vals = []
            for j in range(5, 5 + N_quant):
                vals.append(float(assessments[i][j]))
                # if 0 != 0:
                #     vals.append(precision)
                # else:
                #     vals.append(float(assessments[i][j]))
            globals.TQ_assess.append(
                CQ_assesing(int(assessments[i][0]), (assessments[i][1]), int(assessments[i][2]), (assessments[i][3]), (assessments[i][4]), vals))
        elif (assessments[i][3]) in CQ_index:
            CQ_assess.append(CQ_assesing(int(assessments[i][0]), (assessments[i][1]), int(assessments[i][2]), (assessments[i][3]), (assessments[i][4]),
                                 [float(assessments[i][j]) for j in range(5, 5 + N_quant)]))
            vals = []
            for j in range(5, 5 + N_quant):
                vals.append(float(assessments[i][j]))
                # if 0 != 0:
                #     vals.append(precision)
                # else:
                #     vals.append(float(assessments[i][j]))
            globals.CQ_assess.append(
                CQ_assesing(int(assessments[i][0]), (assessments[i][1]), int(assessments[i][2]), (assessments[i][3]), (assessments[i][4]), vals))
        else:
            # huh! there is CQ_assesing without realisation, consider it as a targetquestion!
            TQ_assess.append(CQ_assesing(int(assessments[i][0]), (assessments[i][1]), int(assessments[i][2]), (assessments[i][3]), (assessments[i][4]),
                               [float(assessments[i][j]) for j in range(5, 5 + N_quant)]))
            vals = []
            for j in range(5, 5 + N_quant):
                vals.append(float(assessments[i][j]))
            globals.TQ_assess.append(
                CQ_assesing(int(assessments[i][0]), (assessments[i][1]), int(assessments[i][2]), (assessments[i][3]), (assessments[i][4]), vals))

            # add to tqs index
            TQ_index.append((assessments[i][3]))
            globals.TQ_index.append((assessments[i][3]))

            # add to TQ_assess CQ_values array
            TQ_values.append(TQ_values_class(int(assessments[i][2]), (assessments[i][3]), -995., (assessments[i][4])))
            globals.TQ_values.append(
                TQ_values_class(int(assessments[i][2]), (assessments[i][3]), -995., (assessments[i][4])))

    for i in np.unique(assessments[:, 0]):
        name = ""
        for j in range(len(assessments)):
            if i == assessments[j][0]:
                name = assessments[j][1]
        globals.experts.append(exp(int(i), name, np.zeros(len(TQ_index)), np.zeros(len(CQ_values)), N_quant))

    return
