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

    confusionMat = np.zeros((5,5))
    testClassValues = np.zeros(5)


    findClass = np.zeros(5)

    for element in a:

        totalElements = totalElements + 1
        matVal = element[0]

        for iClass in range(0,5):
            findClass[iClass] = math.log(pClass[iClass])

        for i in range(0, len(matVal)):
            for j in range(0, len(matVal[i])):
                valToAdd = i * 13 + j
                if matVal[i][j] == " ":
                    for kClass in range(0,5):
                        findClass[kClass] += math.log(featureLabel[kClass][valToAdd][0])
                else:
                    for kClass in range(0,5):
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
    pClass = np.zeros(5)

    featureLabel = np.zeros((5, 390, 2))

    totalElements = 0
    for element in a:
        pClass[element[1]] = pClass[element[1]] + 1
        totalElements = totalElements + 1
        matVal = element[0]
        for i in range(0, len(matVal)):
            for j in range(0, len(matVal[i])):
                valToAdd = i * 13 + j
                if matVal[i][j] == " ":
                    featureLabel[element[1]][valToAdd][0] += 1
                else:
                    featureLabel[element[1]][valToAdd][1] += 1

    kVal = 5.0

    for iterV in range(0,5):
        #print(featureLabel[iterV])
        featureLabel[iterV] = (featureLabel[iterV]+kVal) /(pClass[iterV]+2*kVal)

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
    contentTrain = None
    with open(fileName + "/training_data.txt") as f:
        contentTrain = f.readlines()
            
    contentTrainLabel = None
    with open(fileName + "/training_labels.txt") as f:
        contentTrainLabel = f.readlines()

    trainPair = []
    image = []
    mod = 33 
    #print(len(contentTrain[0]))
    for i in range(0,len(contentTrain)):
        if i % mod == mod-3 or i % mod == mod-2 or i % mod == mod-1:
            continue

        image.append(contentTrain[i][:-1]) 

        if i % mod == mod-4:
            tupleToAdd = (image, int(contentTrainLabel[int(i/mod)])-1)
            trainPair.append(tupleToAdd)
            image = []

    with open('trainPair.json', 'w') as fp:
        json.dump(trainPair, fp)



    contentTest = None
    with open(fileName + "/testing_data.txt") as f:
        contentTest = f.readlines()
            
    contentTestLabel = None
    with open(fileName + "/testing_labels.txt") as f:
        contentTestLabel = f.readlines()

    testPair = []
    image = []
    for i in range(0,len(contentTest)):
        if i % mod == mod-3 or i % mod == mod-2 or i % mod == mod-1:
            continue

        image.append(contentTest[i][:-1]) 

        if i % mod == mod-4:
            tupleToAdd = (image, int(contentTestLabel[int(i/mod)])-1)
            testPair.append(tupleToAdd)
            image = []

    with open('testPair.json', 'w') as fp:
        json.dump(testPair, fp)




if __name__ == "__main__":
    convertToPickle("data")
    naiveBWrapper()
