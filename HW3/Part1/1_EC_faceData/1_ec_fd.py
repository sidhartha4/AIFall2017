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

	#print(featureLabel)

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


def findClassLabelGeneric(m, n, disJoin,ternaryFlag):

	outfile = "pClass.npy"
	pClass = np.load(outfile)

	outfile = "featureLabel.npy"
	featureLabel = np.load(outfile)

	a = 0

	with open('testPair.json') as fh:
		a = json.load(fh)

	totalElements = 0
	correctItems = 0

	numClasses = 2
	rowNum = 70
	colNum = 60

	findClass = np.zeros(numClasses)

	for element in a:
		
		totalElements = totalElements + 1
		matVal = element[0]

		for iClass in range(0,numClasses):
			findClass[iClass] = math.log(pClass[iClass])

		if disJoin == 1:

			for i in range(0, int(rowNum/m)):
				for j in range(0, int(colNum/n)):
					
					totValK = 0

					xAndy = [(x,y) for x in range(0,m) for y in range(0,n)]
					
					if ternaryFlag == 1:

						for x in xAndy:
							if matVal[i*m+x[0]][j*n+x[1]] == " ":
								totValK = totValK*3
							elif matVal[i*m+x[0]][j*n+x[1]] == "+":
								totValK = totValK*3 + 1
							else:
								totValK = totValK*3 + 2


					else:

						for x in xAndy:
							if matVal[i*m+x[0]][j*n+x[1]] == " ":
								totValK = totValK*2
							else:
								totValK = totValK*2 + 1
										
					valToAdd = i * int(colNum/n) + j

					for kClass in range(0,numClasses):
						findClass[kClass] += math.log(featureLabel[kClass][valToAdd][totValK])

		else:

			for i in range(0, len(matVal)-m+1):
				for j in range(0, len(matVal[i])-n+1):
					
					totValK = 0

					xAndy = [(x,y) for x in range(0,m) for y in range(0,n)]
					
					if ternaryFlag == 1:

						for x in xAndy:
							if matVal[i+x[0]][j+x[1]] == " ":
								totValK = totValK*3
							elif matVal[i+x[0]][j+x[1]] == "+":
								totValK = totValK*3 + 1
							else:
								totValK = totValK*3 + 2

					else:

						for x in xAndy:
							if matVal[i+x[0]][j+x[1]] == " ":
								totValK = totValK*2
							else:
								totValK = totValK*2 + 1
										
					valToAdd = i * (len(matVal[i])-n+1) + j
					for kClass in range(0,numClasses):
						findClass[kClass] += math.log(featureLabel[kClass][valToAdd][totValK])


		
		classified = np.argmax(findClass)

		if classified == int(element[1]):
			correctItems += 1

	accu = float(correctItems)/totalElements
	print(correctItems)
	print(totalElements)
	print(accu)

	return accu, 0


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





