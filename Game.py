# Game.py
from random import randrange

# Directional Static Values
LEFT, RIGHT, UP, DOWN = 1, 2, 3, 4
# Size of Game Board (Size x Size)
BOARD_SIZE = 6

class Board:
	board = []
	snakeHead = {'x' : BOARD_SIZE // 2, 'y': BOARD_SIZE // 2}
	snakeTail = {'x' : BOARD_SIZE // 2, 'y': BOARD_SIZE // 2}

	class Tile:
		empty = True
		foodTile = False
		snakeTile = False

		def makeFood(self):
			self.empty = False
			self.foodTile = True

		def makeEmpty(self):
			self.empty = True
			self.foodTile = False
			self.snakeTile = False

		def addSnakeBody(self):
			self.empty = False
			self.snakeTile = True


	def __init__(self):
		for i in range(BOARD_SIZE):
			x = []
			for j in range(BOARD_SIZE):
				x.append(self.Tile())
			self.board.append(x)
		self.board[self.snakeHead['x']][self.snakeHead['y']].addSnakeBody()
		self.board[randrange(BOARD_SIZE)][randrange(BOARD_SIZE)].makeFood()



	def render(self):
		for row in range(BOARD_SIZE):
			for col in range(BOARD_SIZE):
				if self.board[row][col].empty: print("-", end="")
				elif self.board[row][col].foodTile: print("X", end="")
				else: print("O", end="")
			print()

test = Board()
test.render()