import globals
import backup
import copy


def revert():
    globals.quants = copy.deepcopy(backup.quants_bu)
    globals.CQ_values = copy.deepcopy(backup.CQ_values_bu)
    globals.CQ_assess = copy.deepcopy(backup.CQ_assess_bu)
    globals.TQ_index = copy.deepcopy(backup.TQ_index_bu)
    globals.TQ_assess = copy.deepcopy(backup.TQ_assess_bu)
    globals.TQ_values = copy.deepcopy(backup.TQ_values_bu)
    globals.experts = copy.deepcopy(backup.experts_bu)
    return
