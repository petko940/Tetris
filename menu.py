import sys
import pygame
import score_manager

pygame.init()


SCREEN_WIDTH = 400
SCREEN_HEIGHT = 501
FONT = pygame.font.Font("files/other/menu_font.ttf", 29)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
LIGHT_BLUE = (0, 255, 255)
PURPLE = (128, 0, 128)

start_surface = FONT.render("START", True, YELLOW)
exit_surface = FONT.render("EXIT", True, RED)

MENU_FONT = pygame.font.Font("files/other/menu_font.ttf", 25)


class Menu:
    def __init__(self):
        pygame.display.set_caption('Tetris')
        self.last_color_change_time = pygame.time.get_ticks()
        self.text_colors = [RED, ORANGE, YELLOW, GREEN, LIGHT_BLUE, PURPLE]
        self.current_color_index = 0
        self.current_color = self.text_colors[self.current_color_index]

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background = pygame.image.load('files/other/menu_image.png')
        self.start_button_rect = pygame.Rect(155, 230, 89, 22)
        self.exit_button_rect = pygame.Rect(165, 287, 68, 22)

    def draw_buttons(self, x, y, surface):
        self.screen.blit(surface, (x, y))

    def countdown_start(self):
        path = "files/music/countdown.mp3"
        channel = pygame.mixer.Channel(1)
        channel.play(pygame.mixer.Sound(path))

        font = pygame.font.Font(None, 150)

        countdown_interval = 600
        current_time = pygame.time.get_ticks()

        for i in range(3, 0, -1):
            self.screen.fill(BLACK)
            countdown_text = font.render(str(i), True, WHITE)
            countdown_rect = countdown_text.get_rect(center=self.screen.get_rect().center)
            self.screen.blit(countdown_text, countdown_rect)
            pygame.display.flip()

            while pygame.time.get_ticks() - current_time < countdown_interval:
                pygame.event.pump()

            current_time += countdown_interval

        self.screen.fill(BLACK)
        pygame.display.flip()

    def exit_images(self, images):
        clock = pygame.time.Clock()
        delay = 600

        for i in range(len(images)):
            self.screen.fill(BLACK)
            self.screen.blit(images[i], (0, 0))
            pygame.display.flip()

            start_time = pygame.time.get_ticks()
            elapsed_time = 0

            while elapsed_time < delay:
                pygame.event.pump()
                clock.tick(30)
                elapsed_time = pygame.time.get_ticks() - start_time

    def run(self):
        pygame.mixer.stop()
        music_path = "files/music/menu_music.mp3"
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_button_rect.collidepoint(event.pos):
                        self.countdown_start()

                        from game import Tetris
                        game = Tetris()
                        game.run()

                    elif self.exit_button_rect.collidepoint(event.pos):
                        pygame.mixer.music.stop()
                        path = "files/music/exit.mp3"
                        pygame.mixer.music.load(path)
                        pygame.mixer.music.play()

                        image_paths = [
                            "files/exit_images/1.png",
                            "files/exit_images/2.png",
                            "files/exit_images/3.png"
                        ]
                        images = [pygame.image.load(path) for path in image_paths]
                        self.exit_images(images)
                        pygame.quit()
                        sys.exit()

            self.screen.blit(self.background, (0, 0))

            self.draw_buttons(
                155,
                223,
                start_surface
            )
            self.draw_buttons(
                165,
                280,
                exit_surface
            )

            text_score = MENU_FONT.render('HI-SCORE', True, GREEN)
            self.screen.blit(text_score, (7, 250))

            current_time = pygame.time.get_ticks()
            time_since_color_change = current_time - self.last_color_change_time

            if time_since_color_change >= 1000:
                self.last_color_change_time = current_time
                self.current_color_index = (self.current_color_index + 1) % len(self.text_colors)
                self.current_color = self.text_colors[self.current_color_index]

            from game import font_score
            text_score = MENU_FONT.render('HI-SCORE', True, self.current_color)
            self.screen.blit(text_score, (7, 250))

            hi_score_text = font_score.render(f'{str(score_manager.hi_score).zfill(6)}', False, self.current_color)
            self.screen.blit(hi_score_text, (280, 250))

            pygame.display.flip()


menu = Menu()
menu.run()
