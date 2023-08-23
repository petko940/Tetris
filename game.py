import random
import sys
import time

import pygame
from files.other.figures import *
import score_manager

pygame.init()
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 501
BLOCK_SIZE = 25
ROWS = 20
COLS = 10
WHITE = (255, 255, 255)

font_draw = pygame.font.Font(None, 30)
font_score = pygame.font.Font('files/other/custom_font.ttf', 30)
font_lines = pygame.font.Font(None, 36)

font_combo = pygame.font.Font(None, 36)

comboX1_font = pygame.font.Font(None, 36)
comboX2_font = pygame.font.Font(None, 41)
comboX3_font = pygame.font.Font(None, 46)
comboX4_font = pygame.font.Font(None, 51)

start_time = time.time()


class Tetris:
    def __init__(self):
        self.last_combo_display_time = None
        self.FALL_SPEED = 20

        self.s_key_pressed = None

        self.fallen_pieces = []

        self.previous_pieces_color = None
        self.current_piece_color = None

        self.next_piece = None
        self.next_piece_color = None

        self.current_piece = None
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Tetris')

        self.clock = pygame.time.Clock()
        self.game_board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.time_since_last_fall = 0

        self.current_figure_to_rotate = None
        self.current_figure = None

        self.rotate_pieces = {
            figure_keys[0]: deque([FIGURES[0], FIGURES[1]]),
            figure_keys[1]: deque([FIGURES[2], FIGURES[3], FIGURES[4], FIGURES[5]]),
            figure_keys[2]: deque([FIGURES[6], FIGURES[7]]),
            figure_keys[3]: deque([FIGURES[8], FIGURES[9]]),
            figure_keys[4]: deque([FIGURES[10], FIGURES[11], FIGURES[12], FIGURES[13]]),
            figure_keys[5]: deque([FIGURES[14], FIGURES[15], FIGURES[16], FIGURES[17]]),
            figure_keys[6]: deque([FIGURES[18]])
        }

        self.points = 0
        self.lines = 0
        self.combo = 0
        self.show_combo = False

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
                if self.game_board[row][col]:
                    pygame.draw.rect(
                        self.screen,
                        self.game_board[row][col],
                        ((col * BLOCK_SIZE) + 2, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                    )

    def draw_current_figure(self, figure, x, y):
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

    def draw_next_piece(self, next_piece):
        next_piece_color = FIGURES_COLOR[next_piece['shape']]
        shape = FIGURES[next_piece['shape']]

        for row in range(len(shape)):
            for col in range(len(shape[0])):
                if shape[row][col]:
                    rect = pygame.Rect(
                        (col + COLS + 2) * BLOCK_SIZE - 10,
                        (row + 4) * BLOCK_SIZE,
                        BLOCK_SIZE,
                        BLOCK_SIZE,
                    )
                    pygame.draw.rect(
                        self.screen,
                        next_piece_color,
                        rect,
                    )

        '''Border of next piece'''
        width = len(shape[0]) * BLOCK_SIZE + 20
        height = len(shape) * BLOCK_SIZE + 20

        border_x = (COLS + 2) * BLOCK_SIZE - BLOCK_SIZE * 0.25 - 13
        border_y = 4 * BLOCK_SIZE - BLOCK_SIZE * 0.25 - 3

        pygame.draw.rect(
            self.screen,
            (255, 255, 255),  # White color
            pygame.Rect(border_x, border_y, width, height),
            1  # Border width
        )

    def spawn_piece(self):
        self.current_piece = {
            'shape': self.next_piece['shape'],
            'x': COLS // 2,
            'y': 0,
        }
        self.current_piece_color = self.next_piece_color

        self.next_piece = {
            'shape': random.randint(0, len(FIGURES) - 1),
            'x': COLS // 2,
            'y': 0,
        }
        self.next_piece_color = FIGURES_COLOR[self.next_piece['shape']]

    def move_piece_down(self):
        new_y = self.current_piece['y'] + 1
        if not self.check_collision(self.current_piece['shape'], self.current_piece['x'], new_y):
            self.current_piece['y'] = new_y
        else:
            self.lock_piece()
            self.spawn_piece()
            self.show_combo = False

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

        self.previous_pieces_color = self.current_piece_color
        self.current_piece_color = FIGURES_COLOR[self.current_piece['shape']]
        self.score(0)
        if y == 0:
            self.game_over()

    def move_piece_left(self):
        new_x = self.current_piece['x'] - 1
        if not self.check_collision(self.current_piece['shape'], new_x, self.current_piece['y']):
            self.current_piece['x'] = new_x

    def move_piece_right(self):
        new_x = self.current_piece['x'] + 1
        if not self.check_collision(self.current_piece['shape'], new_x, self.current_piece['y']):
            self.current_piece['x'] = new_x

    def fast_down(self):
        new_x = self.current_piece['x']
        if self.s_key_pressed:
            self.FALL_SPEED = 2
        else:
            self.FALL_SPEED = 20

        if not self.check_collision(self.current_piece['shape'], new_x, self.current_piece['y']):
            self.current_piece['x'] = new_x

    def filled_line(self):
        filled_lines = []
        for i, row in enumerate(self.game_board):
            if 0 not in row:
                filled_lines.append(i)

        if filled_lines:
            self.destroy_effect(filled_lines)
            for x in filled_lines:
                del self.game_board[x]
                self.game_board.insert(0, [0 for _ in range(len(self.game_board[0]))])

        return filled_lines

    def destroy_effect(self, rows):
        destroy_line_music_path = 'files/music/destroy_line.mp3'
        music_channel = pygame.mixer.Channel(1)
        music_channel.play(pygame.mixer.Sound(destroy_line_music_path))

        for row in rows:
            self.game_board[row] = [self.previous_pieces_color for _ in range(COLS)]

        self.draw_board()
        pygame.display.flip()
        pygame.time.delay(200)

        for row in rows:
            self.game_board[row] = [0 for _ in range(COLS)]

        self.draw_board()
        pygame.display.flip()

    def rotate_piece(self):
        rotate_times = 0
        for x in self.rotate_pieces[self.current_figure_to_rotate]:
            if x == self.current_figure:
                break
            rotate_times += 1

        self.rotate_pieces[self.current_figure_to_rotate].rotate(-rotate_times - 1)

        new_shape = self.rotate_pieces[self.current_figure_to_rotate][0]
        new_x, new_y = self.current_piece['x'], self.current_piece['y']
        if new_x < 0:
            new_x = 0
        elif new_x + len(new_shape[0]) > COLS:
            new_x = COLS - len(new_shape[0])

        if new_y + len(new_shape) > ROWS:
            new_y = ROWS - len(new_shape)

        self.current_piece['shape'] = FIGURES.index(new_shape)
        self.current_piece['x'] = new_x
        self.current_piece['y'] = new_y
        self.draw_board()

    def score(self, lines):
        scores = {
            0: 10,
            1: 100,
            2: 200,
            3: 300,
            4: 400,
        }
        self.points += scores[lines]

    def draw_score(self):
        score_str = str(self.points).zfill(6)
        text_points = font_score.render(score_str, True, WHITE)
        self.screen.blit(text_points, (270, 220))

        text_hi_score = font_draw.render('High Score', True, WHITE)
        self.screen.blit(text_hi_score, (270, 420))
        text_hi_score = font_score.render(str(score_manager.hi_score).zfill(6), True, WHITE)
        self.screen.blit(text_hi_score, (270, 450))

    def draw_lines(self, num_lines):
        text_lines = font_lines.render('Lines: ', True, WHITE)
        self.screen.blit(text_lines, (264, 285))

        number_lines = font_score.render(str(num_lines), True, WHITE)
        self.screen.blit(number_lines, (344, 283))

    def game_over(self):
        if self.points > score_manager.hi_score:
            score_manager.hi_score = self.points

        self.points = 0
        game_over_image = pygame.image.load("files/other/game_over.jpg")

        return_to_menu = False

        pygame.mixer.music.stop()
        pygame.mixer.music.load("files/music/hi-score-music.mp3")
        pygame.mixer.music.play(-1)
        while not return_to_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    return_to_menu = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    return_to_menu = True

            self.screen.fill((0, 0, 0))
            self.screen.blit(game_over_image, (0, 0))

            hi_score_text = font_draw.render(f'High Score: {score_manager.hi_score}', False, WHITE)
            self.screen.blit(hi_score_text, (130, 220))

            lines_destroyed = font_draw.render(f'Lines Destroyed: {self.lines}', False, WHITE)
            self.screen.blit(lines_destroyed, (110, 257))

            press_any_key_text = font_draw.render('Press any key to return to menu...', False, WHITE)
            self.screen.blit(press_any_key_text, (30, 297))

            pygame.display.flip()

        from menu import Menu
        menu = Menu()
        menu.run()

    def combos(self):
        text_combo = font_combo.render(f"Combo:", True, WHITE)
        self.screen.blit(text_combo, (260, 350))

        if self.combo == 1:
            GREEN = (0, 255, 0)
            text_combo = comboX1_font.render(f"1X", True, GREEN)
            self.screen.blit(text_combo, (355, 350))
        elif self.combo == 2:
            ORANGE = (255, 165, 0)
            text_combo = comboX2_font.render(f"2X", True, ORANGE)
            self.screen.blit(text_combo, (355, 350))
        elif self.combo == 3:
            RED = (255, 0, 0)
            text_combo = comboX3_font.render(f"3X", True, RED)
            self.screen.blit(text_combo, (355, 350))
        elif self.combo == 4:
            PURPLE = (255, 0, 255)
            text_combo = comboX4_font.render(f"4X", True, PURPLE)
            self.screen.blit(text_combo, (355, 350))

        """edno ribarche dade coda
        text_combo = font_combo.render(f"Combo:", True, WHITE)
        self.screen.blit(text_combo, (260, 350))

        combos = {
            1: {"color": (0, 255, 0), "text": "1X", "font": comboX1_font},
            2: {"color": (255, 165, 0), "text": "2X", "font": comboX2_font},
            3: {"color": (255, 0, 0), "text": "3X", "font": comboX3_font},
            4: {"color": (255, 0, 255), "text": "4X", "font": comboX4_font},
            "pos": (355, 350),
        }

        color = combos[self.combo]["color"]
        message = combos[self.combo]["text"]
        text_combo = combos[self.combo]["font"].render(message, True, color)

        self.screen.blit(text_combo, combos["pos"])
        """

    def run(self):
        path = "files/music/in_game_music.mp3"
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(-1)
        font = pygame.font.Font(None, 36)
        text_next = font.render("Next", True, WHITE)

        self.next_piece = {
            'shape': random.randint(0, len(FIGURES) - 1),
            'x': COLS // 2,
            'y': 0,
        }
        self.next_piece_color = FIGURES_COLOR[self.next_piece['shape']]

        self.spawn_piece()

        time_since_last_move_lr = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        self.s_key_pressed = True
                        self.fast_down()
                    elif event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                        self.rotate_piece()

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        self.s_key_pressed = False
                        self.fast_down()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                current_time = pygame.time.get_ticks()
                if current_time - time_since_last_move_lr >= 80:
                    self.move_piece_left()
                    time_since_last_move_lr = current_time
            elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                current_time = pygame.time.get_ticks()
                if current_time - time_since_last_move_lr >= 80:
                    self.move_piece_right()
                    time_since_last_move_lr = current_time

            self.screen.fill((0, 0, 0))
            self.draw_board()
            self.draw_current_figure(
                self.current_piece['shape'],
                self.current_piece['x'],
                self.current_piece['y'],
            )

            self.time_since_last_fall += self.clock.tick()
            if self.time_since_last_fall >= self.FALL_SPEED:
                self.move_piece_down()
                self.time_since_last_fall = 0

            self.draw_lines(self.lines)

            filled_lines = self.filled_line()
            if filled_lines:
                self.score(len(filled_lines))
                self.combo += 1
                self.show_combo = True
                if len(filled_lines) == 1:
                    self.lines += 1
                elif len(filled_lines) == 2:
                    self.lines += 2
                elif len(filled_lines) == 3:
                    self.lines += 3
                elif len(filled_lines) == 4:
                    self.lines += 4

            if self.show_combo:
                self.combos()
            else:
                self.points += self.combo * 50
                self.combo = 0

            if self.current_piece is None:
                self.spawn_piece()

            shape = self.current_piece['shape']
            for key, value in self.rotate_pieces.items():
                if FIGURES[shape] in value:
                    self.current_figure = FIGURES[shape]
                    self.current_figure_to_rotate = key
                    break

            self.screen.blit(text_next, (300, 50))
            self.draw_next_piece(self.next_piece)

            self.draw_score()

            '''temp'''
            current_time = time.time()
            elapsed_time = current_time - start_time
            timer_text = f"Time: {elapsed_time} seconds"  # Convert to int to remove decimals

            font = pygame.font.Font(None, 36)
            timer_surface = font.render(timer_text, True, (255, 255, 255))  # White text_next
            # self.screen.blit(timer_surface, (250, 10))
            ''''''

            pygame.display.flip()
            self.clock.tick(60)
