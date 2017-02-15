#usr/bin/env python
import sys
sys.path.append('/Users/andreas/Downloads/libsvm-3.22/python')
from svmutil import *

class Reader():

	def __init__(self):
		pass

	def read_file(self, filename):
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


if __name__ == "__main__":
	r = Reader()
	#y, x = r.read_file("test_format.txt")
	with open("../test/test1.txt", "w") as file:
		file.write("")
	r.encode_file("../test/salammbo_a_fr.plot.txt", "../test/test1.txt", "1")
	r.encode_file("../test/salammbo_a_en.plot.txt", "../test/test1.txt", "2")
	y, x = r.read_file("../test/test1.txt")
	print y, x
