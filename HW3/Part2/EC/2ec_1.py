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



from os import listdir
from os.path import isfile, join

def convertToPickle():

    mypath = "txt_yesno/training/"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    print(onlyfiles)

    trainPair = []
    for i in onlyfiles:
        readFile = open(mypath+i,"r")
        labels = i[:-4].split('_')
        print(labels)
        content = readFile.readlines()
        example = []
        for j in range(8):
            example = []
            for k in range(25):
                example.append(content[j][j*15+5:(j+1)*15])
            if labels[j] == '0':
                tupleToAdd = (example, 0)
            else:
                tupleToAdd = (example, 1)
            trainPair.append(tupleToAdd)

    with open('trainPair.json', 'w') as fp:
        json.dump(trainPair, fp)



    mypath = "txt_yesno/yes_test/"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    print(onlyfiles)

    testPair = []
    for i in onlyfiles:
        readFile = open(mypath+i, "r")
        content = readFile.readlines()
        testPair.append((content, 1))


    mypath = "txt_yesno/no_test/"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    print(onlyfiles)

    for i in onlyfiles:
        readFile = open(mypath+i, "r")
        content = readFile.readlines()
        testPair.append((content, 0))


    with open('testPair.json', 'w') as fp:
        json.dump(testPair, fp)

if __name__ == "__main__":
    convertToPickle()
    naiveBWrapper()
