import numpy as np
import pickle
import time
import json


def getKNNOutput(x, trainX, trainY, k):

    dist = []
    for i in trainX:
        dist.append((np.sum(((x-i)**2)))**0.5)

    dist = np.array(dist)
    idx = dist.argsort()[:k]
    val = np.zeros(10)

    for i in idx:
        val[trainY[i]] += 1

    maxVal = -1
    maxInd = -1
    j = 0
    for i in val:
        if i > maxVal:
            maxVal = i
            maxInd = j

        j = j+1

    return maxInd

def prepareInput(name):

    a = 0
    with open(name) as fh:
        a = json.load(fh)

    tX = []
    tY = []
    
    for element in a:
        matVal = element[0]

        X = []
        for i in range(0, len(matVal)):
            for j in range(0, len(matVal[i])):
                if matVal[i][j] == " ":
                    X.append(0)
                else:
                    X.append(1)

        tX.append(X)
        tY.append(int(element[1])) 

    tX = np.array(tX)
    tY = np.array(tY)

    return tX, tY 



def test(k):

    testX, testY = prepareInput("testPair.json")
    trainX, trainY = prepareInput("trainPair.json")

    print(trainX.shape)
    print(trainY.shape)
    
    total = 0
    correct = 0

    for x,y in zip(testX,testY):
        total += 1
        classified = getKNNOutput(x, trainX, trainY, k)
        if int(classified) == int(y):
            correct += 1

    print("test accuracy:" + str(float(correct)/total))




def convertToPickle(fileName):

    contentTrain = None
    with open(fileName + "/trainingimages") as f:
        contentTrain = f.readlines()
        
    contentTrainLabel = None
    with open(fileName + "/traininglabels") as f:
        contentTrainLabel = f.readlines()

    trainPair = []
    image = []
    for i in range(0,len(contentTrain)):

        imageLine = []
        for j in range(0,len(contentTrain[i])-1):
            imageLine.append(contentTrain[i][j])

        image.append(imageLine) 

        if i%28 == 27:
            tupleToAdd = (image, int(contentTrainLabel[int(i/28)]))
            trainPair.append(tupleToAdd)
            #print(contentTrainLabel[int(i/28)])
            image = []

    with open('trainPair.json', 'w') as fp:
        json.dump(trainPair, fp)


    contentTest = None
    with open(fileName + "/testimages") as f:
        contentTest = f.readlines()
        
    contentTestLabel = None
    with open(fileName + "/testlabels") as f:
        contentTestLabel = f.readlines()

    testPair = []
    image = []
    for i in range(0,len(contentTest)):

        imageLine = []
        for j in range(0,len(contentTest[i])-1):
            imageLine.append(contentTest[i][j])

        image.append(imageLine) 

        if i%28 == 27:
            tupleToAdd = (image, int(contentTestLabel[int(i/28)]))
            testPair.append(tupleToAdd)
            #print(contentTestLabel[int(i/28)])
            image = []

    with open('testPair.json', 'w') as fp:
        json.dump(testPair, fp)




if __name__ == "__main__":
    k = 3
    convertToPickle("../digitdata")
    test(k)