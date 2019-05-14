import operator
import globals


def print_data(outputfile):
    index = 0
    print(" Id    name   Cal         inf items   inf seeds   W           W_norm")
    for expert in globals.experts:
        print('{:3} {:>7} {:10.5e} {:10.5e} {:10.5e} {:10.5e} {:10.5e}'.format(expert.id, expert.name,
                                                                               expert.W[index][0],
                                                                               expert.W[index][1],
                                                                               expert.W[index][2],
                                                                               expert.W[index][3],
                                                                               expert.W[index][4]))

    print("CQ_assesing quantiles")
    print(" Id     Low        5%         50%        95%        high")
    for CQ_value in globals.CQ_values:
        print('{:3} {:10.5f} {:10.5f} {:10.5f} {:10.5f} {:10.5f}'.format(CQ_value.id, CQ_value.DM[0], CQ_value.DM[1],
                                                                         CQ_value.DM[2], CQ_value.DM[3],
                                                                         CQ_value.DM[4]))
    print("TQ_assess quantiles")
    print(" Id     Low        5%         50%        95%        high")
    for TQ_asses in globals.TQ_values:
        print('{:3} {:10.5f} {:10.5f} {:10.5f} {:10.5f} {:10.5f}'.format(TQ_asses.id, TQ_asses.DM[0], TQ_asses.DM[1],
                                                                         TQ_asses.DM[2], TQ_asses.DM[3],
                                                                         TQ_asses.DM[4]))
    filename = open(outputfile, "w")
    index = 1
    print(" Id    name   Cal         inf items   inf seeds   W           W_norm")
    filename.write("Weight type :" + globals.weight_type + "\n")
    if globals.optimization:
        filename.write("With optimization\n")
    else:
        filename.write("Without optimization\n")
    filename.write("Number of experts:               " + str(int(len(globals.experts) - 1)) + "\n")
    filename.write("Number of calibration questions: " + str(int(len(globals.CQ_values))) + "\n")
    filename.write(" Id    name   Cal         inf items   inf seeds   W           W_norm\n")

    for expert in sorted(globals.experts, key=operator.attrgetter('id')):
        print('{:3} {:>7} {:10.5e} {:10.5e} {:10.5e} {:10.5e} {:10.5e}'.format(expert.id, expert.name,
                                                                               expert.W[index][0],
                                                                               expert.W[index][1],
                                                                               expert.W[index][2],
                                                                               expert.W[index][3],
                                                                               expert.W[index][4]))
        filename.write('{:3} {:>7} {:10.5e} {:10.5e} {:10.5e} {:10.5e} {:10.5e}\n'.format(expert.id, expert.name,
                                                                                          expert.W[index][0],
                                                                                          expert.W[index][1],
                                                                                          expert.W[index][2],
                                                                                          expert.W[index][3],
                                                                                          expert.W[index][4]))
    filename.close()


def print_data_experts(index):
    print(" Id    name   Cal         inf items   inf seeds   W           W_norm")
    for expert in globals.experts:
        print('{:3} {:>7} {:10.5e} {:10.5e} {:10.5e} {:10.5e} {:10.5e}'.format(expert.id, expert.name,
                                                                               expert.W[index][0],
                                                                               expert.W[index][1],
                                                                               expert.W[index][2],
                                                                               expert.W[index][3],
                                                                               expert.W[index][4]))
