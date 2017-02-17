import math
import numpy as np

def sigmoid(w, x):
	nom = 1
	dom = 1 + math.exp(w[0]-w[1]*x)
	return nom/dom


def logRegression(x, y, w, alpha):
	h = sigmoid(w, x)
	w[1] = w[1] + alpha*x*(y - h)



def step(x, y, w, alpha):
	for i in range(0, len(w)):
		w[i] = w[i] + alpha*gradientDecent(x[i], y[i], w[i])
	return w

def predict(x, y, w):
	lost = 0
	for i in range(0, len(y)):
		if round(sigmoid(w[i], x[i])) != round(y[i]):
			lost += 1

	return lost

xRawF = [36961,43621,15694,36231,29945,40588,75255,37709,30899,25486,37497,40398,74105,76725,18317]
yRawF = [2503,2992,1042,2487,2014,2805,5062,2643,2126,1784,2641,2766,5047,5312,1215]

yRawE = [2217,2761,990,2274,1865,2606,4805,2396,1993,1627,2375,2560,4597,4871,1119]
xRawE = [35680,42514,15162,35298,29800,40255,74532,37464,31030,24843,36172,39552,72545,75352,18031]


x1 = [float(i)/max(xRawF) for i in xRawF]
y1 = [float(i)/max(yRawF) for i in yRawF]

x2 = [float(i)/max(xRawE) for i in xRawE]
y2 = [float(i)/max(yRawE) for i in yRawE]


alpha = 0.001
w1 = []
w2 = []

for i in range(0, len(x1)):
	w1.append([])
	w2.append([])
	for j in range(0, 2):
		w1[i].append(1)
		w2[i].append(1)

test = []
for i in range(0, len(x1)):
	test.append([1,1])


for i in range(0, 10000):
	for j in range(0, len(y1)):
		b = 2
		logRegression(x1[j], y1[j], w1[j], alpha)
		logRegression(x2[j], y2[j], w2[j], alpha)

print(str(predict(x1, y1, w1)) + "classified wrong - French")
print(str(predict(x2, y2, w2)) + "classified wrong - English")