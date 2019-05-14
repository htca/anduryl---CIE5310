import filecmp
import os
import warnings
import sys
import numpy as np

import backup
import globals
import revert
import unanswered
from Checking_Robustness import Checking_Robustness_items
from DM_optimization import DM_optimization
from calculate_DM_global import calculate_DM_global
from calculate_DM_item import calculate_DM_item
from globalweights import global_weights
from importascii import importfiles
from plot_robustness import plot_robust
from plotting_itemwise import plotting_itemwise
from print_data import print_data
from randomise import randomise
from setupinput import setupinput
from check_input import check_input


def anduryl(assessments, realisations, quants, alpha, k, cal_power, weight_type, optimization, robust, N_max_it, N_max_ex, output,
               output_items, user_w):

    globals.init(alpha, k, cal_power, weight_type, optimization, robust, N_max_it, N_max_ex, quants)

    warnings.filterwarnings("ignore")

    if not os.path.exists(output_items[0]):
        os.makedirs(output_items[0])

    importfiles(assessments, realisations, quants)
    error, errortext = check_input()
    print (errortext)
    unanswered.unanswered()
    backup.backup()

    # caluclate DMs
    if not optimization:
        if weight_type == 'global':
            global_weights(0)
            calculate_DM_global(0)
        elif weight_type == 'equal':
            for expert in globals.experts:
                expert.W[0][4] = float(1. / len(globals.experts))
            globals.alpha = 0
            calculate_DM_global(0)
        elif weight_type == 'item':
            global_weights(0)
            calculate_DM_item(0)
        elif weight_type == 'user':
            if len(user_w) == 0:
                print("user weight not specified, considering all equal weights")
                for i in range(len(globals.experts)):
                    user_w.append(1.0)
            if len(user_w) != len(globals.experts):
                sys.exit("user weight does not have the same length")

            i = 0
            for expert in globals.experts:
                expert.W[0][4] = float(user_w[i]) / np.sum(user_w)
                i = i + 1
            globals.alpha = 0
            calculate_DM_global(0)
    else:
        DM_optimization()

    if output[1]: print_data(output_items[1])
    if output[0]: plotting_itemwise(globals.CQ_values, globals.CQ_assess, globals.TQ_assess, globals.TQ_values,
                                    globals.experts,
                                    globals.weight_type, globals.optimization, output_items[0])
    # goto robustness
    if robust:
        if weight_type == "global" or weight_type == "item":
            w_index = 0
            revert.revert()
            incl_cal_pwr = "yes"
            robust_table_item = Checking_Robustness_items(incl_cal_pwr, cal_power)

            if output[0]: plot_robust(robust_table_item, output_path)
            w_index = 0
            revert.revert()

    randomisation = False
    if randomisation:
        distr = randomise()
        averages = np.average(distr, axis=0)
        stdevs = np.std(distr, axis=0)
        print('experts: ' + str(len(globals.experts) - 1))
        print('items: ' + str(len(globals.CQ_values)))
        print('Average     {:10.5e} {:10.5e} {:10.5e} {:10.5e} {:10.5e}'.format(averages[0],
                                                                                averages[1],
                                                                                averages[2],
                                                                                averages[3],
                                                                                averages[4]))
        print('Stdev       {:10.5e} {:10.5e} {:10.5e} {:10.5e} {:10.5e}'.format(stdevs[0],
                                                                                stdevs[1],
                                                                                stdevs[2],
                                                                                stdevs[3],
                                                                                stdevs[4]))


if __name__ == "__main__":
    # execute only if run as a script
    path = os.getcwd() + "\\data\\"
    filename1 = path + "Experts_INECC_Crecimiento_assessments.txt"
    filename2 = path + "Experts_INECC_Crecimiento_realizations.txt"
    output_path = os.getcwd() + "\\data\\output\\"
    output_file = path + "Experts_INECC_Crecimiento_realizations_output.txt"

    assessments, realisations, quants = setupinput(filename1, filename2)

    alpha = 0.05
    k = 0.1
    cal_power = 1
    optimization = False  # True or False
    weight_type = 'global'  # choose from 'equal', 'item', 'global', 'user'
    user_w = [0, 0, 0, 0, .4, .6, 0, 0, 0]
    robust = False  # robust analyses to execute
    N_max_it = 5  # number to exclude in robustness analysis items
    N_max_ex = 1  # number to exclude in robustness analysis experts
    Plotting = False  # create graphs
    Printing = True  # create numerical data
    Output = [Plotting, Printing]
    output_items = [output_path, output_file]
    anduryl(assessments, realisations, quants, alpha, k, cal_power, weight_type, optimization, robust, N_max_it, N_max_ex, Output,
               output_items, user_w)

