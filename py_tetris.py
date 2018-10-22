import pygame
import random
import numpy as np

class Piece:
	def __init__(self, color, shape, x, y):
		self.color = color
		self.shape = shape
		self.x = x
		self.y = y

class Game:
	def __init__(self, rows, cols, block_size, screen):
		self.rows = rows
		self.cols = cols
		self.block_size = block_size
		self.screen = screen
		self.state = np.zeros((rows, cols), dtype=(int, 3))
		self.current_piece = None
		self.running = True
		self.possible_shapes = [[[True, True, True, True]], 
								[[True, False, False], [True, True, True]], 
								[[False, False, True], [True, True, True]], 
								[[True, True], [True, True]], 
								[[False, True, True], [True, True, False]],
								[[False, True, False], [True, True, True]], 
								[[True, True, False], [False, True, True]]]
		self.possible_colors = [(0, 0xff, 0xff),
								(0, 0, 0xff),
								(0xff, 0xa5, 0x00),
								(0xff, 0xff, 0x00),
								(0x00, 0xff, 0x00),
								(0x8b, 0x00, 0x8b),
								(0xff, 0x00, 0x00)]

	def init_piece(self, color, shape):
		self.current_piece = Piece(color, shape, self.cols//2, 0)

	def update(self, keys):
		if not self.current_piece:
			return

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

		if(not self.check_collision(self.current_piece.shape, self.current_piece.x, self.current_piece.y + 1)):
			self.current_piece.y += 1
		else:
			x_base = self.current_piece.x
			y_base = self.current_piece.y
			for row in range(len(self.current_piece.shape)):
				for col in range(len(self.current_piece.shape[0])):
					if(self.current_piece.shape[row][col]):
						self.state[y_base + row][x_base + col] = self.current_piece.color

			self.remove_full_rows()

			self.init_piece(random.choice(self.possible_colors), random.choice(self.possible_shapes))

			if(self.check_collision(self.current_piece.shape, self.current_piece.x, self.current_piece.y)):
				self.running = False

	def render(self):
		if not self.current_piece:
			return

		screen.fill((0, 0, 0))

		x_base = self.current_piece.x
		y_base = self.current_piece.y

		for row in range(self.rows):
			for col in range(self.cols):
				self.draw_block(col, row, self.state[row][col])

		for row in range(len(self.current_piece.shape)):
			for col in range(len(self.current_piece.shape[0])):
				if self.current_piece.shape[row][col]:
					self.draw_block(x_base + col, y_base + row, self.current_piece.color)

	def check_collision(self, shape, x, y):
		for row in range(len(shape)):
			for col in range(len(shape[0])):
				if(row + y > self.rows - 1 or col + x > self.cols - 1 or col + x < 0):
					return True
				elif(shape[row][col] and self.state[row + y][col + x].any() > 0):
					return True

		return False

	def remove_full_rows(self):
		updated_state = np.zeros((rows, cols), dtype=(int, 3))

		index = self.rows - 1
		for i in range(self.rows - 1, -1, -1):
			if(not self.is_row_full(self.state[i])):
				updated_state[index] = self.state[i]
				index -= 1

		self.state = updated_state

	def is_row_full(self, row):
		for block in row:
			if(sum(block) == 0):
				return False
		return True

	def draw_block(self, x, y, color):
		x_ord = x * block_size
		y_ord = y * block_size

		pygame.draw.rect(self.screen, color, pygame.Rect(x_ord, y_ord, self.block_size - 2, self.block_size - 2))

if __name__ == "__main__":
	rows, cols = 24, 10
	block_size = 20
	sw, sh = cols * block_size, rows * block_size
	screen = pygame.display.set_mode((sw, sh))
	pygame.display.set_caption("Tetris")
	pygame.display.flip()

	g = Game(rows, cols, block_size, screen)
	g.init_piece(random.choice(g.possible_colors), random.choice(g.possible_shapes))

	while g.running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				g.running = False

		g.update(pygame.key.get_pressed())
		g.render()

		pygame.display.update()
		if(pygame.key.get_pressed()[pygame.K_DOWN]):
			pygame.time.Clock().tick(20)
		else:
			pygame.time.Clock().tick(6)