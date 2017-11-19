#import pandas as pd
import pickle
import json
import numpy as np
import math

def findClassLabel():

    outfile = "pClass.npy"
    pClass = np.load(outfile)

    outfile = "featureLabel.npy"
    featureLabel = np.load(outfile)

    a = 0

    with open('testPair.json') as fh:
        a = json.load(fh)

    totalElements = 0
    correctItems = 0

    findClass = np.zeros(10)

    for element in a:

        totalElements = totalElements + 1
        matVal = element[0]

        for iClass in range(0,10):
            findClass[iClass] = math.log(pClass[iClass])

        for i in range(0, len(matVal)):
            for j in range(0, len(matVal[i])):
                valToAdd = i* 28 + j
                if matVal[i][j] == " ":
                    for kClass in range(0,10):
                        findClass[kClass] += math.log(featureLabel[kClass][valToAdd][0])
                else:
                    for kClass in range(0,10):
                        findClass[kClass] += math.log(featureLabel[kClass][valToAdd][1])

        classified = np.argmax(findClass)

        if classified == int(element[1]):
            correctItems += 1

    print(float(correctItems)/totalElements)

def naiveBayes(a):
    pClass = np.zeros(10)

    featureLabel = np.zeros((10, 784, 2))

    totalElements = 0
    for element in a:
        pClass[element[1]]  = pClass[element[1]]  + 1
        totalElements = totalElements + 1
        matVal = element[0]
        for i in range(0, len(matVal)):
            for j in range(0, len(matVal[i])):
                valToAdd = i* 28 + j
                if matVal[i][j] == " ":
                    featureLabel[element[1]][valToAdd][0] += 1
                else:
                    featureLabel[element[1]][valToAdd][1] += 1

    kVal = 10

    for iterV in range(0,10):
        #print(featureLabel[iterV])
        featureLabel[iterV] = (featureLabel[iterV]+kVal) /(pClass[iterV]+2*kVal)

        #print(featureLabel[iterV])

    pClass = pClass/totalElements

    outfile = "pClass.npy"
    np.save(outfile, pClass)

    outfile = "featureLabel.npy"
    np.save(outfile, featureLabel)

    print(pClass)


def naiveBWrapper():
    a = 0

    with open('trainPair.json') as fh:
        a = json.load(fh)

    print(len(a))
    naiveBayes(a)
    findClassLabel()




def convertToPickle(fileName):

    yesContentTrain = None
    with open(fileName + "/yes_train.txt") as f:
        yesContentTrain = f.readlines()

    noContentTrain = None
    with open(fileName + "/no_train.txt") as f:
        noContentTrain = f.readlines()

    # train for yes
    trainPair = []
    image = []
    #print(len(yesContentTrain[0]))
    for i in range(0,len(yesContentTrain)):
        print(yesContentTrain[i][-1:])
        image.append(yesContentTrain[i][-1:]) 

        if i % 25 == 24:
            tupleToAdd = (image, 1)
            trainPair.append(tupleToAdd)
            image = []
            i += 3

    #train for no
    for i in range(0,len(noContentTrain)):
        image.append(noContentTrain[i][-1:]) 

        if i % 25 == 24:
            tupleToAdd = (image, 0)
            trainPair.append(tupleToAdd)
            image = []
            i += 3


    with open('trainPair.json', 'w') as fp:
        json.dump(trainPair, fp)

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
        image.append(yesContentTest[i][-1:]) 

        if i % 25 == 24:
            tupleToAdd = (image, 1)
            testPair.append(tupleToAdd)
            image = []
            i += 3

    #test for no
    for i in range(0,len(noContentTest)):
        image.append(noContentTest[i][-1:]) 

        if i % 25 == 24:
            tupleToAdd = (image, 0)
            testPair.append(tupleToAdd)
            image = []
            i += 3

    with open('testPair.json', 'w') as fp:
        json.dump(testPair, fp)




if __name__ == "__main__":
    convertToPickle("data")
    naiveBWrapper()
