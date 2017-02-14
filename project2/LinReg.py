
import random
import matplotlib.pyplot as plt
import numpy as np

def error(k, m, x, y):
	sumError = 0
	for i in range(0, len(y)):
		sumError += (y[i] - (k*x[i] + m))**2
	return sumError/len(y)
#k as in the k in y = kx + m
def partialDerivateK(k, m, x, y):
	gradient = 0
	for i in range(0, len(y)):
		gradient += -x[i]*(y[i] - (k*x[i] + m))
	return 2*gradient/len(y)

#m as in the m in y = kx + m
def partialDerivateM(k, m, x, y):
	gradient = 0
	for i in range(0, len(y)):
		gradient += -(y[i] - (k*x[i] + m))
	return 2*gradient/len(y)

#k and m in y = kx + m and alpha as the learning rate
def step(k, m, x, y, alpha):
	newK = 0
	newM = 0
	partDerivateM = partialDerivateM(k, m, x, y)
	partDerivateK = partialDerivateK(k, m, x, y)
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
iterations = 5000*10

m = -1
k = 0
alpha = 0.0005

vec = createRandomValues(minX, maxX, minY, maxY, nbrOfValues)
x = vec[0]
y = vec[1]
plt.plot(x, y, 'ro')
for i in range(0, iterations):
	temp = step(k, m, x, y, alpha)
	k = temp[0]
	m = temp[1]
	
plt.plot([minX, maxX], [k*minX + m, k*maxX + m])
#plt.show()
#Now to test it with a regular least square method



xx = np.asarray(x)
yy = np.asarray(y)
print(str(len(xx)))
print(str(len(yy)))
vec = np.polyfit(xx, yy, 1)
plt.plot([minX, maxX], [vec[0]*minX + vec[1], vec[0]*maxX + vec[1]], 'r--')
plt.show()
