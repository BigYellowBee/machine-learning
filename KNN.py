#coding:utf8
from numpy import *
import operator
import matplotlib
import matplotlib.pyplot as plt


#生成一个简单的数据
def createDataSet():
	group=array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
	labels=['A','A','B','B']
	return group,labels

#分类算法
def classify0(inX,dataSet,labels,k):
	dataSetSize=dataSet.shape[0]
	diffMat=tile(inX,(dataSetSize,1))-dataSet #构建想减的矩阵
	sqDiffMat=diffMat**2
	sqDistances=sqDiffMat.sum(axis=1)
	distances=sqDistances**0.5
	print distances
	sortedDistIndicies=distances.argsort()  #排序返回的是原list中的顺序　sortedDistIndicies的值为[2,3,1,0]
	classCount={}
	for i in range(k):
		print sortedDistIndicies[i]
		voteIlabel=labels[sortedDistIndicies[i]]
		classCount[voteIlabel]=classCount.get(voteIlabel,0)+1  #字典的get 方法，，如果值在里面，就返回值，没有就返回０
	sortedClassCount=sorted(classCount.iteritems(),key=operator.itemgetter(1),reverse=True)
	return sortedClassCount[0][0]

#从分本中解析数据
def file2matrix(filename):
	fr=open(filename)
	arrayOLines=fr.readlines()
	numberOfLines=len(arrayOLines)
	returnMat=zeros((numberOfLines,3))  #创建返回矩阵，初始都为０ 　　注意是两个括号
	classLabelVector=[]
	index=0
	for line in arrayOLines:
		line=line.strip()
		listFromLine=line.split('\t')
		returnMat[index,:]=listFromLine[0:3]
		classLabelVector.append(int(listFromLine[-1])) #把最后一列数值加入到label
		index+=1
	return returnMat,classLabelVector

#增加归一化
def autoNorm(dataSet):
	minVals=dataSet.min(0)
	maxVals=dataSet.max(0)
	ranges=maxVals-minVals
	normDataSet=zeros(shape(dataSet))
	m=dataSet.shape[0]
	normDataSet=dataSet-tile(minVals,(m,1))
	normDataSet=normDataSet/tile(ranges,(m,1))  #特征值相除，，矩阵相除用的是linalg.solve(A,B)
	return normDataSet,ranges,minVals

#测试分类器的正确率
'''
直接选出了，数据的前１０％的数据作为测试集，剩下的数据作为训练集
'''
def datingClassTest():
	hoRatio=0.10
	datingDataMat,datingLabels=file2matrix('datingTestSet2.txt')
	normMat,ranges,minVals=autoNorm(datingDataMat)
	m=normMat.shape[0]
	numTestVecs=int(m*hoRatio)#测试集的大小
	errorCount=0.0
	for i in range(numTestVecs):
		classifierResult=classify0(normMat[i,:],normMat(numTestVecs:m,:),datingLabels[numTestVecs:m],3)
		print "the classifier came back with :%d,the real answer is %d" %(classifierResult,datingLabels[i])
		if(classifierResult != datingLabels[i]):
			errorCount+=1.0
	print "the total error rate is :%f" %(errorCount/float(numTestVecs))



def main():
	'''
	datingDataMat,datingLabels=file2matrix('datingTestSet2.txt')
	
	fig=plt.figure()
	ax=fig.add_subplot(111)
	ax.scatter(datingDataMat[:,1],datingDataMat[:,2],15.0*array(datingLabels),15.0*array(datingLabels),depthshade=True)  #第三个参数是大小，第四个参数是颜色
	plt.show()
	
	normMat,ranges,minVals=autoNorm(datingDataMat)
	print normMat
	'''
	datingClassTest()
main()