#!/usr/bin/env python

### Import packages, declare variables
from random import *
from math import *
import csv
import numpy as np
from munkres import Munkres, print_matrix
generate = False
with open('cost_function.txt') as f:
    content = f.readlines()
def cost_function(L, F): 
    return eval(content[0])

### Get Cost Matrix
def random_ranking(numrow,numcol):
    mat = [["O" for a in range(numcol)] for b in range(numrow)]  # final combined preference matrix [numrow x numcol]
    for row in range(numrow):
        temp = []
        for i in range(1, numcol + 1):
            temp.append(i)
        shuffle(temp)
        mat[row] = temp
    return np.array(mat)

def makelist(prefix, n):
    values = []
    for i in range(n):
        values.append("%s%d" % (prefix,i))
    return values

if (generate):
    # Create a random set of preference for each leader, append into matrix1
    seed(12345)
    num_leaders = 8
    num_follow = 12
    matrix1 = random_ranking(num_leaders,num_follow)
    matrix2 = random_ranking(num_follow,num_leaders)
    leaderlist = dict(zip(range(numrow), makelist("L",numrow)))
    followerlist = dict(zip(range(numcol), makelist("F",numcol)))
    numrow = num_leaders
    numcol = num_follow
else:
    L_input = csv.reader(open("leader_matrix.csv","rb"),delimiter=',')
    L_header = next(L_input)
    L_header = [L_header[i] for i in range(1,len(L_header))]
    matrix1 = np.array(list(L_input))[:, 1:].astype(np.integer)
    F_input = csv.reader(open("follower_matrix.csv","rb"),delimiter=',')
    F_header = next(F_input)
    F_header = [F_header[i] for i in range(1,len(F_header))]
    matrix2 = np.array(list(F_input))[:, 1:].astype(np.integer)
    numrow = matrix1.shape[0]
    numcol = matrix1.shape[1]
    leaderlist = dict(zip(range(numrow), F_header))
    followerlist = dict(zip(range(numcol), L_header))

matrix = cost_function(matrix1,matrix2.T)
matrix_original = matrix.copy()

# Print Function
def printmatrix(matrix, dict1, dict2, sides): 
    left_bottom = np.array(np.c_[dict1.values(), matrix])
    if (sides):
        top = np.array([''] + dict2.values())[np.newaxis]
        matrix = np.r_[top, left_bottom]
    s = [[str(e) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print '\n'.join(table)

print("\nPREFERENCE MATRIX FOR LEADERS (LEADERS LEFT X FOLLOWERS TOP)")
printmatrix(matrix1, leaderlist, followerlist, False)
print("\nPREFERENCE MATRIX FOR FOLLOWERS (FOLLOWERS LEFT X LEADERS TOP)")
printmatrix(matrix2, followerlist, leaderlist, False)
print("\nCOMBINED PREFERENCE MATRIX (LEADERS LEFT X FOLLOWERS TOP)")
printmatrix(matrix, leaderlist, followerlist, False)

### Leader Scores
print("\nLEADER SCORES")
leader_scores = np.mean(matrix2, axis=1)
for i in np.argsort(leader_scores):
    print '%s: %s' % (leaderlist.values()[i], round(leader_scores[i],2))

### Follower Scores
print("\nFOLLOWER SCORES")
follow_scores = np.mean(matrix1, axis=0)
for i in np.argsort(follow_scores):
    print '%s: %s' % (followerlist.values()[i], round(follow_scores[i],2))

m = Munkres()
indexes = m.compute(matrix)
print("\nFINAL PARTNER ASSIGNMENTS: (N[X] means Person N was given their Xth choice)")
print("------------------------------------------------------------")
csv_write = csv.writer(open('match_outputs.csv','wb'),delimiter = ',',quoting=csv.QUOTE_MINIMAL)
csv_write.writerow(['Leader_Name','Choice_Received','Follower_Name','Choice_Received','Penalty'])
total = 0
for row, col in indexes:
    value = matrix_original[row][col]
    total += value
    csv_write.writerow([leaderlist[row], matrix1[row,col], followerlist[col], matrix2[col, row], value])
    print '%s[%d] + %s[%d] >>> %d' % (leaderlist[row], matrix1[row,col], followerlist[col], matrix2[col, row], value)
print 'Total Penalty: %d' % total
csv_write.writerow(['\nTotal Penalty\n', total])

# STABLE MATCH ALGORITHM: FAVORS LEADERS
if numrow == numcol:
    print("\n\nSTABLE MATCH ALGORITHM:")
    singlelist = [0 for a in range(numrow)]  # 0=single
    choicelist = [numrow + 1 for a in range(numcol)]  # all high numbers
    tempmatrix = matrix1.copy()
    print('Starting State')
    print(singlelist)
    print(choicelist)
    print
    counter = 1
    while sorted(singlelist)[0] == 0:  # main algorithm loop, per round
        print("\nROUND #%s" % counter)
        for n in range(len(tempmatrix)):  # For each suitor
            if singlelist[n] == 0:  # If they're single
                p = np.argmin(tempmatrix[n])#tempmatrix[n].index(min(tempmatrix[n]))  # col identifying their first choice
                print("Suitor %s Proposes to Lady %s (His #%s choice)" % (n + 1, p + 1, min(tempmatrix[n])))
                tempmatrix[n][p] = 99  # removes from consideration for next round
                if choicelist[p] > matrix2[p][
                    n]:  # hate of former suitor > hate of new suitor i.e. if you want to trade
                    if choicelist[p] != numrow + 1:
                        print("TRADE UP - Lady drops Suitor %s" % (1 + matrix2[p].tolist().index(choicelist[p])))
                        singlelist[matrix2[p].tolist().index(choicelist[p])] = 0  # set jinked suitor to single
                    singlelist[n] = min(tempmatrix[n]) - 1  # set new suitor to engaged
                    choicelist[p] = matrix2[p][n]  # completes replacement
                else:
                    print("REJECTION")
                print(singlelist)
                print(choicelist)
                print
        counter += 1
    setsum = 0
    print("STABLE MATCH COMPLETE: (N[X] means Person N was given their Xth choice)")
    print("------------------------------------------------------------")
    for row in leaderlist:
        followid = matrix1[row].tolist().index(singlelist[row])
        print('%s[%s] + %s[%s] >>> %s' % (leaderlist[row], singlelist[row], followerlist[followid], 
                                        matrix2[followid,row], matrix_original[row,followid]))
        setsum += matrix_original[row,followid]
    print("PENALTY: " + str(setsum) + "\n")
else:
    print("SKIPPED: STABLE MATCH REQUIRES SQUARE COST MATRIX")



