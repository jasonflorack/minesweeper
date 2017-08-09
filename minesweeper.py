#!/usr/bin/python

import os
from random import randint

class Square():
	def __init__(self):
		self.state = '-'
		self.is_a_bomb = False
		self.bombs_nearby = 0
		self.x = 0
		self.y = 0


class Game():
	def __init__(self):
		self.gameboard = []
		self.gameboard_length = 0
		self.total_squares = 0
		self.num_bombs = 0
		self.placing_bomb_marker = False
		self.finished = False
		self.won = False
	
	def start_game(self):
		self.gameboard_length = input("How long (and wide) should the gameboard be? ")
		self.total_squares = self.gameboard_length * self.gameboard_length
		self.create_gameboard()
		self.num_bombs = input("How many bombs should be on the gameboard (max={})? ".format(self.total_squares/2))
		self.place_bombs()
		self.get_nearby_numbers()
		self.begin_play()
		
	def create_gameboard(self):
		for i in range(0, self.gameboard_length):
			line_of_squares = []
			for n in range(0, self.gameboard_length):
				square = Square()
				square.x = i
				square.y = n
				line_of_squares.append(square)
			self.gameboard.append(line_of_squares)
	
	def place_bombs(self):
		for b in range(0, self.num_bombs):
			x, y = self.generate_x_y()
			while self.gameboard[x][y].is_a_bomb:
				x, y = self.generate_x_y()
			self.gameboard[x][y].is_a_bomb = True

	def generate_x_y(self):
		x = randint(0, self.gameboard_length-1)
		y = randint(0, self.gameboard_length-1)
		return x, y
	
	def get_nearby_numbers(self):
		for line in self.gameboard:
			for sq in line:
				if not sq.is_a_bomb:
					x = sq.x
					y = sq.y
					# Directly Above
					if y-1 >= 0:
						self.maybe_add_to_bombs_nearby(sq, x, y-1)
					# Upper Right
					if y-1 >= 0 and x+1 <= self.gameboard_length-1:
						self.maybe_add_to_bombs_nearby(sq, x+1, y-1)
					# Directly Right
					if x+1 <= self.gameboard_length-1:
						self.maybe_add_to_bombs_nearby(sq, x+1, y)
					# Lower Right
					if x+1 <= self.gameboard_length-1 and y+1 <= self.gameboard_length-1:
						self.maybe_add_to_bombs_nearby(sq, x+1, y+1)
					# Directly Below
					if y+1 <= self.gameboard_length-1:
						self.maybe_add_to_bombs_nearby(sq, x, y+1)
					# Lower Left
					if x-1 >= 0 and y+1 <= self.gameboard_length-1:
						self.maybe_add_to_bombs_nearby(sq, x-1, y+1)
					# Directly Left 
					if x-1 >= 0:
						self.maybe_add_to_bombs_nearby(sq, x-1, y)
					# Upper Left
					if x-1 >= 0 and y-1 >= 0:
						self.maybe_add_to_bombs_nearby(sq, x-1, y-1)

	def maybe_add_to_bombs_nearby(self, sq, x, y):
		if self.gameboard[x][y].is_a_bomb:
			sq.bombs_nearby += 1
	
	def print_gameboard(self):
		print ('')
		print ('')
		header_row = '  | '
		horizontal_line = '--+'
		for i in range(0, self.gameboard_length):
			header_row += str(i) + ' '
			horizontal_line += '--'
		print(header_row)
		print(horizontal_line)
		header_col = 0
		for line in self.gameboard:
			print_str = str(header_col) + ' | '
			for sq in line:
				print_str += sq.state + ' '
			print(print_str)
			header_col += 1
	
	def print_final_gameboard(self):
		print ('')
		print ('')
		header_row = '  | '
		horizontal_line = '--+'
		for i in range(0, self.gameboard_length):
			header_row += str(i) + ' '
			horizontal_line += '--'
		print(header_row)
		print(horizontal_line)
		header_col = 0
		for line in self.gameboard:
			print_str = str(header_col) + ' | '
			for sq in line:
				if sq.bombs_nearby:
					print_str += str(sq.bombs_nearby) + ' '
				else:
					print_str += '* '
			print(print_str)
			header_col += 1
	
	def begin_play(self):
		while self.finished == False:
			self.print_gameboard()
			test_x = str(raw_input("X value (or b/u to mark/unmark bomb): "))
			if test_x == 'b':
				self.placing_bomb_marker = True
				bomb_x = int(raw_input('X value of bomb to mark: '))
				bomb_y = int(raw_input('Y value of bomb to mark: '))
				self.gameboard[bomb_y][bomb_x].state = 'B'
			elif test_x == 'u':
				self.placing_bomb_marker = True
				bomb_x = int(raw_input('X value of bomb to unmark: '))
				bomb_y = int(raw_input('Y value of bomb to unmark: '))
				self.gameboard[bomb_y][bomb_x].state = '-'
			else:
				test_x = int(test_x)
				test_y = int(input("Y value: "))
			if self.placing_bomb_marker == False:
				if self.gameboard[test_y][test_x].is_a_bomb:
					self.gameboard[test_y][test_x].state = '*'
					self.print_final_gameboard()
					self.finished = True
				self.gameboard[test_y][test_x].state = str(self.gameboard[test_y][test_x].bombs_nearby)
			self.placing_bomb_marker = False
			self.check_for_win()
		if self.finished == True and self.won == False:
			print('You hit a bomb.  Game over.')
	
	def check_for_win(self):
		total_misses = 0
		for line in self.gameboard:
			for sq in line:
				if sq.state == str(sq.bombs_nearby):
					total_misses +=1
		if total_misses == self.total_squares-self.num_bombs:
			self.finished = self.won = True
			self.print_gameboard()
			print ('You won!')

# Run the Game
g = Game()
g.start_game()
