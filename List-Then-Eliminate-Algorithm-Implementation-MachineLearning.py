# Emilio Esposito
# Machine Learning
# Part B List then Eliminate Algorithm

import sys
import itertools
import copy

with(open("4Cat-Train.labeled", "r")) as f:
    trainDoc = f.read()

# this fcn takes a document after read() and converts it into 2 lists-of-lists
# first return is is is form df[row][column] and second is dfT[column][row]
def dataframe(doc):
    lines = doc.split("\n")

    df = []

    # read file into list of lists
    for r in range(0, len(lines)):
        # make sure it's not a null line
        if lines[r] != "":
            # split record into distinct attributes
            attr = lines[r].split("\t")
            # create an empty list to hold row contents
            df.append([])
            # iterate through each attr pair and only store the value
            for c in range(0, len(attr)):
                df[r].append(attr[c].split(" ")[1].rstrip())

    # get transposed df: dfT
    dfT = []
    for c in range(0, len(df[0])):
        dfT.append([])
        for r in range(0, len(df)):
            dfT[c].append(df[r][c])

    return df, dfT

# first return is is is form df[row][column] and second is dfT[column][row]
train, trainT = dataframe(trainDoc)

# find input space size |x|
xLen = 1
# find unique values of each X input (exclude last output col)
for attr in trainT[:len(trainT)-1]:
    xLen *= len(set(attr))

# find concept space size |C|
cLen = 2 ** xLen

# find hyp space size |h|
hLen = 1
for attr in trainT[:len(trainT)-1]:
    hLen *= len(set(attr)) + 1
# add null set case
hLen += 1

# output PART B 1-2
sys.stdout.write(str(xLen)+"\n")
sys.stdout.write(str(cLen)+"\n")

# PART B3 List-Then-Eliminate

# initialize  version space to set of all hypotheses

# vs = []
# # loop through each X col
# for i in range(0, len(trainT)-1):
#     vs.append([])
#     # loop through each unique value in each X col
#     for val in set(attr):
#         vs[attr].append()
#
#

vs_tuple = list(itertools.product(["low","high"], repeat=xLen))

i0 = list(set(trainT[0]))
i1 = list(set(trainT[1]))
i2 = list(set(trainT[2]))
i3 = list(set(trainT[3]))

catComb_tuple = list(itertools.product(i0, i1, i2, i3))

vs = []
for hyp in vs_tuple:
    vs.append(list(hyp))

catComb = []
for hyp in catComb_tuple:
    catComb.append(list(hyp))

#using VS
# train
vs_trim = copy.deepcopy(vs)
for obs in train:
    xobs = obs[:len(obs)-1]
    yobs = obs[len(obs)-1]
    for x in range(0, len(catComb)):
        if xobs == catComb[x]:
            for concept in vs:
                if yobs == "high" and concept[x] == "low":
                    vs_trim.remove(concept)
                        # print "del"
                elif yobs == "low" and concept[x] == "high":
                    vs_trim.remove(concept)
                        # print "del"
    vs = copy.deepcopy(vs_trim)


sys.stdout.write(str(len(vs))+"\n")

# PART B4 - Testing
with(open(sys.argv[1], "r")) as f:
    testDoc = f.read()

test, testT = dataframe(testDoc)

for obs in test:
    xobs = obs[:len(obs)-1]
    yobs = obs[len(obs)-1]
    highcount = 0
    for x in range(0, len(catComb)):
        if xobs == catComb[x]:
            for c in vs:
                if c[x] == "high":
                    highcount += 1
    lowcount = len(vs) - highcount
    sys.stdout.write(str(highcount)+" "+str(lowcount)+"\n")