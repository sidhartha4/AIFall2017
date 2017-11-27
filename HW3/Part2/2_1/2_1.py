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

    print(len(a))
    totalElements = 0
    correctItems = 0


    confusionMat = np.zeros((2,2))
    testClassValues = np.zeros(2)

    findClass = np.zeros(2)



    for element in a:

        totalElements = totalElements + 1
        matVal = element[0]

        for iClass in range(0,2):
            findClass[iClass] = math.log(pClass[iClass])

        for i in range(0, len(matVal)):
            for j in range(0, len(matVal[i])):
                valToAdd = i * 10 + j
                if matVal[i][j] == " ":
                    for kClass in range(0,2):
                        findClass[kClass] += math.log(featureLabel[kClass][valToAdd][0])
                else:
                    for kClass in range(0,2):
                        findClass[kClass] += math.log(featureLabel[kClass][valToAdd][1])

        classified = np.argmax(findClass)

        if classified == int(element[1]):
            correctItems += 1

        testClassValues[int(element[1])] += 1
        confusionMat[int(element[1])][classified] += 1

    for j in range(0,testClassValues.shape[0]):
        confusionMat[j] = confusionMat[j]*100/testClassValues[j] 


    print(float(correctItems)/totalElements)
    print(confusionMat)

def naiveBayes(a):
    pClass = np.zeros(2)

    featureLabel = np.zeros((2, 250, 2))

    totalElements = 0
    for element in a:
        pClass[element[1]]  = pClass[element[1]]  + 1
        totalElements = totalElements + 1
        matVal = element[0]
        for i in range(0, len(matVal)):
            for j in range(0, len(matVal[i])):
                valToAdd = i * 10 + j
                if matVal[i][j] == " ":
                    featureLabel[element[1]][valToAdd][0] += 1
                else:
                    featureLabel[element[1]][valToAdd][1] += 1

    kVal = 3

    for iterV in range(0,2):
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
        if i % 28 == 25 or i % 28 == 26 or i % 28 == 27:
            continue

        image.append(yesContentTrain[i][:-1]) 

        if i % 28 == 24:
            tupleToAdd = (image, 1)
            trainPair.append(tupleToAdd)
            image = []

    #train for no
    for i in range(0,len(noContentTrain)):
        if i % 28 == 25 or i % 28 == 26 or i % 28 == 27:
            continue

        image.append(noContentTrain[i][:-1]) 

        if i % 28 == 24:
            tupleToAdd = (image, 0)
            trainPair.append(tupleToAdd)
            image = []


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

    with open('testPair.json', 'w') as fp:
        json.dump(testPair, fp)




if __name__ == "__main__":
    convertToPickle("data")
    naiveBWrapper()
