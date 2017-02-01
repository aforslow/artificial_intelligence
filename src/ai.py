#!usr/bin/env python

class AI():

	def __init__(self):
		self.depth = 3
		self.alpha = -float("inf")
		self.beta = float("inf")

	def make_move(self):
		alphabeta()

	def alphabeta(self, node, depth, alpha, beta, maximizingPlayer):
		if (depth == 0 or len(node.child_list) == 0):
			return node.value
		if maximizingPlayer:
			v = -float("inf")
			for child in node.child_list:
				v = max(v, alphabeta(child, depth-1, alpha, beta, False))
				alpha = max(alpha, v)
				if beta <= alpha:
					break
				return v
		else:
			v = float("inf")
			for child in node.child_list:
				v = min(v, alphabeta(child, depth-1, alpha, beta, True))
				beta = min(beta, v)
				if beta <= alpha:
					break
				return v

class Node():

	def __init__(self):
		self.child_list = []
		self.value = None
		self.state = None

	def add_child(self):
		pass
