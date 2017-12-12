import numpy as np
import pickle
import time
import json
import matplotlib.pyplot as plt


def getKNNOutput(x, trainX, trainY, k):

    dist = []
    for i in trainX:
        #dist.append((np.sum(((x-i)**2)))**0.5)
        dist.append(np.sum(abs(x-i)))

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

    confusionMat = np.zeros((10,10))

    for x,y in zip(testX,testY):
        total += 1
        classified = getKNNOutput(x, trainX, trainY, k)
        if int(classified) == int(y):
            correct += 1
        confusionMat[int(y)][int(classified)] += 1

    acc = float(correct)/total
    print("test accuracy:" + str(acc))

    return acc, confusionMat


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




def confusionMatrix(conf_arr):

    norm_conf = []
    for i in conf_arr:
        a = 0
        tmp_arr = []
        a = sum(i, 0)
        for j in i:
            tmp_arr.append(round(float(j)/float(a),2))
        norm_conf.append(tmp_arr)

    fig = plt.figure()
    plt.clf()
    ax = fig.add_subplot(111)
    ax.set_aspect(1)

    #print(norm_conf)

    res = ax.imshow(np.array(norm_conf), cmap=plt.cm.jet, 
                    interpolation='nearest')

    width, height = conf_arr.shape

    for x in range(width):
        for y in range(height):
            ax.annotate(str(norm_conf[x][y]), xy=(y, x), 
                        horizontalalignment='center',
                        verticalalignment='center')

    cb = fig.colorbar(res)
    alphabet = '0123456789'
    plt.xticks(range(width), alphabet[:width])
    plt.yticks(range(height), alphabet[:height])
    plt.savefig('confusion_matrix.png', format='png')


if __name__ == "__main__":
    
    convertToPickle("../digitdata")


    clust_data = np.zeros((10,2))

    bestAcc = -1
    bestCf = None
    bestK = -1
    for i in range(1,11):
        print(i)
        start_time = time.time()
        acc, cf = test(i)
        print("total time: " + str(time.time() - start_time) + " seconds")
        clust_data[i-1][0] = i
        clust_data[i-1][1] = acc

        if acc > bestAcc:
            bestAcc = acc
            bestCf = cf
            bestK = i

    plt.plot(clust_data[:,0], clust_data[:,1], 'ro')
    plt.axis([0.5, 10+0.5, 0, 1])
    plt.show()


    print(bestK)
    print(bestAcc)
    confusionMatrix(bestCf)


