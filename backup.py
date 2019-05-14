import globals
import copy


def backup():
    global quants_bu
    global CQ_values_bu
    global CQ_assess_bu
    global TQ_index_bu
    global TQ_assess_bu
    global TQ_values_bu
    global experts_bu

    quants_bu = copy.deepcopy(globals.quants)
    CQ_values_bu = copy.deepcopy(globals.CQ_values)
    CQ_assess_bu = copy.deepcopy(globals.CQ_assess)
    TQ_index_bu = copy.deepcopy(globals.TQ_index)
    TQ_assess_bu = copy.deepcopy(globals.TQ_assess)
    TQ_values_bu = copy.deepcopy(globals.TQ_values)
    experts_bu = copy.deepcopy(globals.experts)
    return
