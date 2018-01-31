import csv
from random import shuffle
from math import inf
import time
CSV_PATH="./data.csv"
train_num=469
test_num=100

def getDataFromcsv(randomize=False):
	data=[]
	with open(CSV_PATH,newline='') as csvfile:
		reader=csv.DictReader(csvfile,delimiter=',')
		for row in reader:
			for i in row.keys():
				if(i!='id' and i!='diagnosis'):
					row[i]=float(row[i])
			data.append(row)
	#normalize by min-max
	for column_name in data[0]:
		if(column_name!='id' and column_name!='diagnosis'):
			column_min=min([x[column_name] for x in data])
			column_max=max([x[column_name] for x in data])
			for row in data:
				row[column_name]=(row[column_name]-column_min)/(column_max-column_min)
	#radomize if needed
	if(randomize):
		shuffle(data)
	#divide the data
	return data[:train_num],data[train_num:]

def getSqDistance(a,b):
	res=0
	for column_name in a.keys():
		if(column_name!='id' and column_name!='diagnosis'):
			res+=(a[column_name]-b[column_name])**2
	return res
def getDiagosisFromKNN(trainData,test,k=3):
	'''
	data is the role to be test
	return: diagnosise (B,M)
	'''
	knn=[(0,inf)]*k #(rowNumber,distance) sorted ascendingly
	for data in train_data:
		(dia,sqDis)=(data['diagnosis'],getSqDistance(data,test))
		if(sqDis<knn[k-1][1]):
			knn[k-1]=(dia,sqDis)
			knn.sort(key=lambda x:x[1])
	return getVoteFromKnn(knn)
def getVoteFromKnn(knn):
	#transform
	return "B" if [x[0] for x in knn].count("B")>=len(knn)/2 else "M"
if __name__ == '__main__':
	start_time=time.time()
	correct=0
	(train_data,test_data)=getDataFromcsv(randomize=False)
	for test in test_data:
		if(getDiagosisFromKNN(train_data,test,k=5)==test['diagnosis']):#correct
			correct+=1
	print("accuracy: {}".format(correct/test_num))
	print("elapsed time: {}".format(time.time()-start_time))