def naiveBayesGeneric(a, m, n, disJoin, kVal, ternaryFlag):


	numClasses = 2

	pClass = np.zeros(numClasses)
	distinctVal = None

	if ternaryFlag == 1:
		distinctVal = int(math.pow(3,m*n))
	else:
		distinctVal = int(math.pow(2,m*n))

	rowNum = 70
	colNum = 60


	featureLabel = None
	if disJoin == 1:
		xLength = int(rowNum/m)
		yLength = int(colNum/n)
		featureLabel = np.zeros((numClasses, xLength*yLength, distinctVal))

	else:
		xLength = rowNum-m+1
		yLength = colNum-n+1
		featureLabel = np.zeros((numClasses, xLength*yLength, distinctVal))

	totalElements = 0
	#print(featureLabel.shape)
	for element in a:

		pClass[element[1]] += 1
		totalElements = totalElements + 1
		matVal = element[0]

		if disJoin == 1:

			for i in range(0, int(rowNum/m)):
				for j in range(0, int(colNum/n)):
					
					totValK = 0

					xAndy = [(x,y) for x in range(0,m) for y in range(0,n)]
					
					if ternaryFlag == 1:

						for x in xAndy:
							if matVal[i*m+x[0]][j*n+x[1]] == " ":
								totValK = totValK*3
							elif matVal[i*m+x[0]][j*n+x[1]] == "+":
								totValK = totValK*3 + 1
							else:
								totValK = totValK*3 + 2


					else:

						for x in xAndy:
							if matVal[i*m+x[0]][j*n+x[1]] == " ":
								totValK = totValK*2
							else:
								totValK = totValK*2 + 1
					
					valToAdd = i * int(colNum/n) + j
					featureLabel[element[1]][valToAdd][totValK] += 1

		else:

			for i in range(0, len(matVal)-m+1):
				for j in range(0, len(matVal[i])-n+1):
					
					totValK = 0

					xAndy = [(x,y) for x in range(0,m) for y in range(0,n)]
					
					if ternaryFlag == 1:

						for x in xAndy:
							if matVal[i+x[0]][j+x[1]] == " ":
								totValK = totValK*3
							elif matVal[i+x[0]][j+x[1]] == "+":
								totValK = totValK*3 + 1
							else:
								totValK = totValK*3 + 2

					else:

						for x in xAndy:
							if matVal[i+x[0]][j+x[1]] == " ":
								totValK = totValK*2
							else:
								totValK = totValK*2 + 1
										
					valToAdd = i * (len(matVal[i])-n+1) + j
					featureLabel[element[1]][valToAdd][totValK] += 1

				
	for iterV in range(0,numClasses):
		featureLabel[iterV] = (featureLabel[iterV]+kVal) /(pClass[iterV]+ distinctVal *kVal)


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
#	naiveBayes(a)
#	findClassLabel()

	AccuracyValues = []

	kValues = np.logspace(-1,1,26)

	maxAccuracyVal = -1
	finalConfusionMat = None

	naiveBayesGeneric(a, 1, 1, 0, 0.1, 0)
	accuracyValue, confusionMat =  findClassLabelGeneric(1, 1, 0, 0)

	
	"""
	for kVal in kValues:
		#print(kVal)
		naiveBayesGeneric(a, 4, 4, 1, kVal)
		accuracyValue, confusionMat =  findClassLabelGeneric(4, 4, 1)
		AccuracyValues.append(accuracyValue)
		if maxAccuracyVal < accuracyValue:
			maxAccuracyVal = accuracyValue
			finalConfusionMat = confusionMat
			

	print(maxAccuracyVal)
	print(AccuracyValues)
	"""

def convertToPickle(fileName):

	contentTrain = None
	with open(fileName + "/facedatatrain") as f:
		contentTrain = f.readlines()
		
	contentTrainLabel = None
	with open(fileName + "/facedatatrainlabels") as f:
		contentTrainLabel = f.readlines()

	trainPair = []
	image = []
	for i in range(0,len(contentTrain)):

		imageLine = []
		for j in range(0,len(contentTrain[i])-1):
			imageLine.append(contentTrain[i][j])

		image.append(imageLine) 

		if i%70 == 69:
			tupleToAdd = (image, int(contentTrainLabel[int(i/70)]))
			trainPair.append(tupleToAdd)
			#print(contentTrainLabel[int(i/28)])
			image = []

	with open('trainPair.json', 'w') as fp:
		json.dump(trainPair, fp)


	contentTest = None
	with open(fileName + "/facedatatest") as f:
		contentTest = f.readlines()
		
	contentTestLabel = None
	with open(fileName + "/facedatatestlabels") as f:
		contentTestLabel = f.readlines()

	testPair = []
	image = []
	for i in range(0,len(contentTest)):

		imageLine = []
		for j in range(0,len(contentTest[i])-1):
			imageLine.append(contentTest[i][j])

		image.append(imageLine) 

		if i%70 == 69:
			tupleToAdd = (image, int(contentTestLabel[int(i/70)]))
			testPair.append(tupleToAdd)
			#print(contentTestLabel[int(i/28)])
			image = []

	with open('testPair.json', 'w') as fp:
		json.dump(testPair, fp)




if __name__ == "__main__":
	convertToPickle("../facedata")
	naiveBWrapper()