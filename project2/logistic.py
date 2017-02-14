
def sigmoid(x):
	nom = 1
	dom = 1 + e ** (-x)

	return nom/dom


def gradientDecent(x, y, w):
	theta = 0
	for i in range(0, len(x)):
		theta += x[i]*(y - sigmoid(x[i]*w))
	return theta/len(x)

def step(x, y, w, alpha):
	for i in range(0, len(w)):
		w[i] = w[i] + alpha*gradientDecent(x[i], y[i], w[i])
	return w

