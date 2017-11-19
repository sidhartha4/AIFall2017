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

	print(featureLabel)

	for element in a:
		
		totalElements = totalElements + 1
		matVal = element[0]

		for iClass in range(0,10):
			findClass[iClass] = math.log(pClass[iClass])
		
		for i in range(0, len(matVal)-1):
			for j in range(0, len(matVal[i])-1):
				valToAdd = i* 27 + j

				totValK = 0

				if matVal[i][j] == " ":
					totValK = totValK*2
				else:
					totValK = totValK*2 + 1
				if matVal[i][j+1] == " ":
					totValK = totValK*2
				else:
					totValK = totValK*2 + 1
				
				if matVal[i+1][j] == " ":
					totValK = totValK*2
				else:
					totValK = totValK*2 + 1
				if matVal[i+1][j+1] == " ":
					totValK = totValK*2
				else:
					totValK = totValK*2 + 1

				for kClass in range(0,10):
					findClass[kClass] += math.log(featureLabel[kClass][valToAdd][totValK])

		
		classified = np.argmax(findClass)

		if classified == int(element[1]):
			correctItems += 1

	print(float(correctItems)/totalElements)

def naiveBayes(a):
	pClass = np.zeros(10)

	distinctVal = 16

	featureLabel = np.zeros((10, 729, distinctVal))

	totalElements = 0
	for element in a:
		pClass[element[1]]  = pClass[element[1]]  + 1
		totalElements = totalElements + 1
		matVal = element[0]
		for i in range(0, len(matVal)-1):
			for j in range(0, len(matVal[i])-1):
				valToAdd = i * 27 + j
				totValK = 0

				if matVal[i][j] == " ":
					totValK = totValK*2
				else:
					totValK = totValK*2 + 1
				if matVal[i][j+1] == " ":
					totValK = totValK*2
				else:
					totValK = totValK*2 + 1
				
				if matVal[i+1][j] == " ":
					totValK = totValK*2
				else:
					totValK = totValK*2 + 1
				if matVal[i+1][j+1] == " ":
					totValK = totValK*2
				else:
					totValK = totValK*2 + 1

				featureLabel[element[1]][valToAdd][totValK] += 1
				
	kVal = 0.1

	for iterV in range(0,10):
		#print(featureLabel[iterV])
		featureLabel[iterV] = (featureLabel[iterV]+kVal) /(pClass[iterV]+ distinctVal *kVal)


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
	convertToPickle("../digitdata")
	naiveBWrapper()