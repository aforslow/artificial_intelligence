#!/usr/bin/env python
from reader_function import Reader
import math
import numpy as np

class Perceptron():

	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.w = [0] * 3 #We assume 2 features (as in training set)
		self.training_size = len(self.y)
		print x

	def train(self, size=0):
		if size > 0:
			self.training_size = size
		print "Training..."
		print ""

		#Stop when the number of misclassified examples = 0
		#for the training set
		n_misses = self.training_size
		miss_rate = 1
		miss_rate2 = miss_rate
		idx2 = 0
		while (n_misses > 0): #Stop condition
			idx = 0
			idx2 += 1
			n_misses = 0.0
			for dictionary in self.x[:self.training_size]:
				n_misses += self.simple_update(dictionary, self.y[idx])
				idx += 1
			miss_rate = n_misses / self.training_size
			if (miss_rate < (miss_rate2 - 0.01)):
				miss_rate2 = miss_rate
				print "Imroved miss rate: ", miss_rate

		print "Miss rate:", miss_rate
		print "Number of misses last training:", n_misses
		print "Training set size:", self.training_size
		print ""

	def get_params(self):
		return self.w

	def classify(self, x):
		classification_val = self.w[0] + self.w[1]*x[1] + self.w[2]*x[2]
		guessed_y = 0
		if classification_val > 0:
			guessed_y = 1
		return guessed_y

	def simple_update(self, x, y):
		guessed_y = self.classify(x)
		self.w[0] = self.w[0] + (y - guessed_y)
		self.w[1] = self.w[1] + x[1]*(y - guessed_y)
		self.w[2] = self.w[2] + x[2]*(y - guessed_y)

		if (y-guessed_y) == 0:
			return 0
		return 1

	def simple_test(self):
		self.test(self.y, self.x)

	
	def testset_test(self):
		print "\nTest set results:"
		print "-----------------------"
		self.test(y[self.training_size:], x[self.training_size:])

	def test(self, y, dicts):
		idx = 0
		classification_list = []
		for dictionary in dicts:
			classification_list.append(self.classify(dictionary))
		
		print "Classifications: "
		print classification_list
		print "Actual classes: "
		print y
		print "Accuracy: ", 
		n_misses = 0.0
		for i in range(len(y)):
			if abs(classification_list[i] - y[i]) != 0.0:
				n_misses += 1.0
		print 1.0 - (n_misses / len(y))


	#Logistic definitions
	def sigmoid(self, w, x):
		nom = 1
		dom = 1 + math.exp(-w[0]-w[1]*x[1] - w[2]*x[2])
		return nom/dom

	def logRegression(self, x, y, w, alpha):
		h = self.sigmoid(w, x)
		newW0 = w[0] + alpha*(y - h)
		newW1 = w[1] + alpha*x[1]*(y - h)
		newW2 = w[2] + alpha*x[2]*(y - h)
		normVector = [w[0] - newW0, w[1] - newW1, w[2] - newW2]
		w[0] = newW0
		w[1] = newW1
		w[2] = newW2
		normValue = np.linalg.norm(normVector)
		return normValue

	def predict(self, x, y, w):
		lost = 0
		for i in range(0, len(y)):
			if round(self.sigmoid(w, x[i])) != round(y[i]):
				lost += 1
		return lost

if __name__ == "__main__":
	#perception

	r = Reader()
	r.decode_file("../test/test1.txt")
	r.scale_data()
	y, x = r.get_randomized_data()
	p = Perceptron(x, y)
	p.train(25)
	print "Parameters (w0, w1, w2):", p.get_params()
	p.testset_test()

	#logistic regression
	x1 = x
	y1 = y
	w1 = []

	w1.append(1)
	w1.append(2)
	w1.append(1)

	epsilon = 0.03
	alpha = 0.1

	normValue = 1;
	while normValue > epsilon:
		normValue = 0
		for j in range(0, len(y1)):
			normValue += p.logRegression(x1[j], y1[j], w1, alpha)
		normValue /= len(y1)


	#printing values
	print("Wights")
	print(str(w1))
	print(str(p.predict(x1, y1, w1)) + " classified wrong")



