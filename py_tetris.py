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
		#self.rotate_mat_90 = [[cos(to_radians(90)), -1 * sin(to_radians(90))], 
							  #b[sin(to_radians(90)), cos(to_radians(90))]]

	def init_piece(self, color, shape):
		self.current_piece = Piece(color, shape, self.cols//2, 0)

	def update(self, keys):
		if not self.current_piece:
			return

		if self.current_piece.x != 0 and keys[pygame.K_LEFT]:
			self.current_piece.x -= 1
		elif (self.current_piece.x) != (self.cols - len(self.current_piece.shape[0])) and keys[pygame.K_RIGHT]:
			self.current_piece.x += 1

		if(keys[pygame.K_UP]):
			self.rotate_shape_90()

		if(self.current_piece.y == self.rows - len(self.current_piece.shape) or self.check_collision()):
			x_base = self.current_piece.x
			y_base = self.current_piece.y

			for row in range(len(self.current_piece.shape)):
				for col in range(len(self.current_piece.shape[0])):
					if(self.current_piece.shape[row][col]):
						self.state[y_base + row][x_base + col] = self.current_piece.color
			

			self.init_piece(random.choice(self.possible_colors), random.choice(self.possible_shapes))
		else:
			self.current_piece.y += 1

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

	def check_collision(self):
		final_row = self.current_piece.shape[len(self.current_piece.shape) - 1]
		x_base = self.current_piece.x
		y_base = self.current_piece.y + len(self.current_piece.shape) - 1


		for i in range(len(final_row)):
			block = final_row[i]
			x_off = x_base + i

			if(block and self.state[y_base + 1][x_off].any() > 0):
				return True

		return False

	def rotate_shape_90(self):
		orig_rows = len(self.current_piece.shape)
		orig_cols = len(self.current_piece.shape[0])

		rotated_shape = np.ones((orig_cols, orig_rows), dtype=bool)
		print(rotated_shape)

		for row in range(orig_rows):
			for col in range(orig_cols):
				rotated_shape[col][row] = self.current_piece.shape[row][col]

		self.current_piece.shape = rotated_shape

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

	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		g.update(pygame.key.get_pressed())
		g.render()

		pygame.display.update()
		if(pygame.key.get_pressed()[pygame.K_DOWN]):
			pygame.time.Clock().tick(16)
		else:
			pygame.time.Clock().tick(8)