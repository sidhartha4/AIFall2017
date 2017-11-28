#import pandas as pd
import pickle
import json
import numpy as np
import math
from numpy.linalg import inv



def solve(fileName):
    yesContentTrain = None
    with open(fileName + "/yes_train.txt") as f:
        yesContentTrain = f.readlines()

    noContentTrain = None
    with open(fileName + "/no_train.txt") as f:
        noContentTrain = f.readlines()

    # train for yes
    S = np.zeros((250, 250))
    mean_yes = np.zeros(250)
    yes_train = []
    image = []
    cnt = 0
    #print(len(yesContentTrain[0]))
    for i in range(0,len(yesContentTrain)):
        if i % 28 == 25 or i % 28 == 26 or i % 28 == 27:
            continue

        for j in range(len(yesContentTrain[i][:-1])):
            if yesContentTrain[i][j] == '%':
                image.append(1)
            else:
                image.append(0)

        if i % 28 == 24:
            cnt += 1
            tmp = np.array(image)
            mean_yes += tmp
            yes_train.append(tmp)
            image = []

    mean_yes /= cnt
    for ex in yes_train:
        S += (ex - mean_yes) * (ex-mean_yes)[np.newaxis, :].T

    #train for no
    mean_no = np.zeros(250)
    no_train = []
    image = []
    cnt = 0
    for i in range(0,len(noContentTrain)):
        if i % 28 == 25 or i % 28 == 26 or i % 28 == 27:
            continue

        for j in range(len(noContentTrain[i][:-1])):
            if noContentTrain[i][j] == '%':
                image.append(1)
            else:
                image.append(0)

        if i % 28 == 24:
            cnt += 1
            tmp = np.array(image)
            mean_no += tmp
            no_train.append(tmp)
            image = []

    mean_no /= cnt
    for ex in no_train:
        tmp = (ex - mean_no) * (ex - mean_no)[np.newaxis, :].T
        S += tmp

    print(mean_yes)
    print(mean_no)
    print(S)
    print(S.shape)

    w = inv(S) * (mean_yes - mean_no)
    print(w)

    yesContentTest = None
    with open(fileName + "/yes_test.txt") as f:
        yesContentTest = f.readlines()

    noContentTest = None
    with open(fileName + "/no_test.txt") as f:
        noContentTest = f.readlines()

    # test for yes
    testPair = []
    image = []
    for i in range(0,len(yesContentTest)):
        if i % 28 == 25 or i % 28 == 26 or i % 28 == 27:
            continue

        image.append(yesContentTest[i][:-1]) 

        if i % 28 == 24:
            tupleToAdd = (image, 1)
            testPair.append(tupleToAdd)
            image = []

    #test for no
    for i in range(0,len(noContentTest)):
        if i % 28 == 25 or i % 28 == 26 or i % 28 == 27:
            continue

        image.append(noContentTest[i][:-1]) 

        if i % 28 == 24:
            tupleToAdd = (image, 0)
            testPair.append(tupleToAdd)
            image = []




if __name__ == "__main__":
    solve("data")
