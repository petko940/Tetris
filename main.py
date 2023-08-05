import random
import time

import pygame
from figures import *

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 501
BLOCK_SIZE = 25
ROWS = 20
COLS = 10


class Tetris:
    def __init__(self):
        self.s_key_pressed = False
        self.FALL_SPEED = 30

        self.fallen_pieces = []
        self.current_piece_color = None

        self.current_piece = None
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Tetris')

        self.clock = pygame.time.Clock()
        self.game_board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.time_since_last_fall = 0

        self.current_figure_to_rotate = None
        self.current_figure = None

        self.rotate_pieces = {figure_keys[0]: deque([FIGURES[0], FIGURES[1]]),
                              figure_keys[1]: deque([FIGURES[2], FIGURES[3], FIGURES[4], FIGURES[5]]),
                              figure_keys[2]: deque([FIGURES[6], FIGURES[7]]),
                              figure_keys[3]: deque([FIGURES[8], FIGURES[9]]),
                              figure_keys[4]: deque([FIGURES[10], FIGURES[11], FIGURES[12], FIGURES[13]]),
                              figure_keys[5]: deque([FIGURES[14], FIGURES[15], FIGURES[16], FIGURES[17]]),
                              figure_keys[6]: deque([FIGURES[18]])}

        self.points = 0

        self.timer = 0
        self.timer_interval = 1000

    def draw_board(self):
        for row in range(ROWS):
            for col in range(COLS):
                pygame.draw.rect(
                    self.screen,
                    (0, 0, 0),
                    ((col * BLOCK_SIZE) + 2, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                )
                pygame.draw.rect(
                    self.screen,
                    (255, 255, 255),
                    ((col * BLOCK_SIZE) + 2, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                    1,
                )

        for row in range(ROWS):
            for col in range(COLS):
                if self.game_board[row][col]:
                    pygame.draw.rect(
                        self.screen,
                        self.game_board[row][col],
                        ((col * BLOCK_SIZE) + 2, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                    )

        if self.current_piece is not None:
            self.draw_figure(
                self.current_piece['shape'],
                self.current_piece['x'],
                self.current_piece['y']
            )

    def draw_figure(self, figure, x, y):
        shape = FIGURES[figure]
        for row in range(len(shape)):
            for col in range(len(shape[0])):
                if shape[row][col]:
                    rect = pygame.Rect(
                        (col + x) * BLOCK_SIZE + 2,
                        (row + y) * BLOCK_SIZE,
                        BLOCK_SIZE,
                        BLOCK_SIZE,
                    )
                    pygame.draw.rect(
                        self.screen,
                        self.current_piece_color,
                        rect,
                    )

    def spawn_piece(self):
        self.current_piece = {
            'shape': random.randint(0, len(FIGURES) - 1),
            'x': COLS // 2,
            'y': 0,
        }
        self.current_piece_color = FIGURES_COLOR[self.current_piece['shape']]

    def move_piece_down(self):
        if self.current_piece is not None:
            new_y = self.current_piece['y'] + 1
            if not self.check_collision(self.current_piece['shape'], self.current_piece['x'], new_y):
                self.current_piece['y'] = new_y
            else:
                self.lock_piece()
                self.spawn_piece()

    def check_collision(self, figure, x, y):
        shape = FIGURES[figure]
        for row in range(len(shape)):
            for col in range(len(shape[0])):
                if shape[row][col]:
                    if y + row >= ROWS or x + col < 0 or x + col >= COLS or self.game_board[y + row][x + col]:
                        return True
        return False

    def lock_piece(self):
        shape = FIGURES[self.current_piece['shape']]
        x, y = self.current_piece['x'], self.current_piece['y']
        color = self.current_piece_color
        for row in range(len(shape)):
            for col in range(len(shape[0])):
                if shape[row][col]:
                    self.game_board[y + row][x + col] = color

        self.current_piece_color = FIGURES_COLOR[self.current_piece['shape']]

    def move_piece_left(self):
        if self.current_piece is not None:
            new_x = self.current_piece['x'] - 1
            if not self.check_collision(self.current_piece['shape'], new_x, self.current_piece['y']):
                self.current_piece['x'] = new_x

    def move_piece_right(self):
        if self.current_piece is not None:
            new_x = self.current_piece['x'] + 1
            if not self.check_collision(self.current_piece['shape'], new_x, self.current_piece['y']):
                self.current_piece['x'] = new_x

    def fast_down(self):
        if self.current_piece is not None:
            new_x = self.current_piece['x']
            if self.s_key_pressed:
                self.FALL_SPEED = 2
            else:
                self.FALL_SPEED = 30

            if not self.check_collision(self.current_piece['shape'], new_x, self.current_piece['y']):
                self.current_piece['x'] = new_x
        else:
            self.FALL_SPEED = 30

    def filled_line(self):
        filled_lines = []
        for i, row in enumerate(self.game_board):
            if 0 not in row:
                filled_lines.append(i)
        if filled_lines:
            for x in filled_lines:
                del self.game_board[x]
                self.game_board.insert(0, [0 for _ in range(len(self.game_board[0]))])
        return filled_lines

    def rotate_piece(self):
        rotate_times = 0
        for x in self.rotate_pieces[self.current_figure_to_rotate]:
            if x == self.current_figure:
                break
            rotate_times += 1

        self.rotate_pieces[self.current_figure_to_rotate].rotate(-rotate_times - 1)

        new_shape = self.rotate_pieces[self.current_figure_to_rotate][0]
        self.current_piece['shape'] = FIGURES.index(new_shape)

        self.draw_board()

    def run(self):
        self.spawn_piece()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        exit()
                    elif event.key == pygame.K_a:
                        self.move_piece_left()
                    elif event.key == pygame.K_d:
                        self.move_piece_right()
                    elif event.key == pygame.K_s:
                        self.s_key_pressed = True
                        self.fast_down()
                    elif event.key == pygame.K_SPACE:
                        self.rotate_piece()

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_s:
                        self.s_key_pressed = False
                        self.fast_down()

            self.screen.fill((0, 0, 0))
            self.draw_board()
            self.draw_figure(
                self.current_piece['shape'],
                self.current_piece['x'],
                self.current_piece['y'],
            )

            self.time_since_last_fall += self.clock.tick()
            if self.time_since_last_fall >= self.FALL_SPEED:
                self.move_piece_down()
                self.time_since_last_fall = 0

            filled_lines = self.filled_line()
            if filled_lines:
                self.points += len(filled_lines)
                print("score: " , self.points)

            if self.current_piece is None:
                self.spawn_piece()

            shape = self.current_piece['shape']
            for key, value in rotate_piece.items():
                if FIGURES[shape] in value:
                    self.current_figure = FIGURES[shape]
                    self.current_figure_to_rotate = key
                    break

            pygame.display.flip()
            self.clock.tick(60)


game = Tetris()
game.run()
