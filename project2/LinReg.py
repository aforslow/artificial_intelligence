
import random
import matplotlib.pyplot as plt
import numpy as np

def error(k, m, x, y):
	sumError = 0
	for i in range(0, len(y)):
		sumError += (y[i] - (k*x[i] + m))**2
	return sumError/len(y)
#k as in the k in y = kx + m
def partialDerivateKBatch(k, m, x, y):
	gradient = 0
	for i in range(0, len(y)):
		gradient += -x[i]*(y[i] - (k*x[i] + m))
	return gradient/len(y)

#m as in the m in y = kx + m
def partialDerivateMBatch(k, m, x, y):
	gradient = 0
	for i in range(0, len(y)):
		gradient += -(y[i] - (k*x[i] + m))
	return gradient/len(y)

def partialDerivateKStoch(k, m, x, y):
	gradient = -x*(y - (k*x + m))
	return gradient

#m as in the m in y = kx + m
def partialDerivateMStoch(k, m, x, y):
	gradient = -(y - (k*x + m))
	return gradient





#k and m in y = kx + m and alpha as the learning rate
def step(k, m, x, y, alpha):
	newK = 0
	newM = 0
	partDerivateM = partialDerivateMBatch(k, m, x, y)
	partDerivateK = partialDerivateKBatch(k, m, x, y)
	newK = k - (alpha*partDerivateK)
	newM = m - (alpha*partDerivateM)
	return [newK, newM]
	
def step2(k, m, x, y, alpha):
	newK = 0
	newM = 0
	partDerivateM = partialDerivateMStoch(k, m, x, y)
	partDerivateK = partialDerivateKStoch(k, m, x, y)
	newK = k - (alpha*partDerivateK)
	newM = m - (alpha*partDerivateM)
	return [newK, newM]
def createRandomValues(minX, maxX, minY, maxY, nbrOfValues):
	x = []
	y = []
	for i in range(0, nbrOfValues):
		x.append(random.uniform(minX, maxX))
		y.append(random.uniform(minY, maxY))
	return [x, y]
	

minX = 5
maxX = 20
minY = 5
maxY = 20
nbrOfValues = 200
iterations = 5*2000

m = -1
k = 0
alpha = 0.05*5

#vec = createRandomValues(minX, maxX, minY, maxY, nbrOfValues)
# x = vec[0]
# y = vec[1]
yRaw = [36961,43621,15694,36231,29945,40588,75255,37709,30899,25486,37497,40398,74105,76725,18317]
xRaw = [2503,2992,1042,2487,2014,2805,5062,2643,2126,1784,2641,2766,5047,5312,1215]

x = [float(i)/sum(xRaw) for i in xRaw]
y = [float(i)/sum(yRaw) for i in yRaw]
print(str(len(x)) + " " + str(len(y)))
plt.plot(x, y, 'ro')
for i in range(0, iterations):
	temp = step(k, m, x, y, alpha)
	k = temp[0]
	m = temp[1]
	#print(str(k))


plt.plot([min(x), max(x)], [k*min(x) + m, k*max(x) + m])
print(str(k) + " " + str(m))
#plt.show()
#Now to test it with a regular least square method



xx = np.asarray(x)
yy = np.asarray(y)
vec = np.polyfit(xx, yy, 1)
plt.plot([min(x), max(x)], [vec[0]*min(x) + vec[1], vec[0]*max(x) + vec[1]], 'r--')

m = -1
k = 0
alpha = 0.005*5
for i in range(0, 2000*5):
	for i in range(0, len(x)):
		temp = step2(k, m, x[i], y[i], alpha)
		k = temp[0]
		m = temp[1]
plt.plot([min(x), max(x)], [k*min(x) + m, k*max(x) + m], 'b--')
print(str(k) + " " + str(m))
plt.show()
