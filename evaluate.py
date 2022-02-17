import enum
import numpy as np

def gameOver(self):
	# Find extrema to consider
	j = 6
	i = 5
	player = 1
	opponent = 2
	minRowIndex = max(j - 3, 0)
	maxRowIndex = min(j + 3, self.shape[1]-1)
	maxColumnIndex = max(i - 3, 0)
	minColumnIndex = min(i + 3, self.shape[0]-1)
	minLeftDiag = [max(j - 3, j), min(i + 3, self.shape[0]-1)]
	maxLeftDiag = [min(j + 3, self.shape[1]-1), max(i - 3, 0)]
	minRightDiag = [min(j + 3, j), min(i + 3, self.shape[0]-1)]
	maxRightDiag = [max(j - 3, 0), max(i - 3, 0)]
	# Iterate over extrema to find patterns
	# Horizontal solutions
	count = 0
	for s in range(minRowIndex, maxRowIndex+1):
		if self.board[i, s] == player:
			count += 1
		else:
			count = 0
		if count == 4:
			return True
	# Verticle solutions
	count = 0
	for s in range(maxColumnIndex, minColumnIndex+1):
		if self.board[s, j] == player:
			count += 1
		else:
			count = 0
		if count == 4:
			return True
	# Left diagonal
	row = i
	col = j
	count = 0
	up = 0
	while row > -1 and col > -1 and self.board[row][col] == player:
		count += 1
		row -= 1
		col -= 1
	down_count = count
	row = i + 1
	col = j + 1
	while row < self.shape[0] and col < self.shape[1] and self.board[row][col] == player:
		count += 1
		row += 1
		col += 1
	if count >= 4:
		return True
	# Right diagonal
	row = i
	col = j
	count = 0
	while row < self.shape[0] and col > -1 and self.board[row][col] == player:
		count += 1
		row += 1
		col -= 1
	down_count = count
	row = i - 1
	col = j + 1
	while row > -1 and col < self.shape[1] and self.board[row][col] == player:
		count += 1
		row -= 1
		col += 1
	if count >= 4:
		return True
	return len(self.history[0]) + len(self.history[1]) == self.shape[0]*self.shape[1]

# def terminal(board):
# 	# horizontals
# 	player = 1
# 	for row in board:
# 		count = 0
# 		for cell in row:
# 			if cell == player:
# 				count += 1
# 		if count == 4:
# 			return True
# 	# verticals
# 	for j in range(0, 6):
# 		for i in range(0, 5):
			

def evaluat(board):
	# Count number of possible win conditions
	row_width = 7
	col_height = 6
	# Total possible wins
	# total_wins = (row_width * 4) + (col_height * 4) + (7)

	player = 1
	opponent = 2

	# horizontals
	# for i, row in enumerate(board):
	# 	for j, ele in enumerate(row[:row_width - 3]):
	# 		next_four = [value for index, value in enumerate(row[j:j + 4])]
	# 		# increment for each player and decrement for each opponent
	# 		score += sum(1 for x in next_four if x == player)
	# 		score -= sum(1 for x in next_four if x == opponent)

	# # verticals
	# for j in range(col_height - 3):
	# 	for i in range(row_width):
	# 		next_four = [board[i][j], board[i][j+1], board[i][j + 2], board[i][j + 3]]
	# 		score += sum(1 for x in next_four if x == player)
	# 		score -= sum(1 for x in next_four if x == opponent)

	# diagonals
	
	# pre-added
	weights = np.array([[3, 4, 5, 7, 5, 4, 3],
						[4, 6, 8, 10, 8, 6, 4],
						[5, 8, 11, 13, 11, 8, 5],
						[5, 8, 11, 13, 11, 8, 5],
						[4, 6, 8, 10, 8, 6, 4],
						[3, 4, 5, 7, 5, 4, 3]
	])

	score = 0
	for i, row in range(board):
		for j, cell in enumerate(row): 
			if cell == 0: continue
			elif cell == player: score += weights[i][j]
			else: score -= weights[i][j]

	return score

board = np.array([[0, 1, 0, 0, 0, 0, 0],
				  [0, 0, 0, 0, 0, 0, 0],
				  [0, 0, 0, 0, 0, 0, 0],
				  [0, 0, 0, 0, 0, 0, 0],
				  [0, 0, 0, 0, 0, 0, 0],
				  [0, 0, 0, 0, 0, 0, 0]]
).astype('int32')

print(board)
print(gameOver(board))