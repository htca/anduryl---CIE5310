import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.axisartist as axisartist


def plotting_itemwise(CQ_values, CQ_assess, TQ_assess, TQ_values, experts, weight_type, optimization, output_path):
    def format_axes(ax):
        ax.margins(0.2)
        ax.set_axis_off()

    if optimization:
        opt_text = " optimised"
    else:
        opt_text = ""
    i = 0
    for CQ_value in CQ_values:
        expnames = []
        valuestoplot = []
        for expert in experts:
            expnames.append(expert.name)
            for CQ_asses in CQ_assess:
                if CQ_value.id == CQ_asses.prod_id and expert.id == CQ_asses.exp_id:
                    valuestoplot.append(CQ_asses.vals)
        expnames.append("Realisation")
        valuestoplot.append([CQ_value.value])
        plt.figure(figsize=(15, 7.5))
        for k in range(len(expnames)):
            plt.plot(valuestoplot[k], [expnames[k] for j in range(len(valuestoplot[k]))], "-o")
        plt.title((CQ_value.name + " " + weight_type + opt_text).decode('unicode-escape'))
        plt.ylabel(u"Expert")
        plt.savefig(output_path + CQ_value.name + ".png")

    for CQ_value in TQ_values:
        expnames = []
        valuestoplot = []
        for expert in experts:
            expnames.append(expert.name)
            for TQ_asses in TQ_assess:
                if CQ_value.id == TQ_asses.prod_id and expert.id == TQ_asses.exp_id:
                    valuestoplot.append(TQ_asses.vals)
        plt.figure(figsize=(15, 7.5))
        for k in range(len(expnames)):
            plt.plot(valuestoplot[k], [expnames[k] for j in range(len(valuestoplot[k]))], "-o")
        plt.title((CQ_value.name + " " + weight_type + opt_text).decode('unicode-escape'))
        plt.ylabel(u"Expert")
        plt.savefig(output_path + CQ_value.name + ".png")

    return
