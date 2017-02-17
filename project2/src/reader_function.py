#!/usr/bin/env python
import sys
sys.path.append('/Users/andreas/Downloads/libsvm-3.22/python')
from svmutil import *
import random

class Reader():

	def __init__(self):
		pass

	def libsvm_read_file(self, filename):
		self.y, self.x = svm_read_problem(filename)
		return self.y, self.x

	def encode_file(self, source, dest, idx):
		src_file = open(source, 'r')
		dest_file = open(dest, 'a')
		for src_line in src_file:
			dest_line = ""
			dest_line += idx
			ctr = 1
			for value in src_line.split():
				dest_line += " " + str(ctr) + ":" + str(value)
				ctr += 1
			dest_file.write(dest_line + "\n")
		src_file.close()
		dest_file.close()

	def scale_data(self):
		#Get max & min vals
		max_vals = []
		min_vals = []
		for list_obj in self.x:
			max_vals.append(max(list_obj.values()))
			min_vals.append(min(list_obj.values()))
		min_val = min(min_vals)
		max_val = max(max_vals)

		#Scale the data
		for list_obj in self.x:
			for key in list_obj.keys():
				list_obj[key] = (list_obj[key] - min_val) / (max_val - min_val)

		return self.x

	def get_randomized_data(self):
		y, x = self.shuffle(self.y, self.x)
		return y, x

	def shuffle(self, y, x):
		indices = [n for n in range(len(self.y))]
		random.shuffle(indices)
		rand_y = []
		rand_x = []
		for idx in indices:
			rand_y.append(y[idx])
			rand_x.append(x[idx])
		return rand_y, rand_x

if __name__ == "__main__":
	r = Reader()
	#y, x = r.read_file("test_format.txt")
	with open("../test/test1.txt", "w") as file:
		file.write("")
	r.encode_file("../test/salammbo_a_fr.plot.txt", "../test/test1.txt", "0")
	r.encode_file("../test/salammbo_a_en.plot.txt", "../test/test1.txt", "1")
	y, x = r.libsvm_read_file("../test/test1.txt")
	print x
	print ""
	z = r.scale_data()
	z1 = z[0]
	z2 = z1[1]
	print z
	print z2
