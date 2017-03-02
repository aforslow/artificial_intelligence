import math
import numpy as np
from src.reader_function import Reader

#Guessing y = beta0 + x1*beta1 + x2*beta2ls

def sigmoid(w, x):
	nom = 1
	dom = 1 + math.exp(w[0]-w[1]*x[1] - w[2]*x[2])
	return nom/dom

#Only works for when we've the guess y = beta1 + beta2*x
def logRegression(x, y, w, alpha):
	h = sigmoid(w, x)
	w[0] += alpha*(y - h)
	w[1] = w[1] + alpha*x[1]*(y - h)
	w[2] = w[2] + alpha*x[1]*(y - h)



def step(x, y, w, alpha):
	for i in range(0, len(w)):
		w[i] = w[i] + alpha*gradientDecent(x[i], y[i], w[i])
	return w

def predict(x, y, w):
	lost = 0
	for i in range(0, len(y)):
		if round(sigmoid(w, x[i])) != round(y[i]):
			lost += 1

	return lost

# yRawF = [36961,43621,15694,36231,29945,40588,75255,37709,30899,25486,37497,40398,74105,76725,18317]
# xRawF = [2503,2992,1042,2487,2014,2805,5062,2643,2126,1784,2641,2766,5047,5312,1215]

# xRawE = [2217,2761,990,2274,1865,2606,4805,2396,1993,1627,2375,2560,4597,4871,1119]
# yRawE = [35680,42514,15162,35298,29800,40255,74532,37464,31030,24843,36172,39552,72545,75352,18031]

r = Reader()
r.decode_file("./test/test1.txt")
r.scale_data()
y, x = r.get_randomized_data() 

x1 = x
y1 = y

alpha = 0.001
w1 = []

w1.append(1)
w1.append(1)
w1.append(1)


# for i in range(0, len(x)):
# 	w1.append([])
# 	for j in range(0, len(x[i]) + 1):
# 		w1[i].append(1)

test = []
for i in range(0, len(x1)):
	test.append([1,1])


for i in range(0, 10000):
	for j in range(0, len(y1)):
		b = 2
		logRegression(x1[j], y1[j], w1, alpha)


#printing values
print("Wights")
print(str(w1))
print(str(predict(x1, y1, w1)) + " classified wrong")

