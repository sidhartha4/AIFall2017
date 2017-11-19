import pandas as pd
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
	#convertToPickle("digitdata")
	naiveBWrapper()