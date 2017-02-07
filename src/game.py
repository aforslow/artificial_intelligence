#!usr/bin/env python

import sys

class Game():
	def __init__(self):
		self.table = self.get_init_state()
		self.n_pieces = 4
		self.max_pieces = 8*8
		self.n_possible_moves = 0
		self.players = ['w', 'b']
		self.computer_piece = 'b'
		self.points = {'w':2, 'b':2}
		self.next_player = {'w':'b', 'b':'w'}

	def get_init_state(self):
		table = [['_' for x in range(8)] for y in range(8)]
		table[3][3] = 'b'
		table[3][4] = 'w'
		table[4][3] = 'w'
		table[4][4] = 'b'
		return table

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

		while True:
			try:
				AI_player = raw_input("Which player should AI be? ('b' or 'w')")
				if (AI_player == 'w' or AI_player == 'b'):
					self.computer_piece = AI_player
					self.AI = AI(3, AI_player)
					break
				else:
					print "Wrong input format, try again (write w or b)"
			except:
				print "Wrong input format caused error. Write w or b"

		while (self.n_pieces < self.max_pieces):
			
			print "\n"
			print "===================== NEW ROUND ======================="
			print "Current game board: "
			piece = self.players[self.n_pieces % 2]
			if (piece == self.computer_piece):
				state = self.AI.get_next_state()
				self.set_state(state)
				self.print_table()
			else:
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
				if self.legal_move(self.table, piece, row, col):
					self.table[row][col] = 'x'
					self.n_possible_moves += 1
					self.possible_moves.append((row,col))

	def get_possible_moves(self, state, piece):
		possible_moves = []
		for row in range(8):
			for col in range(8):
				if self.legal_move(state, piece, row, col):
					possible_moves.append((row,col))
		return possible_moves

	def get_state(self):
		return self.table

	def get_current_piece(self):
		if (self.n_pieces % 2 == 0):
			return 'w'
		else:
			return 'b'

	def get_state_piece(self, state):
		n_pieces = get_piece_count(state)
		return self.players[n_pieces % 2]

	def get_piece_count(self, state):
		n_pieces = 0
		for row in range(8):
			for col in range(8):
				if state[row][col] == 'w' or state[row][col] == 'b':
					n_pieces += 1
		return n_pieces

	def set_state(self, state):
		self.table = state
		self.n_pieces = get_piece_count(self.table)

	def get_score(self, state, piece):
		score = 0
		for row in range(8):
			for col in range(8):
				if (state[row][col] == piece):
					score += 1
		return score

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

	def play_from_state(self, state, current_piece, x, y):
		piece = self.next_player[current_piece]
		self.put_piece(state, piece, x, y)
		return self.table, piece

	def computer_play_next_round(self, piece, x, y):
		print piece, "player next."
		self.put_piece(self.table, piece, x, y)
		print "Computer played:", str(x+1) + chr(y+96) 

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
					self.put_piece(self.table, piece, x, y)
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

	def put_piece(self, state, piece, x, y):
		self.table = state
		if (piece == 'w' or piece == 'b'):
			if (self.legal_move(state, piece, x, y)):
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
				if self.direction_ok(self.table, piece, x, y, row_dir, col_dir):
					self.convert_direction(piece, x, y, row_dir, col_dir)

	def convert_direction(self, piece, x, y, row_dir, col_dir):
		x += row_dir
		y += col_dir
		while (self.table[x][y] != piece and 
			self.table[x][y] != '_'):
			self.table[x][y] = piece
			x += row_dir
			y += col_dir

	def legal_move(self, state, piece, x, y):
		if (state[x][y] == '_'):
			for row_dir in range(-1,2):
				for col_dir in range(-1,2):
					if (row_dir == 0 and col_dir == 0):
						continue					
					if self.direction_ok(state, piece, x, y, row_dir, col_dir):
						return True
		return False

	def direction_ok(self, state, piece, x, y, row_dir, col_dir):
		x += row_dir
		y += col_dir
		if not self.in_boundaries(x,y):
			return False
		if piece == 'w' and state[x][y] != 'b':
			return False
		if piece == 'b' and state[x][y] != 'w':
			return False

		x += row_dir
		y += col_dir
		while (self.in_boundaries(x,y)): 
			if (state[x][y] == piece):
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

