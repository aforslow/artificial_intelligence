#!usr/bin/env python

import sys

class Game():
	def __init__(self):
		self.table = [['_' for x in range(8)] for y in range(8)]
		self.table[3][3] = 'b'
		self.table[3][4] = 'w'
		self.table[4][3] = 'w'
		self.table[4][4] = 'b'
		self.n_pieces = 4
		self.max_pieces = 8*8
		self.n_possible_moves = 0

	def print_table(self):
		print ""
		for x in range(9):
			for y in range(9):
				if (x==0):
					if (y==0):
						print " ",
					else:
						print chr(y+96), "",
				elif (y==0):
					print x,
				else:
					print self.table[x-1][y-1] + " ",
			print ""
		print ""

	def play(self):
		self.quitted = False
		while (self.n_pieces < self.max_pieces):
			
			print "\n"
			print "===================== NEW ROUND ======================="
			print "Current game board: "
			if (self.n_pieces % 2 == 0):
				piece = 'w'
			else:
				piece = 'b'
			self.update_possible_moves(piece)
			print "Possible number of moves for",
			print "player", piece +":", self.n_possible_moves
			if (self.quitted or self.n_possible_moves == 0):
				break
			self.print_table()
			self.delete_tips()
			self.play_next_round(piece)
			self.print_score()
		print "Game finished!"
		self.print_score()

	def delete_tips(self):
		for row in range(8):
			for col in range(8):
				if self.table[row][col] == 'x':
					self.table[row][col] = '_'

	def update_possible_moves(self, piece):
		self.n_possible_moves = 0
		self.possible_moves = []
		for row in range(8):
			for col in range(8):
				if self.legal_move(piece, row, col):
					self.table[row][col] = 'x'
					self.n_possible_moves += 1
					self.possible_moves.append((row,col))

	def get_possible_moves(self):
		return self.possible_moves

	def calc_score(self):
		score_w = 0
		score_b = 0
		for x in range(8):
			for y in range(8):
				if (self.table[x][y] == 'b'):
					score_b += 1
				elif (self.table[x][y] == 'w'):
					score_w += 1
		return score_w, score_b

	def print_score(self):
		score_w, score_b = self.calc_score()
		print "______________________"
		print "Score: "
		print "White: ", score_w, "Black: ", score_b
		print "______________________"	

	def play_next_round(self, piece):
		print piece, "player next."
		while True:
			try:
				print "_____________________________________________"
				coords = raw_input("Where do you want to put \n" +
					"your piece (e.g. 1a)? (type q to quit) \n")
				if (coords == 'q'):
					self.quit()
				elif (len(coords) == 2):
					x = int(coords[0]) - 1
					y = ord(coords[1]) - 97
					if not (0 <= y < 8):
						raise ValueError
					self.put_piece(piece, x, y)
				else:
					raise ValueError
				break
			except (NameError, ValueError, IndexError) as e:
				print "Wrong input format, try again! (e.g. 3c)"
			except IllegalMoveError as e:
				pass

		print "_____________________________________________"
		
		

	def quit(self):
		self.print_table()
		self.print_score()
		self.quitted = True
		print "Quitting..."
		sys.exit()

	def put_piece(self, piece, x, y):
		if (piece == 'w' or piece == 'b'):
			if (self.legal_move(piece, x, y)):
				self.convert_table(piece, x, y)
				self.table[x][y] = piece
				self.n_pieces += 1
				self.print_table()
			else:
				print "Illegal move"
				raise IllegalMoveError
		else:
			print "Wrong format for piece. Please write 'w' or 'b'!"

	def convert_table(self, piece, x, y):
		for row_dir in range(-1,2):
			for col_dir in range(-1,2):
				if (row_dir == 0 and col_dir == 0):
					continue
				if self.direction_ok(piece, x, y, row_dir, col_dir):
					self.convert_direction(piece, x, y, row_dir, col_dir)

	def convert_direction(self, piece, x, y, row_dir, col_dir):
		x += row_dir
		y += col_dir
		while (self.table[x][y] != piece and 
			self.table[x][y] != '_'):
			self.table[x][y] = piece
			x += row_dir
			y += col_dir

	def legal_move(self, piece, x, y):
		if (self.table[x][y] == '_'):
			for row_dir in range(-1,2):
				for col_dir in range(-1,2):
					if (row_dir == 0 and col_dir == 0):
						continue					
					if self.direction_ok(piece, x, y, row_dir, col_dir):
						return True
		return False

	def direction_ok(self, piece, x, y, row_dir, col_dir):
		x += row_dir
		y += col_dir
		if not self.in_boundaries(x,y):
			return False
		if piece == 'w' and self.table[x][y] != 'b':
			return False
		if piece == 'b' and self.table[x][y] != 'w':
			return False

		x += row_dir
		y += col_dir
		while (self.in_boundaries(x,y)): 
			if (self.table[x][y] == piece):
				return True
			x += row_dir
			y += col_dir		
		return False

	def in_boundaries(self, x, y):
		if ((0 <= x < 8) and (0 <= y < 8)):
			return True
		return False

class IllegalMoveError(Exception):
	pass

if __name__ == "__main__":
	game = Game()
	game.play()

