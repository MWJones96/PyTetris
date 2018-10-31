import pygame
import random
import numpy as np

"""
Represents a piece that is currently active in the game
Has a color, a shape represented by a Boolean array
and an x, y co-ordinate of its top-left corner
"""
class Piece:
	def __init__(self, color, shape, x, y):
		self.color = color
		self.shape = shape
		self.x = x
		self.y = y

"""
Represents the game of Tetris being played, with separate
update and render routines
"""
class Game:
	def __init__(self, rows, cols, block_size, screen):
		self.rows = rows # Rows in the game
		self.cols = cols # Columns in the game
		self.level = 0 # The current level
		self.score = 0 # The current score
		self.lines_completed = 0 # The total number of lines that have been cleared
		self.block_size = block_size # The size (in pixels) of one block
		self.screen = screen # The screen that will be drawed to
		self.state = np.zeros((rows, cols), dtype=(int, 3)) # Represents the color for each block placed in the game
		self.running = True # Whether the game is ongoing
		self.num_updates = 0 # The number of updates that have occurred since the last reset
		self.gravity_update_rate = 15 - (self.level * 2) # The rate at which the block falls (the update delay)
		self.move_update_rate = 5	# The rate at which player input is received
		self.possible_shapes = [[[True, True, True, True]], 				# Boolean arrays for each possible shape
								[[True, False, False], [True, True, True]], 
								[[False, False, True], [True, True, True]], 
								[[True, True], [True, True]], 
								[[False, True, True], [True, True, False]],
								[[False, True, False], [True, True, True]], 
								[[True, True, False], [False, True, True]]]
		self.possible_colors = [(0, 0xff, 0xff),	# Each possible color of a block
								(0, 0, 0xff),
								(0xff, 0xa5, 0x00),
								(0xff, 0xff, 0x00),
								(0x00, 0xff, 0x00),
								(0x8b, 0x00, 0x8b),
								(0xff, 0x00, 0x00)]
		self.current_piece = Piece(random.choice(self.possible_colors), random.choice(self.possible_shapes), self.cols//2, 0) # A randomly-chosen piece
		self.next_piece = Piece(random.choice(self.possible_colors), random.choice(self.possible_shapes), self.cols//2, 0)	# The piece that comes next

	"""
	Takes in the keys pressed and updates the state of the game accordingly
	"""
	def update(self, keys):
		if not self.current_piece:
			return

		# Checks if the user is pressing left, right, or up
		if(self.num_updates % self.move_update_rate == 0):
			if(keys[pygame.K_LEFT]):
				 if(not self.check_collision(self.current_piece.shape, self.current_piece.x - 1, self.current_piece.y)):
				 	self.current_piece.x -= 1
			elif(keys[pygame.K_RIGHT]):
				 if(not self.check_collision(self.current_piece.shape, self.current_piece.x + 1, self.current_piece.y)):
				 	self.current_piece.x += 1
			elif(keys[pygame.K_UP]):
				rotated_shape = list(zip(*self.current_piece.shape[::-1]))
				if(not self.check_collision(rotated_shape, self.current_piece.x, self.current_piece.y)):
					self.current_piece.shape = rotated_shape

		# Modifies the update rate depending on whether the down key is pressed
		if(keys[pygame.K_DOWN]):
			self.gravity_update_rate = 1
		else:
			self.gravity_update_rate = 15 - (self.level * 2)

		# Will only make the block fall down after update_rate many updates
		if(self.num_updates % self.gravity_update_rate == 0):
			#If the new position of the block will not cause a collision
			if(not self.check_collision(self.current_piece.shape, self.current_piece.x, self.current_piece.y + 1)):
				self.current_piece.y += 1
			# If it will, then initialise new current_block and discard the old one where it was
			else:
				x_base = self.current_piece.x
				y_base = self.current_piece.y
				# Adds the current data from the current block to the previous block state
				for row in range(len(self.current_piece.shape)):
					for col in range(len(self.current_piece.shape[0])):
						if(self.current_piece.shape[row][col]):
							self.state[y_base + row][x_base + col] = self.current_piece.color

				# Checks for and removes full rows
				self.remove_full_rows()

				# Sets the next piece as the current piece
				self.current_piece = self.next_piece
				# Initialises a new next piece
				self.next_piece = Piece(random.choice(self.possible_colors), random.choice(self.possible_shapes), self.cols//2, 0)

				if(self.check_collision(self.current_piece.shape, self.current_piece.x, self.current_piece.y)):
					self.running = False

		self.num_updates += 1

	"""
	Draws the state of the game to the screen
	"""
	def render(self):
		if not self.current_piece:
			return

		# Fill the screen as block
		screen.fill((0, 0, 0))

		# Draw a solid white line in the middle of the canvas
		pygame.draw.line(self.screen, (255, 255, 255), (self.screen.get_width()//2, 0), (self.screen.get_width()//2, self.screen.get_height()), 10)

		#Draw the text in the right half of the screen
		txt_title = pygame.font.Font('freesansbold.ttf', 35)
		ts_title = txt_title.render("PyTetris", True, (255, 255, 255))
		tr_title = ts_title.get_rect()

		txt_next_piece = pygame.font.Font('freesansbold.ttf', 16)
		ts_next_piece = txt_next_piece.render("Next piece", True, (255, 255, 255))
		tr_next_piece = ts_next_piece.get_rect()

		txt_level = pygame.font.Font('freesansbold.ttf', 20)
		ts_level = txt_level.render("Level: " + str(self.level), True, (255, 255, 255))
		tr_level = ts_level.get_rect()

		txt_score = pygame.font.Font('freesansbold.ttf', 20)
		ts_score = txt_score.render("Score: " + str(self.score), True, (255, 255, 255))
		tr_score = ts_score.get_rect()

		tr_title.center = (self.screen.get_width()//(4/3), 50)
		tr_next_piece.center = (self.screen.get_width()//(4/3), 100)
		tr_level.center = (self.screen.get_width()//(4/3), 270)
		tr_score.center = (self.screen.get_width()//(4/3), 320)

		# Blit the text
		screen.blit(ts_title, tr_title)
		screen.blit(ts_next_piece, tr_next_piece)
		screen.blit(ts_level, tr_level)
		screen.blit(ts_score, tr_score)

		# Draw the next piece in the right half of the canvas
		next_piece_height = len(self.next_piece.shape)
		next_piece_width = len(self.next_piece.shape[0])

		height_margin = (5 * self.block_size - next_piece_height * self.block_size)//2
		width_margin = ((5 * self.block_size - next_piece_width * self.block_size)//2)

		base_x = self.screen.get_width()//(4/3) - self.block_size * 2.5
		base_y = 100

		for row in range(next_piece_height):
			for col in range(next_piece_width):
				if(self.next_piece.shape[row][col]):
					pygame.draw.rect(self.screen, self.next_piece.color, pygame.Rect(base_x + width_margin + col * self.block_size, base_y + height_margin + row * self.block_size, self.block_size - 2, self.block_size - 2))

		x_base = self.current_piece.x
		y_base = self.current_piece.y

		# Draw the state of the blocks on the screen
		for row in range(self.rows):
			for col in range(self.cols):
				self.draw_block(col, row, self.state[row][col])

		# Draw the current piece's shadow
		self.draw_shadow()

		# Draw the current piece on the screen
		for row in range(len(self.current_piece.shape)):
			for col in range(len(self.current_piece.shape[0])):
				if self.current_piece.shape[row][col]:
					self.draw_block(x_base + col, y_base + row, self.current_piece.color)

	"""
	Checks if a block with given shape with a top-left corner (x, y)
	collides with the blocks already on the board
	"""
	def check_collision(self, shape, x, y):
		for row in range(len(shape)):
			for col in range(len(shape[0])):
				if(row + y > self.rows - 1 or col + x > self.cols - 1 or col + x < 0):
					return True
				elif(shape[row][col] and self.state[row + y][col + x].any() > 0):
					return True

		return False

	"""
	Checks for full rows on the board, removes them, and shifts all rows above
	them down by 1
	"""
	def remove_full_rows(self):
		updated_state = np.zeros((rows, cols), dtype=(int, 3))
		rows_removed = 0

		index = self.rows - 1
		# Shifts rows that are above down 
		for i in range(self.rows - 1, -1, -1):
			if(not self.is_row_full(self.state[i])):
				updated_state[index] = self.state[i]
				index -= 1
			else:
				rows_removed += 1

		self.state = updated_state
		self.lines_completed += rows_removed

		# If the lines completed is a multiple of 10, then advances the level
		if (self.lines_completed >= 10 and self.level < 10):
			self.lines_completed = 0
			self.level += 1

		# Updates the score
		if(rows_removed == 1):
			self.score += 40 * (self.level + 1)
		elif(rows_removed == 2):
			self.score += 100 * (self.level + 1)
		elif(rows_removed == 3):
			self.score += 300 * (self.level + 1)
		elif(rows_removed == 4):
			self.score += 1200 * (self.level + 1)

	# Determines if the row given by row is full of blocks
	def is_row_full(self, row):
		for block in row:
			if(sum(block) == 0):
				return False
		return True

	# Draws a block at coordinate x, y on the screen with a color given by color, with shadow mode optional
	def draw_block(self, x, y, color, shadow=False):
		x_ord = x * block_size
		y_ord = y * block_size

		pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(x_ord, y_ord, self.block_size, self.block_size))

		if shadow:
			pygame.draw.rect(self.screen, color, pygame.Rect(x_ord, y_ord, self.block_size, self.block_size))
			pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(x_ord + 2, y_ord + 2, self.block_size - 4, self.block_size - 4))
		else:
			pygame.draw.rect(self.screen, color, pygame.Rect(x_ord, y_ord, self.block_size - 2, self.block_size - 2))

	def draw_shadow(self):
		y_off = self.current_piece.y

		while(not self.check_collision(self.current_piece.shape, self.current_piece.x, y_off)):
			y_off += 1

		y_off -= 1
		x_off = self.current_piece.x

		for row in range(len(self.current_piece.shape)):
			for col in range(len(self.current_piece.shape[0])):
				if(self.current_piece.shape[row][col]):
					self.draw_block(x_off + col, y_off + row, self.current_piece.color, shadow=True)


if __name__ == "__main__":
	# Size of the game board
	rows, cols = 24, 10
	# Size of each block (in pixels)
	block_size = 20
	# Size of the screen canvas
	sw, sh = cols * block_size, rows * block_size
	screen = pygame.display.set_mode((2 * sw + 10, sh))
	pygame.display.set_caption("Tetris")
	pygame.display.flip()

	g = Game(rows, cols, block_size, screen)

	pygame.font.init()

	while g.running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				g.running = False

		# Update and render the game
		g.update(pygame.key.get_pressed())
		g.render()

		pygame.display.update()
		# Game should update 60 times per second
		pygame.time.Clock().tick(60)