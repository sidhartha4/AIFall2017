import numpy as np
import pickle
import time
import json

no_epochs = 100
mini_batch_size = 1
learning_rate = 0.02


def initializeLayer(input_size, output_size):

    W = np.random.uniform(-0.0714, 0.0714, size=(output_size, input_size))
    b = np.zeros(output_size)

    return W, b


def getLabelFromOutput(output):
    
    max_label = 0
    max_val = output[0]
    for i in range(1,10):
        if output[i]>max_val:
            max_val = output[i]
            max_label = i

    return max_label


def getMLPOutput(x, W, b):

    layer1_op = np.dot(x, W.T) + b
    output = getLabelFromOutput(layer1_op)

    return output


def getOutputVector(y):
    output = []
    
    for i in range(10):
        if i == y:
            output.append(1)
        else:
            output.append(0)
    output = np.array(output)

    return output

def getGradient(x, y, l1s):

    sigmoid_grad = np.ones(1)
    del_b = sigmoid_grad
    del_W = np.outer(sigmoid_grad, x)

    return del_W, del_b

def dump_model(W, b):

    np.save('weights/W.npy', W)
    np.save('weights/b.npy', b)
    
def obtainTrainedModel():

    W = np.load('weights/W.npy')
    b = np.load('weights/b.npy')
    return W, b




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

def train():
    
    trainX, trainY = prepareInput("trainPair.json")

    W, b = initializeLayer(784,10)

    for epoch in range(no_epochs):
        batches = int(float(trainX.shape[0])/float(mini_batch_size))
        
        for batch in range(batches):
            print("Epoch: ", (epoch+1),"/",no_epochs)
            print("Batch: ", (batch+1),"/",batches)

            training_samplesX = trainX[batch*mini_batch_size:(batch+1)*mini_batch_size]
            training_samplesY = trainY[batch*mini_batch_size:(batch+1)*mini_batch_size]

            for sample in range(mini_batch_size):

                l1 = getMLPOutput(training_samplesX[sample], W, b)
                del_W, del_b = getGradient(training_samplesX[sample], training_samplesY[sample], l1)
                W[int(l1)] = W[int(l1)]+(-learning_rate)*del_W
                b[int(l1)] = b[int(l1)] +(-learning_rate)*del_b

                W[int(training_samplesY[sample])] = W[int(training_samplesY[sample])]+(learning_rate)*del_W
                b[int(training_samplesY[sample])] = b[int(training_samplesY[sample])] +(learning_rate)*del_b


    dump_model(W,b)



def test():

    testX, testY = prepareInput("testPair.json")
    W,b = obtainTrainedModel()

    print(testX.shape)
    print(testY.shape)
    total = 0
    correct = 0
    

    for x,y in zip(testX,testY):
        total += 1
        classified = getMLPOutput(x, W, b)
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
    
    convertToPickle("../digitdata")
    train()
    test()