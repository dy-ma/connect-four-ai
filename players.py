from audioop import reverse
from copy import deepcopy
import enum
import random
import time
import pygame
import math
import numpy as np
import sys # Remove if causing problems

class connect4Player(object):
	def __init__(self, position, seed=0):
		self.position = position
		self.opponent = None
		self.seed = seed
		random.seed(seed)

	def play(self, env, move):
		move = [-1]

class human(connect4Player):

	def play(self, env, move):
		move[:] = [int(input('Select next move: '))]
		while True:
			if int(move[0]) >= 0 and int(move[0]) <= 6 and env.topPosition[int(move[0])] >= 0:
				break
			move[:] = [int(input('Index invalid. Select next move: '))]

class human2(connect4Player):

	def play(self, env, move):
		done = False
		while(not done):
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

				if event.type == pygame.MOUSEMOTION:
					pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
					posx = event.pos[0]
					if self.position == 1:
						pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
					else: 
						pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
				pygame.display.update()

				if event.type == pygame.MOUSEBUTTONDOWN:
					posx = event.pos[0]
					col = int(math.floor(posx/SQUARESIZE))
					move[:] = [col]
					done = True

class randomAI(connect4Player):

	def play(self, env, move):
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		move[:] = [random.choice(indices)]

class stupidAI(connect4Player):

	def play(self, env, move):
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		if 3 in indices:
			move[:] = [3]
		elif 2 in indices:
			move[:] = [2]
		elif 1 in indices:
			move[:] = [1]
		elif 5 in indices:
			move[:] = [5]
		elif 6 in indices:
			move[:] = [6]
		else:
			move[:] = [0]

class minimaxAI(connect4Player):

	def simulateMove(self, env, move, player):
		env.board[env.topPosition[move]][move] = player
		env.topPosition[move] -= 1
		env.history[0].append(move)

	def evaluate(self, env):
		row_width = env.shape[1]
		col_height = env.shape[0]
		player = self.position
		opponent = self.opponent.position

		# make move
		# self.simulateMove(env, move, self.position)

		# expanded weights
		weights = np.array([[3, 4, 5, 7, 5, 4, 3],
							[4, 6, 8, 10, 8, 6, 4],
							[5, 8, 11, 13, 11, 8, 5],
							[5, 8, 11, 13, 11, 8, 5],
							[4, 6, 8, 10, 8, 6, 4],
							[3, 4, 5, 7, 5, 4, 3]
		])
		scores = np.zeros((6,7)).astype('int32')

		score = 0
		for i, row in enumerate(env.board):
			for j, cell in enumerate(row): 
				if cell == 0: continue
				elif cell == player: 
					score += weights[i][j]
				else: 
					score -= weights[i][j]
		return score

	def play(self, env, move):
		depth = 0
		self.max_depth = 3
		player = self.position
		env = deepcopy(env)
		env.visualize = False

		# ==== Decide Next Move ====
		# get possible moves
		possible = env.topPosition >= 0 # holds booleans: 0 for legal or 1 for illegal move
		indices = [] # hold possible moves
		for i, p in enumerate(possible):
			if p: indices.append(i)

		# loop through possible moves
		v = float('-inf')
		vs = [0] * 7
		for col in indices:
			tmp_v = self.min_value(deepcopy(env), col, depth + 1)
			vs[col] = tmp_v
			if tmp_v > v:
				mo = col
				v = tmp_v
		move[:] = [mo]
			
	def max_value(self, env, move, depth):
		self.simulateMove(env, move, self.opponent.position)
		# check for terminal state
		if env.gameOver(move, self.opponent.position):
			# Either win or tie, if every tile is filled then tie (payoff 0), otherwise player won (payoff 1).
			return 0 if len(env.history[0]) + len(env.history[1]) == env.shape[0] * env.shape[1] else -10000
		# If too deep, run evaluation
		if depth == self.max_depth:
			return self.evaluate(deepcopy(env))

		# ==== Decide Next Move ====
		# get possible moves
		possible = env.topPosition >= 0 # holds booleans: 0 for legal or 1 for illegal move
		indices = [] # hold possible moves
		for i, p in enumerate(possible):
			if p: indices.append(i)
		# loop through possible moves
		v = float('-inf')
		for col in indices:
			v = max( v, self.min_value(deepcopy(env), col, depth + 1) )
		return v

	def min_value(self, env, move, depth):
		self.simulateMove(env, move, self.position)
		# self.simulateMove(env, move, player)
		# check for terminal state
		if env.gameOver(move, self.position):
			# Either win or tie, if every tile is filled then tie (payoff 0), otherwise player won (payoff 1).
			return 0 if len(env.history[0]) + len(env.history[1]) == env.shape[0] * env.shape[1] else 10000
		# if too deep return eval
		if depth == self.max_depth:
			return self.evaluate(deepcopy(env))

		# ==== Decide Next Move ====
		# get possible moves
		possible = env.topPosition >= 0 # holds booleans: 0 for legal or 1 for illegal move
		indices = [] # hold possible moves
		for i, p in enumerate(possible):
			if p: indices.append(i)
		# loop through possible moves
		v = float('inf')
		for col in indices:
			v = min( v, self.max_value(deepcopy(env), col, depth + 1) )
		return v

