# Game.py
from random import randrange, choice

# Directional Static Values
LEFT, RIGHT, UP, DOWN = 1, 2, 3, 4
opposite = {LEFT: RIGHT, RIGHT: LEFT, UP: DOWN, DOWN: UP, None: None}

# Size of Game Board (Size x Size)
BOARD_SIZE = 6


class GameOver(Exception):
	"""Custom exception class for when snake dies or if game is won; mainly used to let interface know when to stop"""
	pass


class Board:
	# board contains all Tile objects in a 2x2 array that represents the playing field
	# open_spaces is a set of tuples that represent empty Tile coordinates
	# snake is a list containing coordinates of the snakes body in the order that they are meant to be
	# score is self explanatory (should reflect size of snake)
	# direction used to keep track of the last direction that the player is chose to move in
	board = [] #list of lists(containing Tiles) 
	open_spaces = set() #set of tuples
	snake = [] #list of tuples, last element is where the head of the snake is.
	food = [] #list of integers
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

	def run(self, direction=None):
		# Meant to run the game until an error is thrown
		# direction parameter moves snake in that direction; any invalid number just moves the snake forward

		if direction in [LEFT, RIGHT, UP, DOWN] and direction != opposite[self.direction]:
			self.direction = direction
		self.move_snake(self.direction)
		self.render()

	def make_board(self):
		# Initiates board full of Tile objects in correct size and initiates full open_space set
		for i in range(BOARD_SIZE):
			x = []
			for j in range(BOARD_SIZE):
				x.append(self.Tile())
				self.open_spaces.add((i, j))
			self.board.append(x)

	def make_snake(self):
		# Initiates the snake with a size 1 in the middle of the board
		middle = BOARD_SIZE // 2
		self.snake.append((middle + 1, middle))
		self.snake.append((middle, middle))
		self.board[middle][middle].makeSnakeBody()
		self.board[middle + 1][middle].makeSnakeBody()
		self.open_spaces.remove((middle, middle))
		self.open_spaces.remove((middle + 1, middle))

	def place_random_food(self):
		# Picks a random coordinate from the open_spaces set and places food there
		coords = choice(list(self.open_spaces))
		x, y = coords[0], coords[1]
		self.food = [x, y]
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
			if self.won():
				raise GameOver("You Win")
			self.place_random_food()

	def won(self):
		return self.score == BOARD_SIZE ** 2 - 1

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
		print(self.blocked_direction())
		print(self.food_direction())
		print(self.food_distance())



	def blocked_direction(self):
		"""Returns an array displaying which directions the snake is blocked in.
		Array corresponds to [left, straight, right]. 0 = Not Blocked | 1 = Blocked."""
		def check_block(x, y):
			if (x, y) not in self.open_spaces:
				return 1
			return 0

		x, y = self.snake[-1]

		if self.direction == UP:
			return [check_block(x, y-1), check_block(x-1, y), check_block(x, y+1)]
		elif self.direction == LEFT:
			return [check_block(x+1, y), check_block(x, y-1), check_block(x-1, y)]
		elif self.direction == RIGHT:
			return [check_block(x-1, y), check_block(x, y+1), check_block(x+1, y)]
		else:
			return [check_block(x, y+1), check_block(x+1, y), check_block(x, y-1)]

	def food_distance(self):
		"""Returns a float representing how many units away the food is using distance formula"""
		x, y = self.snake[-1]
		return (((x - self.food[0]) ** 2) + ((y - self.food[1]) ** 2)) ** .5

	def food_direction(self):
		"""Returns an array representing where the food is compared to the snake.
		Output: [x, y]
			x = -1: Food is Up
			x =  0: Food is same row
			x =  1: Food is Down
			y = -1: Food is Left
			y =  0: Food is same col
			y =  1: Food is Right
		"""

		x, y = self.snake[-1]
		output = [0, 0]

		if x < self.food[0]:
			output[0] = 1
		elif x > self.food[0]:
			output[0] = -1
		else:
			pass

		if y < self.food[1]:
			output[1] = 1
		elif y > self.food[1]:
			output[1] = -1
		else:
			pass

		return output


# uncomment this block to run game logic in console; input numbers for direction
if __name__ == "__main__":
	game = Board()

	while True:
		num = eval(input())
		game.run(num)
		if game.won():
			break
