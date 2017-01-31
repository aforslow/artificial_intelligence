

class Table():
	
	def __init__(self):
		self.table = [['_' for x in range(8)] for y in range(8)]
		self.table[3][3] = 'b'
		self.table[3][4] = 'w'
		self.table[4][3] = 'w'
		self.table[4][4] = 'b'

	def print_table(self):
		for x in range(8):
			for y in range(8):
				print self.table[x][y] + " ",
			print ""

if __name__ == "__main__":
	t = Table()
	t.print_table()


