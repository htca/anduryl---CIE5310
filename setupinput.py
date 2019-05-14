import numpy as np


def slices(s, *args):
    position = 0
    for length in args:
        yield s[position:position + length]
        position += length


def setupinput(filename1, filename2):
    dists = ["UNI", "uni", "log_uni", "LOG_UNI", "LOG", "log"]
    with open(filename1) as f:
        head = f.readline()
    f.close()
    N_quant = int(head.split()[6])

    f = open(filename1, "r")
    data1 = f.readlines()
    f.close()
    assessmentsa = []

    # read assessments
    for i in range(1, len(data1)):
        if len(data1[i]) > 1:
            fields = data1[i].split()
            dist_index = 0
            for dist in dists:
                if dist in fields:
                    dist_index = fields.index(dist)
            if dist_index != 0:
                expert = int(fields[0])
                exp_name = fields[1]
                question_id = int(fields[2])
                questiontext = ""
                for j in range(3, dist_index):
                    questiontext = questiontext + fields[j]
                dist = fields[dist_index]
                array_to_add = [expert, exp_name, question_id, questiontext, dist]
                for j in range(dist_index + 1, N_quant + dist_index + 1):
                    array_to_add.append(fields[j])
                assessmentsa.append(array_to_add)
    assessments = np.array(assessmentsa)
    questiontext=""
    assessmentsb = []
    for i in range(1, len(data1)):
        if len(data1[i]) > 1:
            fields = list(slices(data1[i], 39, 100))
            first_part = fields[0].split()
            second_part = fields[1].split()
            expert = int(first_part[0])
            exp_name = first_part[1]
            question_id = int(first_part[2])
            for j in range(3, len(first_part) - 1):
                if j == 3:
                    questiontext = first_part[j]
                else:
                    questiontext = questiontext + " " + first_part[j]
            dist = first_part[-1]
            array_to_add = [expert, exp_name, question_id, questiontext, dist]

            for j in range(0, N_quant):
                array_to_add.append(second_part[j])
            assessmentsb.append(array_to_add)
    assessments = np.array(assessmentsb)

    # read realisations
    f = open(filename2, "r")
    data2 = f.readlines()
    f.close()
    realisationsa = []
    for i in range(0, len(data2)):
        if len(data2[i]) > 1:
            fields = data2[i].split()
            dist_index = 0
            for dist in dists:
                if dist in fields:
                    dist_index = fields.index(dist)
            if dist_index != 0:
                question_id = int(fields[0])
                questiontext = ""
                for j in range(1, dist_index - 1):
                    if j == 1:
                        questiontext = fields[j]
                    else:
                        questiontext = questiontext + " " + fields[j]
                dist = fields[dist_index]
                vals = (fields[dist_index - 1])
                realisationsa.append([question_id, questiontext, vals, dist])

    realisations = np.array(realisationsa)

    f = open(filename2, "r")
    data2 = f.readlines()
    f.close()
    realisationsa = []
    for i in range(0, len(data2)):
        if len(data2[i]) > 1:
            fields = list(slices(data2[i], 21, 100))
            first_part = fields[0].split()
            second_part = fields[1].split()
            question_id = int(first_part[0])
            for j in range(1, len(first_part)):
                if j == 1:
                    questiontext = first_part[j]
                else:
                    questiontext = questiontext + " " + first_part[j]
            dist = second_part[1]
            vals = second_part[0]
            realisationsa.append([question_id, questiontext, vals, dist])

    realisations = np.array(realisationsa)

    with open(filename1) as f:
        head = f.readline()
    f.close()
    N_quant = int(head.split()[6])
    quants = [float(head.split()[i]) / 100 for i in range(8, 8 + N_quant)]

    # write tot txt files here...
    if "RLS" in filename2 or "rls" in filename2:
        rlsfile = filename2.split(".")[0] + "_realizations.txt"
        calvarfile = filename2.split(".")[0] + "_assessments.txt"
        file_rls = open(rlsfile, "w")

        file_calvar = open(calvarfile, "w")
        file_calvar.write(head)
        for line in assessments:
            string = line[0] + " " + line[1] + " " + line[2] + " " + line[3] + " " + line[4] + " "
            for i in range(N_quant):
                string += " " + line[5 + i]
            file_calvar.write(string + "\n")
        for line in realisations:
            file_rls.write(line[0] + " " + line[1] + " " + line[2] + " " + line[3] + "\n")
        file_rls.close()
        file_calvar.close()

    return assessments, realisations, quants
