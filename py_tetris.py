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
		self.level = 1
		self.score = 0
		self.block_size = block_size
		self.screen = screen
		self.state = np.zeros((rows, cols), dtype=(int, 3))
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
		self.current_piece = Piece(random.choice(self.possible_colors), random.choice(self.possible_shapes), self.cols//2, 0)
		self.next_piece = Piece(random.choice(self.possible_colors), random.choice(self.possible_shapes), self.cols//2, 0)

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

			self.current_piece = self.next_piece
			self.next_piece = Piece(random.choice(self.possible_colors), random.choice(self.possible_shapes), self.cols//2, 0)

			if(self.check_collision(self.current_piece.shape, self.current_piece.x, self.current_piece.y)):
				self.running = False

	def render(self):
		if not self.current_piece:
			return

		screen.fill((0, 0, 0))

		pygame.draw.line(self.screen, (255, 255, 255), (self.screen.get_width()//2, 0), (self.screen.get_width()//2, self.screen.get_height()), 10)

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

		screen.blit(ts_title, tr_title)
		screen.blit(ts_next_piece, tr_next_piece)
		screen.blit(ts_level, tr_level)
		screen.blit(ts_score, tr_score)

		pygame.draw.line(self.screen, (255, 255, 255), (self.screen.get_width()//(4/3) - self.block_size * 2.5, 120), (self.screen.get_width()//(4/3) + self.block_size * 2.5, 120), 4)
		pygame.draw.line(self.screen, (255, 255, 255), (self.screen.get_width()//(4/3) + self.block_size * 2.5, 120), (self.screen.get_width()//(4/3) + self.block_size * 2.5, 120 + self.block_size * 5), 4)
		pygame.draw.line(self.screen, (255, 255, 255), (self.screen.get_width()//(4/3) + self.block_size * 2.5, 120 + self.block_size * 5), (self.screen.get_width()//(4/3) - self.block_size * 2.5, 120 + self.block_size * 5), 4)
		pygame.draw.line(self.screen, (255, 255, 255), (self.screen.get_width()//(4/3) - self.block_size * 2.5, 120 + self.block_size * 5), (self.screen.get_width()//(4/3) - self.block_size * 2.5, 120), 4)

		next_piece_height = len(self.next_piece.shape)
		next_piece_width = len(self.next_piece.shape[0])

		height_margin = (5 * self.block_size - next_piece_height * self.block_size)//2
		width_margin = ((5 * self.block_size - next_piece_width * self.block_size)//2)

		base_x = self.screen.get_width()//(4/3) - self.block_size * 2.5
		base_y = 120

		for row in range(next_piece_height):
			for col in range(next_piece_width):
				if(self.next_piece.shape[row][col]):
					pygame.draw.rect(self.screen, self.next_piece.color, pygame.Rect(base_x + width_margin + col * self.block_size, base_y + height_margin + row * self.block_size, self.block_size - 2, self.block_size - 2))

		print(height_margin)
		print(width_margin)

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
	screen = pygame.display.set_mode((2 * sw + 10, sh))
	pygame.display.set_caption("Tetris")
	pygame.display.flip()

	g = Game(rows, cols, block_size, screen)

	pygame.font.init()

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