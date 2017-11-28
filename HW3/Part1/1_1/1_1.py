import pandas as pd
import pickle
import json
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.colors as clr
import matplotlib as mpl


def oddRatioMap(finalConfusionMat):
	outfile = "featureLabel.npy"
	featureLabel = np.load(outfile)

	confusionMatFlat = finalConfusionMat.flatten()

	a = confusionMatFlat.argsort()[-14:][::-1] 
	print(a)

	"""
	"""
	
	for valA in range(10,14):

		xA = a[valA] 

		firstDigit = int(xA/10)
		secondDigit = xA%10
		print(xA)
		print(firstDigit)
		print(secondDigit) 

		x = 0
		x1ListB = []
		y1ListB = []
		x1ListG = []
		y1ListG = []
		x1ListR = []
		y1ListR = []
		x1ListY = []
		y1ListY = []


		some_matrix = np.zeros((28,28))

		my_color = ""
		for i in featureLabel[firstDigit]:

			some_matrix[int(x/28)][x%28] = i[1]
			x = x+1


		cmap = clr.LinearSegmentedColormap.from_list('yo', ['red','yellow','blue'], N=256)

		#print(some_matrix)
		plt.matshow(some_matrix, cmap=cmap)

		plt.show()

		x = 0
		x1ListB = []
		y1ListB = []
		x1ListG = []
		y1ListG = []
		x1ListR = []
		y1ListR = []
		x1ListY = []
		y1ListY = []


		my_color = ""
		for i in featureLabel[secondDigit]:
			some_matrix[int(x/28)][x%28] = i[1]
			x = x+1


		cmap = clr.LinearSegmentedColormap.from_list('yo', ['red','yellow','blue'], N=256)

		#print(some_matrix)
		plt.matshow(some_matrix, cmap=cmap)

		plt.show()


		x1ListB = []
		y1ListB = []
		x1ListG = []
		y1ListG = []
		x1ListR = []
		y1ListR = []
		x1ListY = []
		y1ListY = []


		maxV = -4
		minV = 1500
		for i in range(0,784):

			y1 = 27 - int(i/28)
			x1 = i%28
			v = math.log(featureLabel[firstDigit][i][1]/featureLabel[secondDigit][i][1])
			#print(v)

			maxV = max(maxV,v)
			minV = min(minV,v)

		#print(minV)
		#print(maxV)
		some_matrix = np.zeros((28,28))

		for i in range(0,784):

			x1 = int(i/28)
			y1 = i%28

			v1 = math.log(featureLabel[firstDigit][i][1]/featureLabel[secondDigit][i][1])
			v = float(v1-minV) / (maxV-minV)

			some_matrix[x1][y1] = v

			y11 = 27-int(i/28)
			x11 = i%28
			if v1 <= -0.2:
				x1ListB.append(x11)
				y1ListB.append(y11)
			elif v1 > -0.2 and v1 <= 0.2:
				x1ListY.append(x11)
				y1ListY.append(y11)		
			elif v1 > 0.2:
				x1ListR.append(x11)
				y1ListR.append(y11)		
			
		

		#cmap = mpl.cm.bwr

		cmap = clr.LinearSegmentedColormap.from_list('yo', ['red','yellow','blue'], N=256)

		#cmap = clr.LinearSegmentedColormap.from_list()

		#print(some_matrix)
		plt.matshow(some_matrix, cmap=cmap)

		#plt.plot(some_matrix, cmap=cmap)

		plt.show()

		"""
		plt.plot(x1ListB,y1ListB, 'ro', color='b')
		plt.plot(x1ListG,y1ListG, 'ro', color='g')
		plt.plot(x1ListR,y1ListR, 'ro', color='r')
		plt.plot(x1ListY,y1ListY, 'ro', color='y')
		plt.show()
		"""

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

	confusionMat = np.zeros((10,10))
	#print(confusionMat[0][0])

	testExamplesWithProbabilites = []
	for i in range(0,10):
		tupleToAdd = (0,0,0,1,1,1,0,1)
		testExamplesWithProbabilites.append(tupleToAdd)

	testClassValues = np.zeros(10)


	testNumber = 0
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

		if testExamplesWithProbabilites[int(element[1])][0] < math.exp(findClass[int(element[1])]):
			tupleToAdd = (math.exp(findClass[int(element[1])]),classified,matVal, testExamplesWithProbabilites[int(element[1])][3],\
				testExamplesWithProbabilites[int(element[1])][4],testExamplesWithProbabilites[int(element[1])][5],\
				testNumber, testExamplesWithProbabilites[int(element[1])][7])

			testExamplesWithProbabilites[int(element[1])] = tupleToAdd
			
		elif testExamplesWithProbabilites[int(element[1])][3] > math.exp(findClass[int(element[1])]):
			tupleToAdd = (testExamplesWithProbabilites[int(element[1])][0],testExamplesWithProbabilites[int(element[1])][1]\
				,testExamplesWithProbabilites[int(element[1])][2],math.exp(findClass[int(element[1])]),classified,matVal,\
				 testExamplesWithProbabilites[int(element[1])][6],testNumber)
			
			testExamplesWithProbabilites[int(element[1])] = tupleToAdd
			

		if classified == int(element[1]):
			correctItems += 1

		testClassValues[int(element[1])] += 1
		confusionMat[int(element[1])][classified] += 1

		testNumber  = testNumber  + 1


	for j in range(0,testClassValues.shape[0]):
		confusionMat[j] = confusionMat[j]*100/testClassValues[j] 


	print(float(correctItems)/totalElements)

	accuracyValue = float(correctItems)/totalElements

	return accuracyValue,confusionMat, testExamplesWithProbabilites