class alphaBetaAI(connect4Player):

	def simulateMove(self, env, move, player):
		env.board[env.topPosition[move]][move] = player
		env.topPosition[move] -= 1
		env.history[0].append(move)

	def evaluate(self, env):
		row_width = env.shape[1]
		col_height = env.shape[0]
		player = self.position
		opponent = self.opponent.position

		# make move
		# self.simulateMove(env, move, self.position)

		# expanded weights
		weights = np.array([[3, 4, 5, 7, 5, 4, 3],
							[4, 6, 8, 10, 8, 6, 4],
							[5, 8, 11, 13, 11, 8, 5],
							[5, 8, 11, 13, 11, 8, 5],
							[4, 6, 8, 10, 8, 6, 4],
							[3, 4, 5, 7, 5, 4, 3]
		])
		scores = np.zeros((6,7)).astype('int32')

		score = 0
		for i, row in enumerate(env.board):
			for j, cell in enumerate(row): 
				if cell == 0: continue
				elif cell == player: 
					score += weights[i][j]
				else: 
					score -= weights[i][j]
		return score

	def successors(self, env, indices, player):
		# recieve valid indices, sort
		scores = deepcopy(indices)
		for i, index in enumerate(indices):
			new_board = deepcopy(env)
			self.simulateMove(new_board, index, player)
			scores[i] = self.evaluate(new_board)

		# sorted_indices = [ind for score, ind in sorted(zip(scores, indices))] # nonincreasing
		if player == self.position:
			return [ind for score, ind in sorted(zip(scores, indices), reverse=True)] # nondecreasing
		else:
			return [ind for score, ind in sorted(zip(scores, indices), reverse=False)]

	def play(self, env, move):
		depth = 0
		self.max_depth = 3
		player = self.position
		env = deepcopy(env)
		env.visualize = False

		# ==== Decide Next Move ====
		# get possible moves
		possible = env.topPosition >= 0 # holds booleans: 0 for legal or 1 for illegal move
		indices = [] # hold possible moves
		for i, p in enumerate(possible):
			if p: indices.append(i)

		# loop through possible moves
		v = float('-inf')
		vs = [0] * 7
		for col in self.successors(deepcopy(env), indices, self.position):
			tmp_v = self.min_value(deepcopy(env), col, depth + 1, float('-inf'), float('inf'))
			vs[col] = tmp_v
			if tmp_v > v:
				mo = col
				v = tmp_v
		move[:] = [mo]
			
	def max_value(self, env, move, depth, alpha, beta):
		self.simulateMove(env, move, self.opponent.position)
		# check for terminal state
		if env.gameOver(move, self.opponent.position):
			# Either win or tie, if every tile is filled then tie (payoff 0), otherwise player won (payoff 1).
			return 0 if len(env.history[0]) + len(env.history[1]) == env.shape[0] * env.shape[1] else -10000
		# If too deep, run evaluation
		if depth == self.max_depth:
			return self.evaluate(deepcopy(env))

		# ==== Decide Next Move ====
		# get possible moves
		possible = env.topPosition >= 0 # holds booleans: 0 for legal or 1 for illegal move
		indices = [] # hold possible moves
		for i, p in enumerate(possible):
			if p: indices.append(i)
		# loop through possible moves
		v = float('-inf')
		for col in self.successors(deepcopy(env), indices, self.position):
			v = max( v, self.min_value(deepcopy(env), col, depth + 1, alpha, beta) )
			if v >= beta: return v
			alpha = max(alpha, v)
		return v

	def min_value(self, env, move, depth, alpha, beta):
		self.simulateMove(env, move, self.position)
		# self.simulateMove(env, move, player)
		# check for terminal state
		if env.gameOver(move, self.position):
			# Either win or tie, if every tile is filled then tie (payoff 0), otherwise player won (payoff 1).
			return 0 if len(env.history[0]) + len(env.history[1]) == env.shape[0] * env.shape[1] else 10000
		# if too deep return eval
		if depth == self.max_depth:
			return self.evaluate(deepcopy(env))

		# ==== Decide Next Move ====
		# get possible moves
		possible = env.topPosition >= 0 # holds booleans: 0 for legal or 1 for illegal move
		indices = [] # hold possible moves
		for i, p in enumerate(possible):
			if p: indices.append(i)
		# loop through possible moves
		v = float('inf')
		for col in self.successors(deepcopy(env), indices, self.opponent.position):
			v = min( v, self.max_value(deepcopy(env), col, depth + 1, alpha, beta) )
			if v <= alpha: return v
			beta = min(beta, v)
		return v


SQUARESIZE = 100
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)




