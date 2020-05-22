# Game.py
from random import randrange, choice
import time

# Directional Static Values
LEFT, RIGHT, UP, DOWN = 1, 2, 3, 4
opposite = {LEFT: RIGHT, RIGHT: LEFT, UP: DOWN, DOWN: UP}
# Size of Game Board (Size x Size)
BOARD_SIZE = 6


class GameOver(Exception):
	"""Custom exception class for when snake dies"""
	pass


class Board:
	# board contains all Tile objects in a 2x2 array that represents the playing field
	# open_spaces is a set of tuples that reprsent empty Tile coordinates
	# snake is a list containing coordinates of the snakes body in the order that they are meant to be
	# score is self explanatory (should reflect size of snake)
	# direction used to keep track of the last direction that the player is chose to move in
	board = []
	open_spaces = set()
	snake = []
	score = 1
	direction = UP

	class Tile:
		# Tile object used to represent each square on the board
		# Keeps track of the state of each square to make it easy for rendering
		empty = True
		foodTile = False
		snakeTile = False

		def makeFood(self):
			# Marks tile as having food
			self.empty = False
			self.foodTile = True

		def makeEmpty(self):
			# Marks tile as empty
			self.empty = True
			self.foodTile = False
			self.snakeTile = False

		def makeSnakeBody(self):
			# Adds snake onto the tile
			self.empty = False
			self.snakeTile = True
			self.foodTile = False


	def __init__(self):
		self.make_board()
		self.make_snake()
		self.place_random_food()
		self.render()

	def run(self, direction: int):
		# Meant to run the game until an error is thrown
		# direction parameter moves snake in that direction; any invalid number just moves the snake forward

		"""while True:
			# TODO : CREATE MOVES BASED ON USER ACTIONS FROM PRESSING KEYS

			# Sleep so that the game can be followed when watching it
			time.sleep(0.25)

			# Selects random move that doesn't go the opposite direction the snake was already going
			temp = opposite[self.direction]
			while temp == opposite[self.direction]:
				temp = choice([LEFT, RIGHT, UP, DOWN])
			self.direction = temp

			# Moves the snake and prints the board
			self.move_snake(self.direction)
			self.render()"""

		if direction in [LEFT, RIGHT, UP, DOWN] and direction != opposite[self.direction]:
			self.direction = direction

		self.move_snake(self.direction)
		self.render()
		
	def make_board(self):
		# Initites board full of Tile objects in correct size and initiates full open_space set
		for i in range(BOARD_SIZE):
			x = []
			for j in range(BOARD_SIZE):
				x.append(self.Tile())
				self.open_spaces.add((i, j))
			self.board.append(x)

	def make_snake(self):
		# Initiates the snake with a size 1 in the middle of the board
		middle = BOARD_SIZE // 2
		self.snake.append((middle, middle))
		self.board[middle][middle].makeSnakeBody()
		self.open_spaces.remove((middle, middle))

	def place_random_food(self):
		# Picks a random coordinate from the open_spaces set and places food there
		coords = choice(list(self.open_spaces))
		x, y = coords[0], coords[1]
		self.board[x][y].makeFood()

	def move_snake(self, delta):
		# Moves the direction in the direction that the player last picked
		x, y = self.snake[-1]

		# Figures out coordinates the snake should move into next based on direction
		if delta == UP:
			x, y = x-1, y
		elif delta == DOWN:
			x, y = x+1, y
		elif delta == LEFT:
			x, y = x, y-1
		else:
			x, y = x, y+1

		# Checks if next move is valid or not, if not, throws error
		if (x, y) not in self.open_spaces:
			raise GameOver("Game Over")

		# First moves snake into new spot and checks if there is food underneath
		self.snake.append((x, y))
		landed_on_food = self.board[x][y].foodTile
		
		# Accounts for a move where there is no food on the tile by removing tail-end of snake
		if landed_on_food == False:
			x2, y2 = self.snake.pop(0)
			self.board[x2][y2].makeEmpty()
			self.open_spaces.add((x2, y2))

		# Adds new snake body to the coordinate player moved into
		self.board[x][y].makeSnakeBody()
		self.open_spaces.remove((x, y))

		# Places food on board if snake ate one
		if landed_on_food:
			self.score += 1
			self.place_random_food()

	def render(self):
		# Renders the snake board onto the terminal
		for i in range(10): print()
		print("SCORE:", self.score)
		for row in range(BOARD_SIZE):
			for col in range(BOARD_SIZE):
				if self.board[row][col].empty: print("-", end="")
				elif self.board[row][col].foodTile: print("X", end="")
				else: print("O", end="")
			print()


# uncomment this block to run game logic in console; input numbers for direction
"""game = Board()
while True:
	num = eval(input())
	game.run(num)"""