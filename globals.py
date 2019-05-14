import copy


def init(alpha_inp, k_inp, cal_power_inp, weight_type_inp, optimization_inp, robust_inp, N_max_it_inp, N_max_ex_inp,
         quants_inp):
    global alpha
    global k
    global cal_power
    global weight_type
    global optimization
    global robust
    global N_max_it
    global N_max_ex
    global quants
    global CQ_values
    global CQ_assess
    global TQ_index
    global TQ_assess
    global TQ_values
    global experts
    global N_quant

    alpha = alpha_inp
    k = k_inp
    cal_power = cal_power_inp
    weight_type = weight_type_inp
    optimization = optimization_inp
    robust = robust_inp
    N_max_it = N_max_it_inp
    N_max_ex = N_max_ex_inp
    quants = quants_inp

    CQ_values = []
    CQ_assess = []
    TQ_index = []
    TQ_assess = []
    TQ_values = []
    experts = []
    N_quant = len(quants)
    return