def naiveBayes(a, kVal):
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


	for iterV in range(0,10):
		#print(featureLabel[iterV])
		featureLabel[iterV] = (featureLabel[iterV]+kVal) /(pClass[iterV]+2*kVal)


		#print(featureLabel[iterV])

	pClass = pClass/totalElements

	outfile = "pClass.npy"
	np.save(outfile, pClass)

	outfile = "featureLabel.npy"
	np.save(outfile, featureLabel)

	print(kVal)





def naiveBWrapper():
	a = 0

	with open('trainPair.json') as fh:
		a = json.load(fh)

	finalConfusionMat = None
	finaltestExamplesWithProbabilites = None


	print(len(a))
	AccuracyValues = []
	
	kValues = np.logspace(-1,1,21)

	maxAccuracyVal = -1

	kVal = 10 ** -0.9
	"""
	for kVal in kValues:
		naiveBayes(a,kVal)
		accuracyValue, confusionMat, testExamplesWithProbabilites = findClassLabel()
		AccuracyValues.append(accuracyValue)
		if maxAccuracyVal < accuracyValue:
			maxAccuracyVal = accuracyValue
			finalConfusionMat = confusionMat
			finaltestExamplesWithProbabilites = testExamplesWithProbabilites
	"""

	naiveBayes(a,kVal)
	accuracyValue, confusionMat, testExamplesWithProbabilites = findClassLabel()
	AccuracyValues.append(accuracyValue)
	if maxAccuracyVal < accuracyValue:
		maxAccuracyVal = accuracyValue
		finalConfusionMat = confusionMat
		finaltestExamplesWithProbabilites = testExamplesWithProbabilites

	print(maxAccuracyVal)	
	#print(finalConfusionMat)
	for ka in finalConfusionMat:
		for ja in ka:
			print(round(ja,2),end='\t')
		print()


	"""
	for i in finaltestExamplesWithProbabilites:
		print("--------------------------------------max---------------------------------------")
		print(i[0])
		print(i[1])
		print(i[6])

		for j in i[2]:
			stringPrint = ""
			for kappa in j:
				stringPrint = stringPrint + kappa
			print(stringPrint)

		print("--------------------------------------min---------------------------------------")
		print(i[3])
		print(i[4])
		print(i[7])

		for j in i[5]:
			stringPrint = ""
			for kappa in j:
				stringPrint = stringPrint + kappa
			print(stringPrint)
	"""	
	oddRatioMap(finalConfusionMat)

	outfile = "finalConfusionMat.npy"
	np.save(outfile, finalConfusionMat)

					
	#plt.semilogx(kValues, AccuracyValues, 'ro')
	#plt.show()
	#plt.xlabel('K')
	#plt.ylabel('Accuracy')

	#plt.savefig('accuracyValues.png')




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
	#print("this is fun")
	
	convertToPickle("../digitdata")
	naiveBWrapper()