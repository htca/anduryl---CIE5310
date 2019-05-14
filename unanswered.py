import globals
import numpy as np


def unanswered():
    unanswered_questions = []
    for CQ_asses in globals.CQ_assess:
        if CQ_asses.vals[0] < -900:
            # consider unanswered!
            unanswered_questions.append(CQ_asses.prod_id)
            for expert in globals.experts:
                if CQ_asses.exp_id == expert.id:
                    expert.unanswered_cal = expert.unanswered_cal + 1

    for TQ_asses in globals.TQ_assess:
        if TQ_asses.vals[0] < -900:
            # consider unanswered!
            unanswered_questions.append(TQ_asses.prod_id)
            for expert in globals.experts:
                if TQ_asses.exp_id == expert.id:
                    expert.unanswered_tq = expert.unanswered_tq + 1

    # for prod_id in np.unique(unanswered_questions):
    #     for CQ_value in globals.CQ_values:
    #         if CQ_value.id == prod_id:
    #             globals.CQ_values.remove(CQ_value)
    #     for CQ_asses in globals.CQ_assess:
    #         if CQ_asses.prod_id == prod_id:
    #             globals.CQ_assess.remove(CQ_asses)

    return
