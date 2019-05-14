import globals

def check_input():
    error = False
    i = 0
    errorstring = ""
    for i in range(len(globals.quants)):
        if globals.quants[i] <= 0 or globals.quants[i] >= 1 or not isinstance(globals.quants[i],float):
            errorstring += "Error: Quantiles not between 0 and 1; quant = " + str(globals.quants[i]) + "\n"
            error = True
        if i > 0:
            if globals.quants[i] <= globals.quants[i-1]:
                errorstring += "Error: Quantiles not in increasing order \n"
                error = True

    if globals.alpha > 0.5 or globals.alpha < 0.0 or not isinstance(globals.alpha,float):
        errorstring += "Error: alpha larger than 0.5 or smaller than 0 \n"
        error = True

    if globals.k > 1 or globals.k < 0 or not isinstance(globals.k,float):
        errorstring += "Error: k larger than 1 or smaller than 0 \n"
        error = True

    if globals.cal_power < 0 or globals.cal_power > 1 or not isinstance(globals.cal_power,(float,int)):
        errorstring += "Error: Calibration power not between 0 and 1 \n"
        error = True

    if not globals.weight_type in ['global', 'item', 'user', 'equal']:
        errorstring += "Error: Weight type: " + globals.weight_type + " is not allowed \n"
        errorstring += "       Weight type should be either 'global' , 'item', 'user' or 'equal' \n"
        error = True

    if not isinstance (globals.robust, bool):
        errorstring += "Error: Robustness must be boolean: 'True' or 'False' \n"
        error = True

    if not isinstance(globals.optimization,bool):
        errorstring += "Error: Optimisation must be boolean: 'True' or 'False' \n"
        error = True

    if globals.robust and (not isinstance(globals.N_max_it,int) or globals.N_max_it <=0 or globals.N_max_it >= len(globals.CQ_values)):
        errorstring += "Error: Robustness must be boolean 'True' or 'False' \n"
        error = True
    if globals.robust and (not isinstance(globals.N_max_ex,int) or globals.N_max_ex <=0 or globals.N_max_ex >= len(globals.experts)):
        errorstring += "Error: Robustness must be boolean 'True' or 'False' \n"
        error = True

    for CQ_value in globals.CQ_values:
        if not (CQ_value.dist.lower() == "uni" or CQ_value.dist.lower() == "log"):
            errorstring += "Error: Distribution in calibration question should be: 'log' or 'uni' \n"
            errorstring += "       " + CQ_value.name + " should be adjusted \n"
            error = True
        if not isinstance(CQ_value.value,float):
            errorstring += "Error: value should be a floating number \n"
            errorstring += "       " + CQ_value.name + " in the realisation should be adjusted \n"
            error = True
        if CQ_value.dist.lower() == "log" and (CQ_value.value <0  ):
            errorstring += "Error: Log distribution should have a positive value \n"
            errorstring += "       " + CQ_value.name + " in the realisation should be adjusted \n"
            error = True

    for TQ_value in globals.TQ_values:
        if not (TQ_value.dist.lower() == "uni" or TQ_value.dist.lower() == "log"):
            errorstring += "Error: Distribution in calibration question should be: 'log' or 'uni' \n"
            errorstring += "       " + TQ_value.name + " should be adjusted \n"
            error = True

    for CQ_assess in globals.CQ_assess:
        find_value = False
        for CQ_value in globals.CQ_values:
            if CQ_value.id == CQ_assess.prod_id:
                find_value = True
                if not CQ_value.dist.lower() == CQ_assess.prod_dist.lower():
                    errorstring += "Error: Distribution of assessment by expert does not correspond with question \n"
                    error = True
        if not find_value:
            errorstring += "Error: Assessment by expert not in questions\n"
            error = True

        i = 0
        for i in range(len(CQ_assess.vals)):
            if CQ_assess.vals[i]  > -900:
                if i > 0:
                    if CQ_assess.vals[i] <= CQ_assess.vals[i-1]:
                        errorstring += "Error: assessment not in increasing order\n"
                        errorstring += "       " + CQ_assess.prod_name + " should be adjusted \n"
                        error = True
                if not isinstance(CQ_assess.vals[i],float):
                    errorstring += "Error: assessment should be floating number \n"
                    error = True
                if CQ_assess.vals[i] <= 0 and CQ_assess.prod_dist.lower() == 'log':
                    errorstring += "Error: logarithmic distribution cannot have negative assessments\n"
                    error = True

    for TQ_assess in globals.TQ_assess:
        find_value = False
        for TQ_value in globals.TQ_values:
            if TQ_value.id == TQ_assess.prod_id:
                find_value = True
                if not TQ_value.dist.lower() == TQ_assess.prod_dist.lower():
                    errorstring += "Error: Distribution of assessment by expert does not correspond with target question \n"
                    error = True
        if not find_value:
            errorstring += "Error: Assessment by expert not in target questions\n"
            error = True

        i = 0
        for i in range(len(TQ_assess.vals)):
            if TQ_assess.vals[i] > -900:
                if i > 0:
                    if TQ_assess.vals[i] <= TQ_assess.vals[i-1]:
                        errorstring += "Error: assessment not in increasing order\n"
                        errorstring += "       " + TQ_assess.prod_name+ " should be adjusted \n"
                        error = True
                if not isinstance(TQ_assess.vals[i],float):
                    errorstring += "Error: assessment should be floating number \n"
                    error = True
                if TQ_assess.vals[i] <= 0 and TQ_assess.prod_dist.lower() == 'log':
                    errorstring += "Error: logarithmic distribution cannot have negative assessments\n"
                    error = True

    # global CQ_assess
    # global TQ_index
    # global TQ_assess
    # global experts



    return error, errorstring