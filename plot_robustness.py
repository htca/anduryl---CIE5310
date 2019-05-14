import re
import numpy as np
import matplotlib.pyplot as plt


def plot_robust(data, output_path):
    N_max = 0
    for row in data:

        if isinstance(row[1], float):
            num_of_skipped = len((re.sub("[^0123456789.,]", "", row[0])).split(','))
            if num_of_skipped > N_max:
                N_max = num_of_skipped

    # create 3D array
    var1 = []

    for row in data:
        if isinstance(row[1], float):
            num_of_skipped = len((re.sub("[^0123456789.,]", "", row[0])).split(','))
            if len(var1) < num_of_skipped:
                var1.append([])
            var1[num_of_skipped - 1].append([row[1], row[2], row[3]])
    # var1(i,j,k):
    # i number of "removed"
    # j CQ_assess
    # k vars (calscore, total, real)
    data = []
    for j in range(3):
        data.append([])
        labels = []
        for i in range(len(var1)):
            data[j].append([var1[i][k][j] for k in range(len(var1[i]))])
            labels.append(str(i + 1))

        plt.figure(figsize=(15, 7.5))
        plt.xlabel("Items left out")
        plt.boxplot(np.array(data[j]), patch_artist=True, labels=labels)
        # plt.show()
        plt.savefig(output_path + "data_" + str(j) + ".png")
    # plt.boxplot(np.array(data2))
    # plt.savefig(output_path + "data2" + ".png")
    # plt.boxplot(np.array(data3))
    # plt.savefig(output_path + "data3" + ".png")
