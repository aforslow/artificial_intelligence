
import random
import matplotlib.pyplot as plt
import numpy as np

def error(k, m, x, y):
	sumError = 0
	for i in range(0, len(y)):
		sumError += (y[i] - (k*x[i] + m))**2
	return sumError/len(y)


#k as in the k in y = kx + m, batch version
def partialDerivateKBatch(k, m, x, y):
	gradient = 0
	for i in range(0, len(y)):
		gradient += -x[i]*(y[i] - (k*x[i] + m))
	return 2*gradient/len(y)

#m as in the m in y = kx + m, batch version
def partialDerivateMBatch(k, m, x, y):
	gradient = 0
	for i in range(0, len(y)):
		gradient += -(y[i] - (k*x[i] + m))
	return 2*gradient/len(y)
#m as in the m in y = kx + m, stoch version
def partialDerivateKStoch(k, m, x, y):
	gradient = -x*(y - (k*x + m))
	return 2*gradient

#m as in the m in y = kx + m, stoch version
def partialDerivateMStoch(k, m, x, y):
	gradient = -(y - (k*x + m))
	return 2*gradient



#k and m in y = kx + m and alpha as the learning rate
#Linear regression batch version
def linRegBatch(k, m, x, y, alpha, epsi):
	dError = 1
	while dError > epsi:
		partDerivateM = partialDerivateMBatch(k, m, x, y)
		partDerivateK = partialDerivateKBatch(k, m, x, y)
		k = k - (alpha*partDerivateK)
		m = m - (alpha*partDerivateM)
		dError = abs(partDerivateM) + abs(partDerivateK)
	return [k, m]

#k and m in y = kx + m and alpha as the learning rate
#Linear regression stochaistic version
def linRegStoch(k, m, x, y, alpha, epoch):
	j = 0
	while j < epoch:
		temp = 0
		for i in range(0, len(x)):
			partDerivateM = partialDerivateMStoch(k, m, x[i], y[i])
			partDerivateK = partialDerivateKStoch(k, m, x[i], y[i])
			k = k - (alpha*partDerivateK)
			m = m - (alpha*partDerivateM)
			temp += abs(partDerivateM) + abs(partDerivateK)
		j += 1
	return [k, m]

#only used to generate randomdata 
def createRandomValues(minX, maxX, minY, maxY, nbrOfValues):
	x = []
	y = []
	for i in range(0, nbrOfValues):
		x.append(random.uniform(minX, maxX))
		y.append(random.uniform(minY, maxY))
	return [x, y]
	


#testingData (the french version, english is commented out)
epsilon = 0.001
epoch = 2000
m = -1
k = 0
alpha = 0.1

yRawE = [36961,43621,15694,36231,29945,40588,75255,37709,30899,25486,37497,40398,74105,76725,18317]
xRawE = [2503,2992,1042,2487,2014,2805,5062,2643,2126,1784,2641,2766,5047,5312,1215]

#xRawE = [2217,2761,990,2274,1865,2606,4805,2396,1993,1627,2375,2560,4597,4871,1119]
#yRawE = [35680,42514,15162,35298,29800,40255,74532,37464,31030,24843,36172,39552,72545,75352,18031]


x = [float(i)/max(xRawE) for i in xRawE]
y = [float(i)/max(yRawE) for i in yRawE]

xx = np.asarray(x)
yy = np.asarray(y)
vec = np.polyfit(xx, yy, 1)

vec = linRegBatch(k,m,x,y,alpha,epsilon)
k1 = vec[0]
m1 = vec[1]


vec = linRegStoch(k,m,x,y,alpha,epoch)
k2 = vec[0]
m2 = vec[1]



#plotting the originaldata
plt.plot(x, y, 'ro')

#plotting the polyfit
plt.plot([min(x), max(x)], [vec[0]*min(x) + vec[1], vec[0]*max(x) + vec[1]], 'r--')

#plotting the batch regression
plt.plot([min(x), max(x)], [k1*min(x) + m1, k1*max(x) + m1], 'b--')
print("Batch: " + str(k1) + " - k " + str(m1) + " - m")
#plotting the stoch regression
plt.plot([min(x), max(x)], [k2*min(x) + m2, k2*max(x) + m2], 'g--')
print("Stoch: " + str(k1) + " - k " + str(m1) + " - m")
plt.show()
