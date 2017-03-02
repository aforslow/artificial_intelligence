import math
import numpy as np
#from src.reader_function import Reader

#Guessing y = beta0 + x1*beta1 + x2*beta2ls

def sigmoid(w, x):
	nom = 1
	dom = 1 + math.exp(-w[0]-w[1]*x[0] - w[2]*x[1])
	return nom/dom

#Only works for when we've the guess y = beta1 + beta2*x
def logRegression(x, y, w, alpha):
	h = sigmoid(w, x)
	newW0 = w[0] + alpha*(y - h)
	newW1 = w[1] + alpha*x[0]*(y - h)
	newW2 = w[2] + alpha*x[1]*(y - h)
	normVector = [w[0] - newW0, w[1] - newW1, w[2] - newW2]
	w[0] = newW0
	w[1] = newW1
	w[2] = newW2
	normValue = np.linalg.norm(normVector)
	return normValue
	# w[0] += alpha*(y - h)
	# w[1] = w[1] + alpha*x[0]*(y - h)
	# w[2] = w[2] + alpha*x[1]*(y - h)




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

x2Raw = [36961,43621,15694,36231,29945,40588,75255,37709,30899,25486,37497,40398,74105,76725,18317,35680,42514,15162,35298,29800,40255,74532,37464,31030,24843,36172,39552,72545,75352,18031]
x1Raw = [2503,2992,1042,2487,2014,2805,5062,2643,2126,1784,2641,2766,5047,5312,1215,2217,2761,990,2274,1865,2606,4805,2396,1993,1627,2375,2560,4597,4871,1119]

# x1RawE = [2217,2761,990,2274,1865,2606,4805,2396,1993,1627,2375,2560,4597,4871,1119]
# x2RawE = [35680,42514,15162,35298,29800,40255,74532,37464,31030,24843,36172,39552,72545,75352,18031]

x1 = [float(i)/max(x1Raw) for i in x1Raw]
x2 = [float(i)/max(x2Raw) for i in x2Raw]
y = []
for i in range(0, 15):
	y.append(0)

for i in range (15, 30):
	y.append(1)
# r = Reader()
# r.decode_file("./test/test1.txt")
# r.scale_data()
# y, x = r.get_randomized_data() 
print(str(len(x1)))
print(str(len(x2)))
x = []
for i in range(0, len(x1)):
	x.append([x1[i], x2[i]])

alpha = 0.2
epsilon = 0.03
w1 = []

w1.append(1)
w1.append(1)
w1.append(1)


# for i in range(0, len(x)):
# 	w1.append([])
# 	for j in range(0, len(x[i]) + 1):
# 		w1[i].append(1)
print(str(len(x)))
print(str(len(y)))

normValue = 1

# for i in range(0, 10000*6):
while epsilon < normValue:
	normValue = 0
	for j in range(0, len(y)):
		normValue += logRegression(x[j], y[j], w1, alpha)
	normValue /= len(y)
	# print(normValue)

#printing values
print("Wights")
print(str(w1))
print(str(predict(x, y, w1)) + " classified wrong")

